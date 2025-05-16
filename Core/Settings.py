import FreeCAD

class SettingsManager:
    def __init__(self):
        self.param = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/AICAD")

    def get_api_key(self, llm_id):
        """Get API key for specified LLM"""
        key = self.param.GetString(f"APIKey_{llm_id}", "")
        return key if key else "YOUR_API_KEY_HERE"

    def set_api_key(self, llm_id, key):
        """Store API key for specified LLM"""
        self.param.SetString(f"APIKey_{llm_id}", key)

    def get_setting(self, key, default=""):
        """Get generic setting value"""
        return self.param.GetString(key, default)

    def set_setting(self, key, value):
        """Store generic setting value"""
        self.param.SetString(key, value)
