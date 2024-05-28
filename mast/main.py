from PySide6.QtCore import QDir, QUrl
from PySide6.QtWidgets import *
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor, QTextDocument
import os
import shutil
import subprocess
from mast.gui import Ui_MainWindow

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.model = QFileSystemModel()

        self.supportFileType = "Text Files (*.txt);;Markdown Files (*.md);;LaTeX Files (*.tex);;Typst Files (*.typ)"
        
        self.isSaved = True # 标志位，用来判断文本框中的文本是否保存，默认已经保存


        self.defaultFileDir = os.path.expanduser("~\\Documents")
        self.currentFileDir = self.defaultFileDir 
        self.currentFilePath = None # 当前文件的路径，默认没有打开文件，所以路径为 None

        self.model.setRootPath(self.currentFileDir)
        self.ui.treeView.setModel(self.model)
        self.ui.treeView.setRootIndex(self.model.index(self.model.rootPath()))

        self.connectSlot()

    def connectSlot(self):
        self.ui.fileOpen.triggered.connect(self.fileOpen)
        self.ui.fileNew.triggered.connect(self.fileNew)
        self.ui.fileOpenFolder.triggered.connect(self.fileOpenFolder)
        self.ui.fileNewWindow.triggered.connect(self.fileNewWindow)
        self.ui.fileSave.triggered.connect(self.fileSave)
        self.ui.fileSaveAs.triggered.connect(self.fileSaveAs)
        self.ui.fileMoveTo.triggered.connect(self.fileMoveTo)

        self.ui.editUndo.triggered.connect(self.ui.textEdit.undo)
        self.ui.editRedo.triggered.connect(self.ui.textEdit.redo)
        self.ui.editCopy.triggered.connect(self.ui.textEdit.copy)
        self.ui.editCut.triggered.connect(self.ui.textEdit.cut)
        self.ui.editPaste.triggered.connect(self.ui.textEdit.paste)
        self.ui.editFind.triggered.connect(self.editFind)
        self.ui.editJumpToTop.triggered.connect(self.editJumpToTop)
        self.ui.editJumpToBottom.triggered.connect(self.editJumpToBottom)
        self.ui.editJumpToSelection.triggered.connect(self.editJumpToSelection)
        self.ui.editJumpToLineStart.triggered.connect(self.editJumpToLineStart)
        self.ui.editJumpToLineEnd.triggered.connect(self.editJumpToLineEnd)
        self.ui.editReplace.triggered.connect(self.editReplace)

        self.ui.textEdit.textChanged.connect(self._textChanged)

        self.ui.compileLaTeX.triggered.connect(self.compileLaTeX)
        # self.ui.compileTypst.triggered.connect(self.compileTypst) # 拼写错误

        self.ui.helpAbout.triggered.connect(self.helpAbout)

    def fileOpen(self):
        file, ok = QFileDialog.getOpenFileName(self, "Open", self.currentFileDir, self.supportFileType)
        if ok:
            self.currentFilePath = file
            with open(file, 'r') as f:
                content = f.read()
            self.ui.textEdit.setText(content)
            self.ui.statusBar.showMessage(f"Opened: {file}")

    def fileNew(self):
        file, ok = QFileDialog.getSaveFileName(self, "New File", "", self.supportFileType)
        if ok:
            self.currentFilePath = file
            with open(file, 'w') as f:
                f.write('')
            self.ui.textEdit.clear()
            self.ui.statusBar.showMessage(f"Created: {file}")

    def fileNewWindow(self):
        new_window = MainWindow()
        new_window.show()
        self.new_window = new_window

    def fileSave(self):
        """
        保存文件
        """
        if self.currentFilePath: # 如果已经打开了文件
            with open(self.currentFilePath, 'w') as f:
                f.write(self.ui.textEdit.toPlainText())
            self.ui.statusBar.showMessage(f"Saved: {self.currentFilePath}")
        else: # 如果没有打开文件
            if self.ui.textEdit.toPlainText() == '': # 如果文本框中没有文本
                QMessageBox.warning(self, "Warning", "No content to save.")
                return
            else: # 如果文本框中有文本
                self.fileSaveAs()
        
        self.isSaved = True

    def fileSaveAs(self):
        """
        文件另存为
        """
        file, ok = QFileDialog.getSaveFileName(self, "Save File As", "", self.supportFileType)
        if ok:
            self.currentFilePath = file
            with open(file, 'w') as f:
                f.write(self.ui.textEdit.toPlainText())
            self.ui.statusBar.showMessage(f"Saved As: {file}")

    def fileOpenFolder(self):
        """
        打开文件夹
        """
        folder = QFileDialog.getExistingDirectory(self, "Open Folder", self.currentFileDir)
        if folder:
            self.currentFileDir = folder
            self.model.setRootPath(folder)
            self.ui.treeView.setRootIndex(self.model.index(folder))
            self.ui.statusBar.showMessage(f"Opened Folder: {folder}")

    def fileMoveTo(self):
        """
        文件移动
        """
        sourceFile, ok = QFileDialog.getOpenFileName(self, "Select File", "", self.supportFileType)
        if ok:
            destinationFolder = QFileDialog.getExistingDirectory(self, "Select Destination Folder", "")
            if destinationFolder:
                destinationFile = shutil.move(sourceFile, destinationFolder)
                self.ui.statusBar.showMessage(f"Moved to: {destinationFile}")

    def editFind(self):
        text, ok = QInputDialog.getText(self, 'Find', 'Enter text:')
        if ok and text:
            cursor = self.ui.textEdit.textCursor()
            format = QTextCharFormat()
            format.setBackground(QColor('yellow'))
            cursor.setCharFormat(format)
            start_pos = 0
            while self.ui.textEdit.find(text, start_pos, QTextDocument.FindFlags()):
                extra_selections = []
                selection = QTextEdit.ExtraSelection()
                selection.format.setBackground(QColor('yellow'))
                selection.cursor = self.ui.textEdit.textCursor()
                extra_selections.append(selection)
                self.ui.textEdit.setExtraSelections(extra_selections)
                start_pos = self.ui.textEdit.textCursor().position()

    def editReplace(self):
        cursor = self.ui.textEdit.textCursor()
        if cursor.hasSelection():
            text, ok = QInputDialog.getText(self, 'Replace Text', 'Enter new text:')
            if ok:
                cursor.insertText(text)
                self.ui.textEdit.setTextCursor(cursor)

    def editJumpToTop(self):
        self.ui.textEdit.moveCursor(QTextCursor.Start)

    def editJumpToBottom(self):
        self.ui.textEdit.moveCursor(QTextCursor.End)

    def editJumpToSelection(self):
        cursor = self.ui.textEdit.textCursor()
        if cursor.hasSelection():
            start_pos = cursor.selectionStart()
            cursor.setPosition(start_pos)
            self.ui.textEdit.setTextCursor(cursor)
    
    def editJumpToLineStart(self):
        self.ui.textEdit.moveCursor(QTextCursor.StartOfLine)

    def editJumpToLineEnd(self):
        self.ui.textEdit.moveCursor(QTextCursor.EndOfLine)

    def compileLaTeX(self):
        if not self.currentFilePath or not self.currentFilePath.endswith('.tex'):
            QMessageBox.warning(self, "Warning", "The file is not a LaTeX file.")
            return
        
        directory, file = os.path.split(self.currentFilePath)
        command = ['pdflatex', '-interaction=nonstopmode', file]

        try:
            process = subprocess.Popen(command, cwd=directory)
            process.wait()
            self.ui.statusBar.showMessage(f"Compiled LaTeX: {file}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def compileTypst(self):
        if not self.currentFilePath or not self.currentFilePath.endswith('.typ'):
            QMessageBox.warning(self, "Warning", "The file is not a Typst file.")
            return
        
        directory, file = os.path.split(self.currentFilePath)
        command = ['typst', 'compile', file]

        try:
            process = subprocess.Popen(command, cwd=directory)
            process.wait()
            self.ui.statusBar.showMessage(f"Compiled Typst: {file}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def helpAbout(self):
        QMessageBox.about(self, "About", "This is a software created by BFmHNO3.\n\nVersion: 1.0.0")

    # def closeEvent(self, event):
    #     if self.ui.textEdit.toPlainText():
    #         reply = QMessageBox.question(
    #             self, 'Message',
    #             "Are you sure to quit? Any unsaved work will be lost.",
    #             QMessageBox.Yes | QMessageBox.No, QMessageBox.No
    #         )
    #         if reply == QMessageBox.Yes:
    #             event.accept()
    #         else:
    #             event.ignore()
    #     else:
    #         event.accept()

    def _textChanged(self):
        self.isSaved = False

    def closeEvent(self, event):
        if self.currentFilePath:  # 如果打开了文件
            if not self.isSaved:  # 检查是否有未保存的更改
                reply = QMessageBox.question(
                    self, 'Message',
                    "You have unsaved changes. Do you want to save before exiting?",
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
            else:
                event.accept()
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
