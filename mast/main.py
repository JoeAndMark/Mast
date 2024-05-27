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
        
        self.defaultFileDir = os.path.expanduser("~\\Documents")
        self.currentFileDir = self.defaultFileDir
        self.currentFilePath = None

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
        if self.currentFilePath:
            with open(self.currentFilePath, 'w') as f:
                f.write(self.ui.textEdit.toPlainText())
            self.ui.statusBar.showMessage(f"Saved: {self.currentFilePath}")
        else:
            self.fileSaveAs()

    def fileSaveAs(self):
        file, ok = QFileDialog.getSaveFileName(self, "Save File As", "", self.supportFileType)
        if ok:
            self.currentFilePath = file
            with open(file, 'w') as f:
                f.write(self.ui.textEdit.toPlainText())
            self.ui.statusBar.showMessage(f"Saved As: {file}")

    def fileOpenFolder(self):
        folder = QFileDialog.getExistingDirectory(self, "Open Folder", self.currentFileDir)
        if folder:
            self.currentFileDir = folder
            self.model.setRootPath(folder)
            self.ui.treeView.setRootIndex(self.model.index(folder))
            self.ui.statusBar.showMessage(f"Opened Folder: {folder}")

    def fileMoveTo(self):
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

    def closeEvent(self, event):
        if self.ui.textEdit.toPlainText():
            reply = QMessageBox.question(
                self, 'Message',
                "Are you sure to quit? Any unsaved work will be lost.",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
