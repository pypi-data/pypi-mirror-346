import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from .main_window import Ui_MainWindow
from datetime import datetime
from .command import execute

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Connect signals
        self.ui.pushButton_send.clicked.connect(self.send_message)
        self.ui.lineEdit_cmd.returnPressed.connect(self.send_message)
        
        self.add_message("System", "Chat started")
    
    def send_message(self):
        user_msg = self.ui.lineEdit_cmd.text().strip()
        if user_msg:
            self.add_message("You", user_msg)
            self.ui.lineEdit_cmd.clear()
            self.handle_user_msg(user_msg)

    def handle_user_msg(self, user_msg):
        result = execute(user_msg)
        self.add_message("System", result)
    
    def add_message(self, sender, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.ui.textEdit_msg.append(f"[{timestamp}] <b>{sender}:</b> {message}")

def run():
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())

