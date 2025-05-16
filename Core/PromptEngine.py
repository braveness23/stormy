# AIFreeCADWorkbench/Core/SettingsPanel.py
import os
import FreeCAD # For console messages, not strictly for GUI
from PySide2 import QtWidgets # Or PySide6 if your FreeCAD uses Qt6
from .Settings import SettingsManager # Import the manager

# Path to icons for this preference page (optional)
# workbench_mod_path = os.path.dirname(os.path.dirname(__file__)) # Up to AIFreeCADWorkbench/
# icon_path = os.path.join(workbench_mod_path, "Resources", "Icons")


class SettingsPanelWidget:
    def __init__(self):
        self.settings_manager = SettingsManager()
        
        self.form = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout()
        self.form.setLayout(layout)

        self.widgets_to_save = [] # To store widgets and their mapping for saving

        # --- OpenAI API Key ---
        layout.addRow(QtWidgets.QLabel("<b>OpenAI (e.g., GPT-4o)</b>"))
        self.openai_key_edit = self._add_api_key_input(layout, "API Key:", "openai_gpt-4o")
        
        # --- Google Gemini API Key ---
        layout.addRow(QtWidgets.QLabel("<b>Google Gemini (e.g., Gemini Pro)</b>"))
        self.gemini_key_edit = self._add_api_key_input(layout, "API Key:", "gemini_pro")

        # --- Ollama Settings ---
        layout.addRow(QtWidgets.QLabel("<b>Ollama (Local LLMs)</b>"))
        self.ollama_url_edit = self._add_generic_setting_input(layout, "Ollama Server URL:", "OllamaBaseURL", "http://localhost:11434")
        self.ollama_model_edit = self._add_generic_setting_input(layout, "Default Ollama Model:", "OllamaDefaultModel", "llama3")
        
        # Add a spacer or stretch at the end if layout is too sparse
        layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))


    def _add_api_key_input(self, layout, label_text, llm_id_for_key):
        edit = QtWidgets.QLineEdit()
        current_key = self.settings_manager.get_api_key(llm_id_for_key)
        
        if current_key and current_key != "YOUR_API_KEY_HERE":
             edit.setText(current_key)
        else:
            edit.setPlaceholderText("Enter your API key here")
        
        # For API keys, you might want to use setEchoMode if it's sensitive data,
        # but for copy-paste, normal mode is better.
        # edit.setEchoMode(QtWidgets.QLineEdit.Password) 
        
        layout.addRow(QtWidgets.QLabel(label_text), edit)
        self.widgets_to_save.append({"widget": edit, "type": "api_key", "id": llm_id_for_key})
        return edit

    def _add_generic_setting_input(self, layout, label_text, setting_key, default_value):
        edit = QtWidgets.QLineEdit()
        current_value = self.settings_manager.get_setting(setting_key, default_value)
        edit.setText(current_value)
        edit.setPlaceholderText(f"e.g., {default_value}")
        
        layout.addRow(QtWidgets.QLabel(label_text), edit)
        self.widgets_to_save.append({"widget": edit, "type": "generic_setting", "key": setting_key})
        return edit

    def save(self):
        """Called when user clicks OK or Apply in Preferences"""
        for item in self.widgets_to_save:
            widget = item["widget"]
            if item["type"] == "api_key":
                self.settings_manager.set_api_key(item["id"], widget.text().strip())
            elif item["type"] == "generic_setting":
                self.settings_manager.set_setting(item["key"], widget.text().strip())
        FreeCAD.Console.PrintMessage("AI-CAD Workbench settings saved.\n")
        return True

    def load(self):
        """Called when Preference page is opened"""
        # Values are loaded during widget initialization, so this can often be pass.
        # If you need to refresh values (e.g. if settings could change elsewhere), do it here.
        for item in self.widgets_to_save:
            widget = item["widget"]
            if item["type"] == "api_key":
                current_key = self.settings_manager.get_api_key(item["id"])
                if current_key and current_key != "YOUR_API_KEY_HERE":
                    widget.setText(current_key)
                else:
                    widget.setText("") # Clear if it's the placeholder
                    widget.setPlaceholderText("Enter your API key here")
            elif item["type"] == "generic_setting":
                default_value_for_placeholder = widget.placeholderText().replace("e.g., ", "") # Bit hacky
                current_value = self.settings_manager.get_setting(item["key"], default_value_for_placeholder)
                widget.setText(current_value)
        return True


    def getName(self):
        return "AI-CAD Workbench" # Name for the preferences page section

    def getIcon(self):
        # You can return a path to an icon file here or a standard FreeCAD icon name
        # icon_file = os.path.join(icon_path, "AIConfigure.svg")
        # if os.path.exists(icon_file):
        #    return icon_file
        return "Std_DlgPreferences" # A generic preferences icon from FreeCAD

    # Required by FreeCAD's preference page system
    def getWidget(self):
        return self.form


class PromptEngine:
    """Manages prompt generation and processing for AI interactions."""
    
    def __init__(self):
        self.settings_manager = SettingsManager()

    def get_system_prompt(self, llm_id):
        """Returns the appropriate system prompt based on LLM type."""
        return self.settings_manager.get_system_prompt(llm_id)