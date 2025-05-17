import FreeCADGui as Gui
from PySide2 import QtWidgets, QtCore

class ConsoleWidget(QtWidgets.QDockWidget):
    def __init__(self):
        super().__init__("Stormy Console")
        self.text_area = QtWidgets.QTextEdit()
        self.setWidget(self.text_area)
        self.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable |
                        QtWidgets.QDockWidget.DockWidgetMovable |
                        QtWidgets.QDockWidget.DockWidgetClosable)

class ShowConsole:
    def GetResources(self): return {'MenuText': 'Console', 'ToolTip': 'Open Console'}
    def Activated(self): Gui.getMainWindow().addDockWidget(QtCore.Qt.RightDockWidgetArea, ConsoleWidget())
    def IsActive(self): return True

Gui.addCommand('ShowConsole', ShowConsole())
