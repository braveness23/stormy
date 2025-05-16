# AIFreeCADWorkbench/AIWorkbench.py
import FreeCAD
import FreeCADGui

# Store a reference to the panel if it's created
_panel_instance = None

def open_ai_panel():
    global _panel_instance
    if _panel_instance is None or not FreeCADGui.Control.isTaskPanel("AIPromptTaskPanel"):
        from .Panels.AIPromptTaskPanel import AIPromptTaskPanel
        _panel_instance = AIPromptTaskPanel()
        FreeCADGui.Control.showDialog(_panel_instance)
    else:
        # Panel already exists, maybe bring to front if needed, or just log
        FreeCAD.Console.PrintMessage("AI Prompt Panel is already open.\n")

def close_ai_panel():
    global _panel_instance
    if _panel_instance and FreeCADGui.Control.isTaskPanel("AIPromptTaskPanel"):
        FreeCADGui.Control.closeDialog(_panel_instance)
        _panel_instance = None

# This module can be expanded with more workbench-specific logic if needed.