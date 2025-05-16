# AIFreeCADWorkbench/Core/CodeExecutor.py
import FreeCAD
import FreeCADGui
# Import common modules that scripts are likely to use, to make them available in exec's scope
import Part
import Draft
import Sketcher
import math # Often useful
import signal
from .constants import SCRIPT_EXECUTION_TIMEOUT, ALLOWED_MODULES, BLOCKED_BUILTINS, ERRORS

class CodeExecutor:
    """Executes FreeCAD Python scripts with security measures and timeout protection."""
    
    def __init__(self):
        """Initialize the code executor with security measures."""
        self._setup_sandbox()

    def _setup_sandbox(self):
        """Configure the restricted execution environment."""
        self.safe_builtins = dict(__builtins__)
        for func in BLOCKED_BUILTINS:
            if func in self.safe_builtins:
                del self.safe_builtins[func]

    def _validate_script(self, script):
        """Validate script doesn't import unauthorized modules."""
        import ast
        try:
            tree = ast.parse(script)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        module = name.name.split('.')[0]
                        if module not in ALLOWED_MODULES:
                            return False, ERRORS['invalid_module'].format(module)
                elif isinstance(node, ast.ImportFrom):
                    if node.module.split('.')[0] not in ALLOWED_MODULES:
                        return False, ERRORS['invalid_module'].format(node.module)
            return True, ""
        except SyntaxError as e:
            return False, f"Syntax error in script: {str(e)}"

    def _timeout_handler(self, signum, frame):
        """Handle script execution timeout."""
        raise TimeoutError(ERRORS['execution_timeout'].format(SCRIPT_EXECUTION_TIMEOUT))

    def execute_script(self, script_string):
        """Execute a FreeCAD script with security measures and timeout protection."""
        log_output = []
        doc = FreeCAD.ActiveDocument

        if not doc:
            # If no document is open, create one.
            # Some scripts might assume a document exists.
            try:
                doc = FreeCAD.newDocument("AI_Generated_Doc")
                FreeCAD.Console.PrintMessage("Created new document: AI_Generated_Doc\n")
                log_output.append("Info: No active document, created 'AI_Generated_Doc'.")
            except Exception as e:
                log_output.append(f"Error: Could not create a new document: {str(e)}")
                FreeCAD.Console.PrintError(f"Document creation error: {str(e)}\n")
                return False, "\n".join(log_output)
        
        # Validate script first
        is_valid, validation_msg = self._validate_script(script_string)
        if not is_valid:
            log_output.append(validation_msg)
            return False, "\n".join(log_output)

        # Set up timeout
        signal.signal(signal.SIGALRM, self._timeout_handler)
        signal.alarm(SCRIPT_EXECUTION_TIMEOUT)

        # Make common modules and the active document available to the executed script
        # This creates a controlled global scope for the exec call.
        script_globals = {
            "App": FreeCAD, # App is often used as an alias for FreeCAD module
            "FreeCAD": FreeCAD,
            "Gui": FreeCADGui,
            "Part": Part,
            "Draft": Draft,
            "Sketcher": Sketcher,
            "math": math,
            "doc": doc, # Provide current document
            "__builtins__": self.safe_builtins
        }

        transaction_name = "AI Generated Script"
        if doc:
            doc.openTransaction(transaction_name) # Start transaction for undo
            FreeCAD.Console.PrintMessage(f"Starting transaction: {transaction_name}\n")

        try:
            FreeCAD.Console.PrintMessage(f"Executing script:\n---\n{script_string}\n---\n")
            # Execute the script_string in the defined global scope
            exec(script_string, script_globals)
            
            if doc:
                doc.recompute() # Crucial after modifications
                FreeCAD.Console.PrintMessage("Document recomputed.\n")
            log_output.append("Script executed successfully (preliminary).")

        except TimeoutError as e:
            log_output.append(str(e))
            if doc and doc.isTransactionActive():
                doc.abortTransaction()
                FreeCAD.Console.PrintMessage("Transaction aborted due to timeout.\n")
            return False, "\n".join(log_output)
        except Exception as e:
            log_output.append(f"Error during script execution: {str(e)}")
            FreeCAD.Console.PrintError(f"Script Execution Error: {str(e)}\n")
            if doc and doc.isTransactionActive(): # Check if transaction is still active
                doc.abortTransaction()
                FreeCAD.Console.PrintMessage("Transaction aborted due to error.\n")
            return False, "\n".join(log_output)
        
        finally:
            signal.alarm(0)  # Disable alarm
            if doc and doc.isTransactionActive():
                doc.commitTransaction()
                FreeCAD.Console.PrintMessage("Transaction committed.\n")

        # Attempt to fit the view after execution
        try:
            if Gui.ActiveDocument and Gui.ActiveDocument.ActiveView:
                Gui.SendMsgToActiveView("ViewFit")
        except Exception as e:
            FreeCAD.Console.PrintWarning(f"Could not ViewFit: {str(e)}\n")
            
        return True, "\n".join(log_output)