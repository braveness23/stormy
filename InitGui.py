import FreeCADGui as Gui
import os
import FreeCAD as App

class StormyWorkbench(Workbench):
    """Stormy workbench class for FreeCAD"""
    
    MenuText = "Stormy"
    ToolTip = "Stormy Workbench"
    Icon = os.path.join(App.getUserAppDataDir(), "Mod", "stormy", "resources", "stormy_icon.svg")

    def Initialize(self):
        """Initialize workbench - this method is mandatory"""
        import stormy_console  # Import commands when needed
        
        # Create command list
        self.command_list = ["ShowConsole"]
        # self.appendToolbar("Stormy Tools", self.command_list)
        self.appendMenu("Stormy", self.command_list)

    def Activated(self):
        """Called when workbench is activated"""
        return

    def Deactivated(self):
        """Called when workbench is deactivated"""
        return

    def GetClassName(self):
        """Returns workbench classname - mandatory"""
        return "Gui::PythonWorkbench"

Gui.addWorkbench(StormyWorkbench())
