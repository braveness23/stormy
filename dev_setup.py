import os
import sys
import subprocess

def setup_dev_environment():
    """Configure development environment for FreeCAD addon development"""
    
    # Set development mode
    os.environ['FREECAD_DEV_MODE'] = '1'
    
    # Install development dependencies
    subprocess.check_call([
        sys.executable,
        "-m", 
        "pip",
        "install",
        "pytest",
        "pylint",
        "black"
    ])
    
    # Create VSCode settings if needed
    vscode_settings = {
        "python.pythonPath": sys.executable,
        "python.linting.enabled": True,
        "python.linting.pylintEnabled": True,
        "python.formatting.provider": "black"
    }
    
    os.makedirs(".vscode", exist_ok=True)
    with open(".vscode/settings.json", "w") as f:
        import json
        json.dump(vscode_settings, f, indent=4)

if __name__ == "__main__":
    setup_dev_environment()
