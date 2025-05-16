# AIFreeCADWorkbench/Core/CodeExecutor.py
import FreeCAD
import FreeCADGui
# Import common modules that scripts are likely to use, to make them available in exec's scope
import Part
import Draft
import Sketcher
import math # Often useful

class CodeExecutor:
    def execute_script(self, script_string):
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
            # You can add more standard modules here if commonly needed
        }

        # Store original stdout/stderr and redirect for capturing script output (Advanced)
        # For simplicity in this initial version, we'll rely on FreeCAD's console.
        
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

        except Exception as e:
            log_output.append(f"Error during script execution: {str(e)}")
            FreeCAD.Console.PrintError(f"Script Execution Error: {str(e)}\n")
            if doc and doc.isTransactionActive(): # Check if transaction is still active
                doc.abortTransaction()
                FreeCAD.Console.PrintMessage("Transaction aborted due to error.\n")
            return False, "\n".join(log_output)
        
        finally:
            if doc and doc.isTransactionActive():
                doc.commitTransaction()
                FreeCAD.Console.PrintMessage("Transaction committed.\n")
            # Restore stdout/stderr if redirected

        # Attempt to fit the view after execution
        try:
            if Gui.ActiveDocument and Gui.ActiveDocument.ActiveView:
                Gui.SendMsgToActiveView("ViewFit")
        except Exception as e:
            FreeCAD.Console.PrintWarning(f"Could not ViewFit: {str(e)}\n")
            
        return True, "\n".join(log_output)