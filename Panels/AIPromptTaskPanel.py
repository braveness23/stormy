# AIFreeCADWorkbench/Panels/AIPromptTaskPanel.py
import FreeCAD
import FreeCADGui
from PySide2 import QtCore, QtWidgets

from ..Core.LLMManager import LLMManager
from ..Core.CodeExecutor import CodeExecutor
from ..Core.PromptEngine import PromptEngine
from ..Core.Settings import SettingsManager # To get settings

class AIPromptTaskPanel:
    def __init__(self):
        self.settings_manager = SettingsManager()
        self.llm_manager = LLMManager(self.settings_manager)
        self.code_executor = CodeExecutor()
        self.prompt_engine = PromptEngine()

        self.form = QtWidgets.QWidget()
        self.form.setObjectName("AIPromptTaskPanel") # Important for FreeCAD to identify it
        layout = QtWidgets.QVBoxLayout(self.form)

        # LLM Selector
        llm_layout = QtWidgets.QHBoxLayout()
        llm_layout.addWidget(QtWidgets.QLabel("Select LLM:"))
        self.llm_combo = QtWidgets.QComboBox()
        # Populate with available LLMs (add more as you implement them in LLMManager)
        self.llm_combo.addItems(["MockLLM (Test)", "Gemini Pro (Placeholder)", "OpenAI GPT-4o (Placeholder)", "Ollama (Placeholder)"])
        llm_layout.addWidget(self.llm_combo)
        layout.addLayout(llm_layout)
        
        # API Key Status (Simple Label)
        self.api_key_status_label = QtWidgets.QLabel("API Key Status: Unknown")
        self.llm_combo.currentIndexChanged.connect(self.update_api_key_status) # Update status on change
        layout.addWidget(self.api_key_status_label)
        self.update_api_key_status() # Initial check

        # Prompt Input
        layout.addWidget(QtWidgets.QLabel("Enter your prompt:"))
        self.prompt_input = QtWidgets.QTextEdit()
        self.prompt_input.setPlaceholderText("e.g., Create a 10mm cube named 'MyCube'")
        self.prompt_input.setMinimumHeight(100)
        layout.addWidget(self.prompt_input)

        # Submit Button
        self.submit_button = QtWidgets.QPushButton("Submit Prompt")
        self.submit_button.clicked.connect(self.on_submit_prompt)
        layout.addWidget(self.submit_button)

        # Generated Code Area
        layout.addWidget(QtWidgets.QLabel("Generated Code (Review Carefully!):"))
        self.code_output = QtWidgets.QTextEdit()
        self.code_output.setReadOnly(True)
        self.code_output.setFontFamily("monospace") # Good for code
        self.code_output.setMinimumHeight(150)
        layout.addWidget(self.code_output)

        # Execute Code Button
        self.execute_button = QtWidgets.QPushButton("Execute Code")
        self.execute_button.clicked.connect(self.on_execute_code)
        self.execute_button.setEnabled(False) # Disabled until code is generated
        layout.addWidget(self.execute_button)

        # Log/Status Area
        layout.addWidget(QtWidgets.QLabel("Log/Status:"))
        self.log_output = QtWidgets.QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMinimumHeight(80)
        layout.addWidget(self.log_output)
        
        # Clear Button
        self.clear_button = QtWidgets.QPushButton("Clear All")
        self.clear_button.clicked.connect(self.on_clear_all)
        layout.addWidget(self.clear_button)


    def update_api_key_status(self):
        selected_llm_id = self.llm_combo.currentText().split(" ")[0].lower() # e.g. "mockllm"
        if selected_llm_id == "mockllm":
            self.api_key_status_label.setText("API Key Status: N/A for MockLLM")
            return

        # For real LLMs, you'd check if the key is set in SettingsManager
        # This is a simplified check, expand in SettingsManager
        api_key = self.settings_manager.get_api_key(selected_llm_id)
        if api_key and api_key != "YOUR_API_KEY_HERE": # Check if it's not the placeholder
            self.api_key_status_label.setText(f"API Key Status: Set for {selected_llm_id}")
            self.api_key_status_label.setStyleSheet("color: green;")
        else:
            self.api_key_status_label.setText(f"API Key Status: NOT SET for {selected_llm_id} (Configure in Preferences)")
            self.api_key_status_label.setStyleSheet("color: red;")


    def on_submit_prompt(self):
        user_prompt = self.prompt_input.toPlainText()
        if not user_prompt:
            self.log_output.append("Please enter a prompt.")
            return

        selected_llm_text = self.llm_combo.currentText()
        # Extract a simple ID, e.g., "MockLLM (Test)" -> "mockllm"
        llm_id = selected_llm_text.split(" ")[0].lower()


        self.log_output.append(f"Sending prompt to {selected_llm_text}...")
        self.code_output.clear()
        self.execute_button.setEnabled(False)
        QtWidgets.QApplication.processEvents() # Update UI

        # Get system prompt
        system_prompt = self.prompt_engine.get_system_prompt(llm_id)
        
        # For real LLMs, you would get the API key from settings_manager
        # api_key = self.settings_manager.get_api_key(llm_id)
        # if not api_key and llm_id != "mockllm":
        #     self.log_output.append(f"Error: API Key for {llm_id} not set. Configure in Preferences.")
        #     return

        try:
            # The LLMManager will handle specifics for each LLM type
            generated_code = self.llm_manager.send_prompt(llm_id, user_prompt, system_prompt)
            
            if generated_code and not generated_code.startswith("Error:"):
                self.code_output.setPlainText(generated_code)
                self.log_output.append("Code received. Review carefully before execution.")
                self.execute_button.setEnabled(True)
            else:
                self.log_output.append(f"Failed to get code: {generated_code}")

        except Exception as e:
            self.log_output.append(f"Error during LLM communication: {str(e)}")
            FreeCAD.Console.PrintError(f"LLM Error: {str(e)}\n")


    def on_execute_code(self):
        script_to_execute = self.code_output.toPlainText()
        if not script_to_execute:
            self.log_output.append("No code to execute.")
            return

        # Critical Safety Warning
        reply = QtWidgets.QMessageBox.warning(self.form, "Security Warning",
                                           "You are about to execute Python code generated by an AI. "
                                           "This code could potentially perform unintended or harmful actions "
                                           "if not reviewed carefully.\n\n"
                                           "ARE YOU SURE YOU WANT TO EXECUTE THIS CODE?\n\n"
                                           f"Code:\n------\n{script_to_execute[:500]}...\n------", # Show first 500 chars
                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                           QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            self.log_output.append("Executing code...")
            QtWidgets.QApplication.processEvents() # Update UI
            
            success, log_msg = self.code_executor.execute_script(script_to_execute)
            self.log_output.append(log_msg)
            if success:
                self.log_output.append("Code execution finished.")
            else:
                self.log_output.append("Code execution failed or had errors.")
        else:
            self.log_output.append("Code execution cancelled by user.")

    def on_clear_all(self):
        self.prompt_input.clear()
        self.code_output.clear()
        self.log_output.clear()
        self.execute_button.setEnabled(False)
        self.log_output.append("Cleared all fields.")

    def getForm(self): # This is what FreeCAD's TaskPanel system expects
        return self.form

    # FreeCAD TaskPanel Lifecycle Methods (Optional but good practice)
    def accept(self): # Called when OK or Apply is clicked (if those buttons were added)
        FreeCAD.Console.PrintMessage("AIPromptTaskPanel: Accept called\n")
        return True

    def reject(self): # Called when Cancel is clicked
        FreeCAD.Console.PrintMessage("AIPromptTaskPanel: Reject called\n")
        # self.destroy() # Clean up if necessary
        return True

    def clicked(self, clb): # Called for checkbox clicks (if any)
        FreeCAD.Console.PrintMessage(f"AIPromptTaskPanel: Clicked {clb}\n")

    def open(self): # Called when the panel is opened
        FreeCAD.Console.PrintMessage("AIPromptTaskPanel: Open called\n")

    def needsReportButton(self): # Whether to show the "Report view" button
        return False

    def helpRequested(self): # Called for F1 key / Help button
        FreeCAD.Console.PrintMessage("AIPromptTaskPanel: Help requested\n")
        # QtWidgets.QDesktopServices.openUrl(QtCore.QUrl("http://your-plugin-docs.com/help"))

    # def destroy(self):
    #     FreeCAD.Console.PrintMessage("AIPromptTaskPanel: Destroy called\n")
    #     # Any cleanup