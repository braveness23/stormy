# stormy

## Development

### Running Tests

1. First, activate the virtual environment:

   ```bash
   # On Windows
   .\.venv\Scripts\Activate.ps1
   
   # On Linux/Mac
   source .venv/bin/activate
   ```

2. Make sure test dependencies are installed:

   ```bash
   pip install -r Core/requirements.txt
   ```

3. Run the tests:

   ```bash
   # Run all tests
   python run_tests.py
   
   # Run with coverage report
   coverage run run_tests.py && coverage report
   
   # Run specific test file
   python run_tests.py Tests/test_settings_panel.py
   
   # Run tests matching a pattern
   python run_tests.py -k "test_openai"
   ```
