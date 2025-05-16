import FreeCAD
import base64
from .constants import DEFAULT_SYSTEM_PROMPTS, ALLOWED_MODULES

class SettingsManager:
    """Manages settings and configuration for the AI-CAD Workbench."""

    def __init__(self):
        """Initialize settings manager with FreeCAD parameter group."""
        self.param = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/AICAD")

    def _encode_api_key(self, key):
        """Basic obfuscation of API keys (not true encryption)."""
        return base64.b64encode(key.encode()).decode()

    def _decode_api_key(self, encoded_key):
        """Decode obfuscated API key."""
        try:
            return base64.b64decode(encoded_key.encode()).decode()
        except:
            return "YOUR_API_KEY_HERE"

    def get_api_key(self, llm_id):
        """Get API key for specified LLM with basic obfuscation."""
        encoded_key = self.param.GetString(f"APIKey_{llm_id}", "")
        return self._decode_api_key(encoded_key) if encoded_key else "YOUR_API_KEY_HERE"

    def set_api_key(self, llm_id, key):
        """Store API key with basic obfuscation."""
        if key and key != "YOUR_API_KEY_HERE":
            encoded_key = self._encode_api_key(key)
            self.param.SetString(f"APIKey_{llm_id}", encoded_key)

    def get_system_prompt(self, llm_id):
        """Get system prompt for specified LLM, with fallback to default."""
        custom_prompt = self.param.GetString(f"SystemPrompt_{llm_id}", "")
        if custom_prompt:
            return custom_prompt
        
        # Get default prompt and format with current allowed modules
        default_prompt = DEFAULT_SYSTEM_PROMPTS.get(
            llm_id, 
            DEFAULT_SYSTEM_PROMPTS['default']
        )
        return default_prompt.format(allowed_modules=", ".join(sorted(ALLOWED_MODULES)))

    def set_system_prompt(self, llm_id, prompt):
        """Store custom system prompt for an LLM."""
        self.param.SetString(f"SystemPrompt_{llm_id}", prompt)

    def get_setting(self, key, default=""):
        """Get generic setting value"""
        return self.param.GetString(key, default)

    def set_setting(self, key, value):
        """Store generic setting value"""
        self.param.SetString(key, value)
