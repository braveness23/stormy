import os
import FreeCAD
from PySide2 import QtWidgets
from .Settings import SettingsManager

class SettingsPanelWidget:
    """Settings panel for the AI-CAD Workbench."""
    def __init__(self):
        self.settings_manager = SettingsManager()
        
        self.form = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout()
        self.form.setLayout(layout)

        self.widgets_to_save = []
        self.status_labels = {}  # Store status labels

        # --- OpenAI API Key ---
        layout.addRow(QtWidgets.QLabel("<b>OpenAI Settings</b>"))
        key_layout = self._add_api_key_input(layout, "API Key:", "openai_gpt-4o", 
            "Enter your OpenAI API key.")
        self._add_test_button(key_layout, "openai_gpt-4o")
        self._add_generic_setting_input(layout, "Model:", "OpenAIModel", "gpt-4",
            "Select OpenAI model (e.g. gpt-4, gpt-3.5-turbo)")
        
        # --- Google Gemini API Key ---
        layout.addRow(QtWidgets.QLabel("<b>Google Gemini Settings</b>"))
        key_layout = self._add_api_key_input(layout, "API Key:", "gemini_pro", 
            "Enter your Google Gemini API key.")
        self._add_test_button(key_layout, "gemini_pro")
        self._add_generic_setting_input(layout, "Model:", "GeminiModel", "gemini-pro",
            "Select Google Gemini model (e.g. gemini-pro, gemini-lite)")

        # --- Ollama Settings ---
        layout.addRow(QtWidgets.QLabel("<b>Ollama Settings</b>"))
        key_layout = self._add_generic_setting_input(layout, "Server URL:", "OllamaBaseURL", "http://localhost:11434",
            "Enter the base URL for Ollama server.")
        self._add_generic_setting_input(layout, "Model:", "OllamaModel", "llama2",
            "Select Ollama model (e.g. llama2, llama1)")

        # Add a spacer at the end
        layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

    def _add_api_key_input(self, layout, label, setting_key, tooltip=""):
        """Helper to add API key input fields."""
        row_layout = QtWidgets.QHBoxLayout()
        
        input_field = QtWidgets.QLineEdit()
        input_field.setToolTip(tooltip)
        
        # Get key directly from settings
        current_key = self.settings_manager.get_setting(setting_key)
        if current_key:
            input_field.setText(current_key)
        
        status_label = QtWidgets.QLabel()
        status_label.setFixedWidth(20)
        self.status_labels[setting_key] = status_label
        
        row_layout.addWidget(input_field)
        row_layout.addWidget(status_label)
        
        layout.addRow(QtWidgets.QLabel(label), row_layout)
        self.widgets_to_save.append((setting_key, input_field, "generic"))
        
        return row_layout

    def _add_generic_setting_input(self, layout, label, setting_key, default_value, tooltip=""):
        """Helper to add generic input fields."""
        input_field = QtWidgets.QLineEdit()
        input_field.setText(self.settings_manager.get_setting(setting_key, default_value))
        input_field.setToolTip(tooltip)
        layout.addRow(QtWidgets.QLabel(label), input_field)
        self.widgets_to_save.append((setting_key, input_field, "generic"))

    def _add_test_button(self, layout, api_key_id):
        """Add a test connection button."""
        test_btn = QtWidgets.QPushButton("Test")
        test_btn.setFixedWidth(60)
        test_btn.clicked.connect(lambda: self._test_api_connection(api_key_id))
        layout.addWidget(test_btn)

    def _test_api_connection(self, api_key_id):
        """Test API connection and update status indicator."""
        try:
            # Get the current input value
            for key, field, type_ in self.widgets_to_save:
                if key == api_key_id and type_ == "generic":
                    api_key = field.text()
                    break
            
            if not api_key:
                self._update_status(api_key_id, False, "No API key provided")
                return

            # Test connection based on API type
            success = self._test_specific_api(api_key_id, api_key)
            self._update_status(api_key_id, success)
            
        except Exception as e:
            self._update_status(api_key_id, False, str(e))

    def _update_status(self, api_key_id, success, tooltip=""):
        """Update the status indicator."""
        status_label = self.status_labels.get(api_key_id)
        if status_label:
            status_label.setText("✓" if success else "✗")
            status_label.setStyleSheet(
                f"color: {'green' if success else 'red'};"
                f"font-weight: bold;"
            )
            if tooltip:
                status_label.setToolTip(tooltip)

    def _test_specific_api(self, api_key_id, api_key):
        """Test connection with specific LLM API."""
        import requests
        from .constants import LLM_CONFIGS, API_ENDPOINTS
        
        config = LLM_CONFIGS.get(api_key_id)
        if not config:
            raise ValueError(f"Unknown API type: {api_key_id}")
            
        try:
            # Add connection test result tracking for unit tests
            self._last_test_result = False
            
            if config['type'] == 'openai':
                response = requests.get(
                    'https://api.openai.com/v1/models',
                    headers={'Authorization': f'Bearer {api_key}'},
                    timeout=5
                )
                self._last_test_result = response.status_code == 200
                return self._last_test_result
                
            elif config['type'] == 'gemini':
                # Google requires API key in URL
                model = self.settings_manager.get_setting("GeminiModel", "gemini-pro")
                url = API_ENDPOINTS['gemini'].format(model=model)
                response = requests.get(
                    f"{url}?key={api_key}",
                    timeout=5
                )
                self._last_test_result = response.status_code == 200
                return self._last_test_result
                
            elif config['type'] == 'ollama':
                base_url = self.settings_manager.get_setting("OllamaBaseURL", "http://localhost:11434")
                response = requests.get(
                    f"{base_url}/api/tags",
                    timeout=5
                )
                self._last_test_result = response.status_code == 200
                return self._last_test_result
                
            else:
                self._last_test_result = True  # For mock LLM, always return success
                return self._last_test_result
                
        except requests.RequestException as e:
            FreeCAD.Console.PrintError(f"API test failed: {str(e)}\n")
            self._last_test_result = False
            return False

    # Add helper methods for testing
    def get_last_test_result(self):
        """Get the result of the last API test (for unit testing)"""
        return getattr(self, '_last_test_result', None)
        
    def get_input_field(self, setting_key):
        """Get an input field by setting key (for unit testing)"""
        for key, field, _ in self.widgets_to_save:
            if key == setting_key:
                return field
        return None

    def save_settings(self):
        """Save all settings directly."""
        for setting_key, input_field, _ in self.widgets_to_save:
            value = input_field.text()
            if value:  # Only store if value is provided
                self.settings_manager.set_setting(setting_key, value)
        
        FreeCAD.Console.PrintMessage("Settings saved successfully\n")
