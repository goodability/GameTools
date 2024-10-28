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
        self.setFocusPolicy(Qt.NoFocus)
        self.setMouseTracking(False)
    def wheelEvent(self, event):
        pass  # 拦截鼠标滚轮事件
    def mouseReleaseEvent(self,event):
        pass
    def mousePressEvent(self, event):
        event.ignore()
    def enterEvent(self, event):
        cursor = self.textCursor()
        cursor.clearSelection()
        self.setTextCursor(cursor)
        self.viewport().setCursor(Qt.ArrowCursor)
    def mouseDoubleClickEvent(self, event):
        event.ignore()

    def keyPressEvent(self, event):
        event.ignore()  # 忽略键盘按下事件，使其不会传递到父组件

    def keyReleaseEvent(self, event):
        event.ignore()  # 忽略键盘释放事件，使其不会传递到父组件
class TransparentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground,True)
        self.setMouseTracking(False)
        self.setGeometry(GUIconfig.positionX, GUIconfig.positionY, GUIconfig.guiSizeX, GUIconfig.guiSizeY)
        # self.setWindowOpacity(1)  # 设置窗口完全透明
        self.installEventFilter(self)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.text_edit =MyTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setEnabled(False)
        font = QFont(GUIconfig.fontType, GUIconfig.fontSize)
        self.text_edit.setFont(font)
        self.text_edit.setTextColor(QColor(GUIconfig.textcolor))
        self.text_edit.setContextMenuPolicy(Qt.NoContextMenu)
        self.text_edit.setAttribute(Qt.WA_TransparentForMouseEvents)
        layout.addWidget(self.text_edit)

        self.setCentralWidget(central_widget)
        self.text_edit.setStyleSheet(
            "QTextEdit {border: none; padding: 0; background: rgba(255,255,255,0); color: red;font-weight: bold;}")  # 设置文本框背景透明

        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    def showmessage(self, message,**kwargs):
        if "importantText" in kwargs.keys():
            self.text_edit.setTextColor(QColor(GUIconfig.importantTextColor))
        else:
            self.text_edit.setTextColor(QColor(GUIconfig.textcolor))
        self.text_edit.append(message)
        self.text_edit.ensureCursorVisible()

    def event(self, event):
        if event.type() == QEvent.WindowActivate:
            return False
        return super().event(event)

app = QApplication([])
window = TransparentWindow()
window.show()

