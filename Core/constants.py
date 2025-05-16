"""Constants and configuration for the AI-CAD Workbench."""

# Timeout in seconds for script execution
SCRIPT_EXECUTION_TIMEOUT = 30

# Allowed FreeCAD modules for sandboxing
ALLOWED_MODULES = {
    'FreeCAD', 'Part', 'Draft', 'Sketcher', 'math',
    'Mesh', 'Points', 'MeshPart', 'Drawing', 'Arch'
}

# Dangerous Python built-ins to block
BLOCKED_BUILTINS = {
    'eval', 'exec', 'compile', '__import__',
    'open', 'file', 'input', 'raw_input'
}

# Error Messages
ERRORS = {
    'api_key_missing': "Error: {0} API Key not configured in Preferences.",
    'execution_timeout': "Error: Script execution timed out after {0} seconds.",
    'invalid_module': "Error: Attempt to use unauthorized module: {0}",
    'invalid_builtin': "Error: Attempt to use blocked function: {0}",
    'script_validation': "Error: Script validation failed: {0}",
}

# Default system prompts by LLM
DEFAULT_SYSTEM_PROMPTS = {
    'default': """You are a CAD assistant specialized in FreeCAD's Python API.
Generate only valid Python code that creates 3D models using FreeCAD's API.
Your code should:
- Use proper error handling
- Follow FreeCAD best practices
- Be well-commented
- Be concise but clear
- Handle document creation/activation
- Include view operations when appropriate
- Only use these allowed modules: {allowed_modules}""",
    
    'mockllm': """You are a CAD assistant specialized in FreeCAD's Python API.
This is a test environment.
Generate only valid Python code that creates 3D models using FreeCAD's API.""",
}

# LLM Configuration
LLM_CONFIGS = {
    'openai_gpt-4o': {
        'name': 'OpenAI GPT-4',
        'type': 'openai',
        'default_model': 'gpt-4',
        'timeout': 60,
    },
    'gemini_pro': {
        'name': 'Google Gemini Pro',
        'type': 'gemini',
        'default_model': 'gemini-pro',
        'timeout': 30,
    },
    'ollama': {
        'name': 'Ollama (Local)',
        'type': 'ollama',
        'default_model': 'llama2',
        'timeout': 30,
    },
    'mockllm': {
        'name': 'Mock LLM (Test)',
        'type': 'mock',
        'timeout': 1,
    }
}

# API Endpoints
API_ENDPOINTS = {
    'openai': 'https://api.openai.com/v1/chat/completions',
    'gemini': 'https://generativelanguage.googleapis.com/v1/models/{model}:generateContent',
    'ollama': '{base_url}/api/generate',
}
