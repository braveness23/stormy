# AIFreeCADWorkbench/InitGui.py
import FreeCAD
import FreeCADGui
import os
from PySide2 import QtGui # PySide2 for Qt5, common in many FreeCAD versions

# Path to icons (assuming they are in Resources/Icons/ within the Mod directory)
workbench_path = os.path.dirname(__file__)
icon_path = os.path.join(workbench_path, "Resources", "Icons")

class AIWorkbench(FreeCADGui.Workbench):
    """
    AI CAD Workbench class
    """
    MenuText = "AI-CAD Workbench"
    ToolTip = "A workbench for interacting with LLMs to generate FreeCAD scripts."
    Icon = os.path.join(icon_path, "AIWorkbench.svg") # Path to your workbench icon

    def Initialize(self):
        """This function is called during FreeCAD initialization"""
        import AIWorkbench as MainModule # Main logic module for the workbench
        self.main_module = MainModule

        self.open_panel_cmd = OpenAIPanelCommand()
        self.configure_cmd = ConfigureLLMsCommand()

        self.appendToolbar("AI Commands", [self.open_panel_cmd.name])
        self.appendMenu("AI-CAD", [self.open_panel_cmd.name, self.configure_cmd.name])

        FreeCADGui.addPreferencePage(os.path.join(workbench_path, "Core", "SettingsPanel.py"), "AI-CAD Workbench")


    def Activated(self):
        """This function is called when the workbench is activated"""
        FreeCAD.Console.PrintMessage("AI-CAD Workbench Activated\n")
        # Open the panel automatically when workbench is activated
        if not FreeCADGui.Control.isTaskPanel("AIPromptTaskPanel"):
            self.main_module.open_ai_panel()


    def Deactivated(self):
        """This function is called when the workbench is deactivated"""
        FreeCAD.Console.PrintMessage("AI-CAD Workbench Deactivated\n")
        # Optionally close the panel or other cleanup
        panel = FreeCADGui.Control.getTaskProxy("AIPromptTaskPanel")
        if panel:
            FreeCADGui.Control.closeDialog(panel)
        return

class OpenAIPanelCommand:
    """Command to open the AI Prompt Task Panel"""
    def GetResources(self):
        return {
            "Pixmap": os.path.join(icon_path, "AISendPrompt.svg"), # Use a relevant icon
            "MenuText": "Open AI Prompt Panel",
            "ToolTip": "Opens the panel to send prompts to AI.",
        }

    @property # Make 'name' a property for easy access
    def name(self):
        return "AI_OpenPromptPanel"

    def Activated(self):
        import AIWorkbench as MainModule
        MainModule.open_ai_panel()

    def IsActive(self):
        return True

class ConfigureLLMsCommand:
    """Command to open LLM Configuration (Placeholder)"""
    def GetResources(self):
        return {
            "Pixmap": os.path.join(icon_path, "AIConfigure.svg"),
            "MenuText": "Configure LLMs",
            "ToolTip": "Configure API keys and settings for LLMs (via Preferences).",
        }
    
    @property
    def name(self):
        return "AI_ConfigureLLMs"

    def Activated(self):
        # This will open the FreeCAD Preferences dialog to the specific page
        FreeCADGui.Dialog.showPreferences("AI-CAD Workbench")


    def IsActive(self):
        return True

# Register the workbench
FreeCADGui.addWorkbench(AIWorkbench())