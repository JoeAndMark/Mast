"""
模块名称：testUtils.py
模块描述：本模块为对 utils.py 模块的测试模块，用于测试 utils.py 模块的功能是否正常
作者：JoeAndMark
版本：1.0
日期：2024-5-1
"""

# 导入标准库
import os
import sys

sys.path.append("..")

# 导入第三方库
from PySide6.QtCore import QDir, QUrl
from PySide6.QtWidgets import *
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor, QTextDocument, QCloseEvent

# 导入自定义库
from mast.gui import Ui_MainWindow
from mast.utils import FileHandler

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        # 属性
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.model = QFileSystemModel()

        # 设置 Splitter 控件的初始大小
        self.ui.splitter.setSizes([100, 600, 300])

        # 文件操作
        self.fileHandler = FileHandler(self.ui.textEdit)

        # 展示文件目录结构
        self.model.setRootPath(self.fileHandler._getCurrentFileDir)
        self.ui.treeView.setModel(self.model)
        self.ui.treeView.setRootIndex(self.model.index(self.model.rootPath()))
        # 隐藏不需要的栏
        self.ui.treeView.setColumnHidden(1, True)
        self.ui.treeView.setColumnHidden(2, True)
        self.ui.treeView.setColumnHidden(3, True)

        # 渲染窗口
        # self.ui.webEngineView.

        self.connectSlot()

        self.loadCustomCSS()

    def connectSlot(self):
        """
        连接信号与槽函数
        """
        self.ui.fileOpen.triggered.connect(self.fileHandler.fileOpen)
        self.ui.fileNew.triggered.connect(self.fileHandler.fileNew)
        self.ui.fileOpenFolder.triggered.connect(self.fileHandler.fileOpenFolder)
        # self.ui.fileNewWindow.triggered.connect(self.fileHandler.fileNewWindow)
        self.ui.fileSave.triggered.connect(self.fileHandler.fileSave)
        self.ui.fileSaveAs.triggered.connect(self.fileHandler.fileSaveAs)
        self.ui.fileMoveTo.triggered.connect(self.fileHandler.fileMoveTo)

        self.ui.treeView.doubleClicked.connect(self.treeViewDoubleClicked)

    def closeEvent(self, event):
        if self.currentFilePath:  # 如果打开了文件
            self._notSaveWarning()
        else:  # 如果没有打开文件
            if self.ui.textEdit.toPlainText() != '':  # 检查文本框中是否有文本
                reply = QMessageBox.question(
                    self, 'Message',
                    "You have unsaved text. Do you want to save before exiting?",
                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                    QMessageBox.Cancel
                )

                if reply == QMessageBox.Yes:
                    self.fileSave()
                    event.accept()
                elif reply == QMessageBox.No:
                    event.accept()
                else:
                    event.ignore()
            
            else: # 文本框中没有文本，直接退出
                event.accept()
    
    def treeViewDoubleClicked(self):
        """
        目录结构视图下双击文件操作
        """
        filePath = self.model.filePath(self.ui.treeView.currentIndex())
        if os.path.isfile(filePath): # 进行文件操作
            self._notSaveWarning()
            self.fileOpen(filePath)

def main():
    app = QApplication(sys.argv)
    test = MainWindow()
    test.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()