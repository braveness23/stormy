import FreeCADGui as Gui
from PySide2 import QtWidgets, QtCore

class ConsoleWidget(QtWidgets.QDockWidget):
    """A dockable console widget for the Stormy workbench"""
    
    def __init__(self):
        super().__init__("Stormy Console")
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the UI components"""
        self.text_area = QtWidgets.QTextEdit()
        self.text_area.setReadOnly(True)  # Make read-only by default
        self.setWidget(self.text_area)
        self.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable |
                        QtWidgets.QDockWidget.DockWidgetMovable |
                        QtWidgets.QDockWidget.DockWidgetClosable)

class ShowConsole:
    """Command to show the Stormy console"""
    
    def GetResources(self):
        return {
            'MenuText': 'Console',
            'ToolTip': 'Open Stormy Console',
            'Pixmap': ''  # Add an icon path here
        }
        
    def Activated(self):
        mw = Gui.getMainWindow()
        # Check if console already exists
        for widget in mw.findChildren(ConsoleWidget):
            widget.show()
            widget.raise_()
            return
        # Create new console if none exists
        mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, ConsoleWidget())
        
    def IsActive(self):
        return True

Gui.addCommand('ShowConsole', ShowConsole())
