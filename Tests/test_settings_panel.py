import unittest
from unittest.mock import MagicMock, patch, Mock
import requests
from PySide2.QtWidgets import QApplication
import sys

# Create QApplication instance for widget tests
app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

# Mock FreeCAD and related modules
mock_freecad = MagicMock()
mock_gui = MagicMock()
mock_param = MagicMock()

# Set up module-level mocks
sys.modules['FreeCAD'] = mock_freecad
sys.modules['FreeCADGui'] = mock_gui

# Now we can import our module
from stormy.Core.SettingsPanel import SettingsPanelWidget
from stormy.Core.Settings import SettingsManager

class TestSettingsPanel(unittest.TestCase):
    def setUp(self):
        # Reset mocks before each test
        mock_freecad.reset_mock()
        mock_gui.reset_mock()
        mock_param.reset_mock()
        
        # Set up mock parameter group
        mock_freecad.ParamGet.return_value = mock_param
        
        self.panel = SettingsPanelWidget()
        
    def tearDown(self):
        pass
        
    @patch('requests.get')
    def test_openai_connection_test(self, mock_get):
        """Test OpenAI API connection test"""
        mock_get.return_value = Mock(status_code=200)
        
        success = self.panel._test_specific_api("openai_gpt-4o", "fake_key")
        self.assertTrue(success)
        
        mock_get.assert_called_once_with(
            'https://api.openai.com/v1/models',
            headers={'Authorization': 'Bearer fake_key'},
            timeout=5
        )
        
    @patch('requests.get')
    def test_failed_connection(self, mock_get):
        """Test failed API connection"""
        mock_get.side_effect = requests.RequestException("Connection failed")
        
        success = self.panel._test_specific_api("openai_gpt-4o", "fake_key")
        self.assertFalse(success)
        
        mock_get.assert_called_once()
        
    def test_invalid_api_type(self):
        """Test invalid API type handling"""
        with self.assertRaises(ValueError):
            self.panel._test_specific_api("invalid_api", "fake_key")
            
    def test_save_settings(self):
        """Test settings save functionality"""
        # Mock input field with test value
        test_key = "test_api_key"
        mock_field = MagicMock()
        mock_field.text.return_value = test_key
        
        self.panel.widgets_to_save.append({
            "widget": mock_field,
            "type": "api_key",
            "id": "openai_gpt-4o"
        })
        
        self.panel.save()
        mock_param.SetString.assert_called_with("APIKey_openai_gpt-4o", test_key)

if __name__ == '__main__':
    unittest.main()
