# AIFreeCADWorkbench/Core/LLMManager.py
import FreeCAD
# For real LLMs, you would import their respective libraries
# import openai
# import google.generativeai as genai
# import requests # For Ollama or custom APIs
# import json

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


    def send_prompt(self, llm_id, user_prompt, system_prompt):
        FreeCAD.Console.PrintMessage(f"LLMManager: Sending to {llm_id}. System Prompt: {system_prompt[:100]}...\nUser Prompt: {user_prompt}\n")
        
        api_key = self.settings_manager.get_api_key(llm_id) # Fetches from FreeCAD params

        if llm_id == "mockllm":
            # Simulate a delay and return a fixed script
            # import time
            # time.sleep(1) # Simulate network delay
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

        elif llm_id == "gemini pro" or llm_id == "gemini-pro": # Example using gemini-pro
            # Placeholder - Implement actual Google Gemini API call here
            # try:
            #     if not api_key or api_key == "YOUR_API_KEY_HERE":
            #         return "Error: Gemini API Key not configured in Preferences."
            #     genai.configure(api_key=api_key)
            #     model = genai.GenerativeModel('gemini-pro')
            #     full_prompt = f"{system_prompt}\n\nUser Request:\n{user_prompt}"
            #     response = model.generate_content(full_prompt)
            #     return self._extract_code_from_response(response.text, "gemini")
            # except Exception as e:
            #     FreeCAD.Console.PrintError(f"Gemini API Error: {str(e)}\n")
            #     return f"Error: Gemini API call failed: {str(e)}"
            return "Error: Gemini Pro (Placeholder) not fully implemented yet."

        elif llm_id == "openai gpt-4o" or llm_id == "openai-gpt-4o":
            # Placeholder - Implement actual OpenAI API call here
            # try:
            #     if not api_key or api_key == "YOUR_API_KEY_HERE":
            #         return "Error: OpenAI API Key not configured in Preferences."
            #     client = openai.OpenAI(api_key=api_key)
            #     completion = client.chat.completions.create(
            #         model="gpt-4o", # Or your preferred model
            #         messages=[
            #             {"role": "system", "content": system_prompt},
            #             {"role": "user", "content": user_prompt}
            #         ]
            #     )
            #     return self._extract_code_from_response(completion.choices[0].message.content, "openai")
            # except Exception as e:
            #     FreeCAD.Console.PrintError(f"OpenAI API Error: {str(e)}\n")
            #     return f"Error: OpenAI API call failed: {str(e)}"
            return "Error: OpenAI GPT-4o (Placeholder) not fully implemented yet."

        elif llm_id == "ollama":
            # Placeholder - Implement Ollama call
            # base_url = self.settings_manager.get_setting("ollama_base_url", "http://localhost:11434")
            # model_name = self.settings_manager.get_setting("ollama_model_name", "llama3") # Default model
            # try:
            #     response = requests.post(
            #         f"{base_url}/api/generate",
            #         json={
            #             "model": model_name,
            #             "system": system_prompt,
            #             "prompt": user_prompt,
            #             "stream": False # For simpler handling initially
            #         },
            #         timeout=60 # seconds
            #     )
            #     response.raise_for_status() # Check for HTTP errors
            #     return self._extract_code_from_response(response.json().get("response", ""), "ollama")
            # except requests.RequestException as e:
            #     FreeCAD.Console.PrintError(f"Ollama API Error: {str(e)}\n")
            #     return f"Error connecting to Ollama ({base_url}): {e}"
            # except Exception as e:
            #     FreeCAD.Console.PrintError(f"Ollama processing Error: {str(e)}\n")
            #     return f"Error processing Ollama response: {e}"
            return "Error: Ollama (Placeholder) not fully implemented yet."
            
        else:
            return f"Error: LLM ID '{llm_id}' not recognized or implemented."