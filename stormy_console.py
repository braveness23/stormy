import FreeCADGui as Gui
from PySide2 import QtWidgets, QtCore
import os

class ConsoleWidget(QtWidgets.QDockWidget):
    """A dockable AI console widget for the Stormy workbench"""
    
    def __init__(self):
        super().__init__("Stormy AI Console")
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the UI components"""
        main_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        
        # Chat history
        self.chat_history = QtWidgets.QTextEdit()
        self.chat_history.setReadOnly(True)
        layout.addWidget(self.chat_history)
        
        # Input area
        input_layout = QtWidgets.QHBoxLayout()
        self.input_field = QtWidgets.QLineEdit()
        self.input_field.setPlaceholderText("Enter your prompt here...")
        self.input_field.returnPressed.connect(self._handle_input)
        
        self.send_button = QtWidgets.QPushButton("Send")
        self.send_button.clicked.connect(self._handle_input)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)
        
        main_widget.setLayout(layout)
        self.setWidget(main_widget)
        self.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable |
                        QtWidgets.QDockWidget.DockWidgetMovable |
                        QtWidgets.QDockWidget.DockWidgetClosable)

    def _handle_input(self):
        """Handle user input and generate mock response"""
        user_input = self.input_field.text().strip()
        if not user_input:
            return
            
        # Display user input
        self.chat_history.append(f"\nYou: {user_input}")
        
        # Mock AI response
        response = f"AI: I received your prompt: '{user_input}'. This is a mock response."
        self.chat_history.append(response)
        
        # Clear input field
        self.input_field.clear()

class ShowAIConsole:
    """Command to show the Stormy AI console"""
    
    def GetResources(self):
        return {
            'MenuText': 'AI Console',
            'ToolTip': 'Open Stormy AI Console',
            'Pixmap': os.path.join(os.path.dirname(__file__), "resources", "ai_console.svg")
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

Gui.addCommand('ShowAIConsole', ShowAIConsole())
