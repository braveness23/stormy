import FreeCADGui as Gui

class StormyWorkbench(Workbench):
    MenuText = "Stormy"
    ToolTip = "Stormy Workbench"
    
    def Initialize(self):
        pass  # Add tools and commands here later

Gui.addWorkbench(StormyWorkbench())
