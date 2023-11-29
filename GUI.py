# encoding: utf-8
"""
@Project ：GameTools
@File    ：GUI.py
@IDE     ：
@Author  ：WeiHao
@Date    ：2023/11/28
@Email   ：WeiHao.fox@foxmail.com
"""
from  config import GUIconfig
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
import sys
class MyTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def wheelEvent(self, event):
        pass  # 拦截鼠标滚轮事件
class TransparentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(GUIconfig.positionX, GUIconfig.positionY, GUIconfig.guiSizeX, GUIconfig.guiSizeY)
        # self.setWindowOpacity(1)  # 设置窗口完全透明

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.text_edit =MyTextEdit(self)
        self.text_edit.setReadOnly(True)

        font = QFont(GUIconfig.fontType, GUIconfig.fontSize)
        self.text_edit.setFont(font)
        self.text_edit.setTextColor(QColor(GUIconfig.textcolor))

        layout.addWidget(self.text_edit)

        self.setCentralWidget(central_widget)
        self.text_edit.setStyleSheet(
            "QTextEdit {border: none; padding: 0; background: rgba(255,255,255,0); color: red;font-weight: "";}")  # 设置文本框背景透明

        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    def showmessage(self, message):
        self.text_edit.append(message)
        self.text_edit.ensureCursorVisible()

    def event(self, event):
        if event.type() == QEvent.WindowActivate:
            return False
        return super().event(event)

app = QApplication([])
window = TransparentWindow()
window.show()

