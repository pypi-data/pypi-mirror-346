# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(728, 563)
        font = QFont()
        font.setFamilies([u"DejaVu Sans Mono"])
        font.setPointSize(12)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"/* Main window background */\n"
"QMainWindow {\n"
"    background-color: #282c34;\n"
"}\n"
"\n"
"/* Scroll bars */\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
"    background: #282c34;\n"
"    width: 10px;\n"
"    margin: 0px 0px 0px 0px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background: #4f5666;\n"
"    min-height: 20px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"    background: none;\n"
"}\n"
"\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"}\n"
"\n"
"/* Text edit (message input) */\n"
"QTextEdit {\n"
"    background-color: #282c34;\n"
"    color: #abb2bf;\n"
"    border: 1px solid #3e4451;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"    selection-background-color: #3e4451;\n"
"    font-family: 'Consolas', 'Monaco', monospace;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"/* Message display area */\n"
"QTextBrowser {\n"
"    background-color: #282"
                        "c34;\n"
"    color: #abb2bf;\n"
"    border: none;\n"
"    padding: 5px;\n"
"    selection-background-color: #3e4451;\n"
"    font-family: 'Consolas', 'Monaco', monospace;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"/* Buttons */\n"
"QPushButton {\n"
"    background-color: #3e4451;\n"
"    color: #abb2bf;\n"
"    border: 1px solid #3e4451;\n"
"    border-radius: 4px;\n"
"    padding: 5px 10px;\n"
"    min-width: 60px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #4f5666;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #3e4451;\n"
"}\n"
"\n"
"/* Line edits (username, etc.) */\n"
"QLineEdit {\n"
"    background-color: #282c34;\n"
"    color: #abb2bf;\n"
"    border: 1px solid #3e4451;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"    selection-background-color: #3e4451;\n"
"    font-family: 'Consolas', 'Monaco', monospace;\n"
"}\n"
"\n"
"/* Labels */\n"
"QLabel {\n"
"    color: #abb2bf;\n"
"    font-family: 'Consolas', 'Monaco', monospace;\n"
"}\n"
"\n"
"/* List widgets (user l"
                        "ist, etc.) */\n"
"QListWidget {\n"
"    background-color: #282c34;\n"
"    color: #abb2bf;\n"
"    border: 1px solid #3e4451;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"    selection-background-color: #3e4451;\n"
"    font-family: 'Consolas', 'Monaco', monospace;\n"
"}\n"
"\n"
"/* Tab widgets */\n"
"QTabWidget::pane {\n"
"    border: 1px solid #3e4451;\n"
"    background: #282c34;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    background: #282c34;\n"
"    color: #abb2bf;\n"
"    border: 1px solid #3e4451;\n"
"    padding: 5px 10px;\n"
"    margin-right: 2px;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    background: #3e4451;\n"
"    border-bottom: 2px solid #61afef;\n"
"}\n"
"\n"
"/* Tooltips */\n"
"QToolTip {\n"
"    background-color: #3e4451;\n"
"    color: #abb2bf;\n"
"    border: 1px solid #3e4451;\n"
"    padding: 5px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"/* Message bubbles */\n"
".message-bubble {\n"
"    background-color: #3e4451;\n"
"    color: #abb2bf;\n"
"    border-radius: 4px;\n"
"    paddi"
                        "ng: 5px;\n"
"    margin: 2px;\n"
"}\n"
"\n"
".message-bubble-sender {\n"
"    background-color: #3e4451;\n"
"    color: #61afef;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
".message-bubble-time {\n"
"    color: #5c6370;\n"
"    font-size: 10px;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.textEdit_msg = QTextEdit(self.centralwidget)
        self.textEdit_msg.setObjectName(u"textEdit_msg")
        self.textEdit_msg.setStyleSheet(u"")
        self.textEdit_msg.setUndoRedoEnabled(False)
        self.textEdit_msg.setReadOnly(True)

        self.verticalLayout.addWidget(self.textEdit_msg)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit_cmd = QLineEdit(self.centralwidget)
        self.lineEdit_cmd.setObjectName(u"lineEdit_cmd")

        self.horizontalLayout.addWidget(self.lineEdit_cmd)

        self.pushButton_send = QPushButton(self.centralwidget)
        self.pushButton_send.setObjectName(u"pushButton_send")

        self.horizontalLayout.addWidget(self.pushButton_send)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QChat", None))
        self.pushButton_send.setText(QCoreApplication.translate("MainWindow", u"Send", None))
    # retranslateUi

