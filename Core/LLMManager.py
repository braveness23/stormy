# AIFreeCADWorkbench/Core/LLMManager.py
import FreeCAD
import requests
import json
from .constants import LLM_CONFIGS, API_ENDPOINTS

class LLMManager:
    def __init__(self, settings_manager):
        self.settings_manager = settings_manager

    def _extract_code_from_response(self, response_text, llm_id="unknown"):
        """
        Attempts to extract Python code from LLM's markdown response.
        Looks for ```python ... ``` or just ``` ... ``` blocks.
        """
        if "```python" in response_text:
            code = response_text.split("```python")[1].split("```")[0].strip()
            return code
        elif "```" in response_text:
            code = response_text.split("```")[1].split("```")[0].strip()
            # If it's just a simple statement, it might not have 'python' tag
            # but could still be Python code.
            if "\n" in code or code.startswith("import ") or code.startswith("App.") or code.startswith("Part."):
                 return code
            return f"Error: Found a code block for {llm_id} but it might not be Python."
        return response_text # Assume the whole response is code if no backticks

    def _make_api_request(self, llm_id, endpoint, headers, data):
        """Make API request with proper error handling and timeout"""
        timeout = LLM_CONFIGS[llm_id]['timeout']
        try:
            response = requests.post(endpoint, headers=headers, json=data, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.Timeout:
            raise TimeoutError(f"Request to {llm_id} timed out after {timeout} seconds")
        except requests.RequestException as e:
            raise ConnectionError(f"API request failed: {str(e)}")

    def _handle_openai(self, llm_id, system_prompt, user_prompt):
        api_key = self.settings_manager.get_api_key(llm_id)
        model = self.settings_manager.get_setting("OpenAIModel", "gpt-4")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }
        
        response = self._make_api_request(
            llm_id, 
            API_ENDPOINTS['openai'],
            headers,
            data
        )
        return response['choices'][0]['message']['content']

    def _handle_gemini(self, llm_id, system_prompt, user_prompt):
        api_key = self.settings_manager.get_api_key(llm_id)
        model = self.settings_manager.get_setting("GeminiModel", "gemini-pro")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "system": system_prompt,
            "prompt": user_prompt
        }
        
        response = self._make_api_request(
            llm_id, 
            API_ENDPOINTS['gemini'],
            headers,
            data
        )
        return response['response']

    def _handle_ollama(self, llm_id, system_prompt, user_prompt):
        base_url = self.settings_manager.get_setting("OllamaBaseURL", "http://localhost:11434")
        model_name = self.settings_manager.get_setting("OllamaModelName", "llama3")
        
        data = {
            "model": model_name,
            "system": system_prompt,
            "prompt": user_prompt,
            "stream": False
        }
        
        response = self._make_api_request(
            llm_id, 
            f"{base_url}/api/generate",
            {},
            data
        )
        return response.get("response", "")

    def send_prompt(self, llm_id, user_prompt, system_prompt):
        """Main method to send prompts to various LLMs"""
        try:
            if llm_id == "mockllm":
                # Simulate a delay and return a fixed script
                FreeCAD.Console.PrintMessage("MockLLM generating response...\n")
                if "sphere" in user_prompt.lower():
                    return """import Part
import FreeCAD as App

doc = App.ActiveDocument
if not doc:
    doc = App.newDocument("MockDoc")

sphere = Part.makeSphere(10)
sphere.Label = "MockSphere"
Part.show(sphere)
doc.recompute()
App.ActiveDocument.ActiveView.viewAxometric()
Gui.SendMsgToActiveView("ViewFit")
"""
                else: # Default to a cube
                    return """import Part
import FreeCAD as App

doc = App.ActiveDocument
if not doc:
    doc = App.newDocument("MockDoc")

cube = Part.makeBox(15, 20, 25) # Length, Width, Height
cube.Label = "MockCube"
Part.show(cube)
doc.recompute()
App.ActiveDocument.ActiveView.viewTop()
Gui.SendMsgToActiveView("ViewFit")
"""

            config = LLM_CONFIGS.get(llm_id)
            if not config:
                return f"Error: Unknown LLM ID '{llm_id}'"

            if config['type'] == 'openai':
                response = self._handle_openai(llm_id, system_prompt, user_prompt)
            elif config['type'] == 'gemini':
                response = self._handle_gemini(llm_id, system_prompt, user_prompt)
            elif config['type'] == 'ollama':
                response = self._handle_ollama(llm_id, system_prompt, user_prompt)
            else:
                return f"Error: Unsupported LLM type '{config['type']}'"

            return self._extract_code_from_response(response, llm_id)

        except Exception as e:
            FreeCAD.Console.PrintError(f"LLM Error ({llm_id}): {str(e)}\n")
            return f"Error: {str(e)}"