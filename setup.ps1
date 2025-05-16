# Check if Python is installed
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not installed or not in PATH"
    exit 1
}

# Create virtual environment
Write-Host "Creating virtual environment..."
python -m venv .venv

# Activate virtual environment
Write-Host "Activating virtual environment..."
.\.venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
Write-Host "Installing requirements..."
pip install -r Core\requirements.txt

Write-Host "Setup complete! Virtual environment is active."
Write-Host "To activate the environment later, run: .\.venv\Scripts\Activate.ps1"
