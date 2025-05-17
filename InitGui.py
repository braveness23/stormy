import FreeCADGui as Gui
import os

class StormyWorkbench(Workbench):
    MenuText = "Stormy"
    ToolTip = "Stormy Workbench"
    Icon = os.path.join(App.getUserAppDataDir(), "Mod", "stormy", "resources", "stormy_icon.svg")

    def Initialize(self):
        pass  # Add tools and commands here later

Gui.addWorkbench(StormyWorkbench())
