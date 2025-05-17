import FreeCADGui as Gui
from PySide2 import QtWidgets, QtCore, QtGui
import os
from enum import Enum, auto

class MessageType(Enum):
    """Enum for different types of chat messages"""
    USER = auto()
    AI = auto()
    SYSTEM = auto()

class ChatMessageWidget(QtWidgets.QWidget):
    """Widget to display any type of chat message with optional copy button"""
    
    def __init__(self, message: str, msg_type: MessageType, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        
        # Message container for better word wrapping
        msg_container = QtWidgets.QWidget()
        msg_layout = QtWidgets.QVBoxLayout()
        msg_layout.setContentsMargins(0, 0, 0, 0)
        msg_container.setLayout(msg_layout)
        
        # Message text with prefix based on type
        prefix = "You: " if msg_type == MessageType.USER else "AI: " if msg_type == MessageType.AI else ""
        text = QtWidgets.QLabel(f"{prefix}{message}")
        text.setWordWrap(True)
        text.setTextFormat(QtCore.Qt.PlainText)
        text.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        text.setMinimumWidth(100)  # Ensure minimum width for wrapping
        msg_layout.addWidget(text)
        
        layout.addWidget(msg_container, stretch=1)
        
        # Add copy button for AI responses
        if msg_type == MessageType.AI:
            copy_button = QtWidgets.QPushButton()
            copy_button.setIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), "resources", "copy_icon.svg")))
            copy_button.setToolTip("Copy response to clipboard")
            copy_button.setFixedSize(20, 20)
            copy_button.clicked.connect(lambda: self._copy_to_clipboard(message))
            layout.addWidget(copy_button, alignment=QtCore.Qt.AlignTop)
        
        self.setLayout(layout)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        
    def _copy_to_clipboard(self, text: str) -> None:
        """Copy text to clipboard"""
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(text)

class ConsoleWidget(QtWidgets.QDockWidget):
    """A dockable AI console widget for the Stormy workbench"""
    
    def __init__(self):
        super().__init__("Stormy AI Console")
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the UI components"""
        main_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        
        # Chat history - using QScrollArea for better control
        scroll_area = QtWidgets.QScrollArea()
        self.chat_container = QtWidgets.QWidget()
        self.chat_layout = QtWidgets.QVBoxLayout()
        self.chat_container.setLayout(self.chat_layout)
        scroll_area.setWidget(self.chat_container)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
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
        self.chat_layout.addWidget(ChatMessageWidget(user_input, MessageType.USER))
        
        # Mock AI response
        response = f"I received your prompt: '{user_input}'. This is a mock response."
        self.chat_layout.addWidget(ChatMessageWidget(response, MessageType.AI))
        
        # Clear input field
        self.input_field.clear()
        
        # Scroll to bottom using proper scroll area method
        scroll_area = self.chat_container.parent()
        if isinstance(scroll_area, QtWidgets.QScrollArea):
            vsb = scroll_area.verticalScrollBar()
            vsb.setValue(vsb.maximum())

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
