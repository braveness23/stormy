import os
import sys
import subprocess
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_dev_environment():
    """Configure development environment for FreeCAD addon development"""
    try:
        # Set development mode
        os.environ['FREECAD_DEV_MODE'] = '1'
        
        # Install development dependencies
        logger.info("Installing development dependencies...")
        pip_install_deps()
        
        # Create VSCode settings
        logger.info("Configuring VSCode settings...")
        create_vscode_settings()
        
        logger.info("Development environment setup complete!")
        
    except Exception as e:
        logger.error(f"Setup failed: {str(e)}")
        raise

def pip_install_deps():
    """Install Python development dependencies"""
    try:
        subprocess.check_call([
            sys.executable,
            "-m", 
            "pip",
            "install",
            "-r",
            "requirements.txt"
        ])
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to install dependencies: {str(e)}")

def create_vscode_settings():
    """Create or update VSCode settings"""
    settings_dir = ".vscode"
    settings_file = os.path.join(settings_dir, "settings.json")
    
    vscode_settings = {
        "python.pythonPath": sys.executable,
        "python.linting.enabled": True,
        "python.linting.pylintEnabled": True,
        "python.formatting.provider": "black",
        "python.testing.pytestEnabled": True,
        "editor.formatOnSave": True
    }
    
    os.makedirs(settings_dir, exist_ok=True)
    
    with open(settings_file, "w") as f:
        json.dump(vscode_settings, f, indent=4)

if __name__ == "__main__":
    setup_dev_environment()
