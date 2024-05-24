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
        self.model = QFileSystemModel()\

        self.supportFileType = "Text Files (*.txt);;Markdown Files (*.md);;LaTeX Files (*.tex);;Typst Files (*.typ)"
        
        self.defaultFileDir = os.path.expanduser("~\\Documents")

        self.currentFileDir = self.defaultFileDir # 刚运行软件时，设置为默认文件路径
        self.model.setRootPath(self.currentFileDir)
        self.ui.treeView.setModel(self.model)
        self.ui.treeView.setRootIndex(self.model.index(self.model.rootPath()))

        self.connectSlot()
    
    def fileOpen(self):
        file, ok = QFileDialog.getOpenFileName(self, "Open", self.currentFileDir, self.supportFileType)
        if ok:
            with open(file, 'r') as f:
                content = f.read()
            self.ui.textEdit.setText(content)
        self.ui.statusBar.showMessage(file)

    def fileOpenFolder(self):
        folder = QFileDialog.getExistingDirectory(self, "Open Folder", self.currentFileDir)
        self.ui.statusBar.showMessage(folder)
    
    def fileNew(self):
        file, ok = QFileDialog.getSaveFileName(self, "New File", "", self.supportFileType)
        if ok:
            with open(file, 'w') as f:
                f.write('')
            self.ui.statusBar.showMessage(file)
    
    def fileNewWindow(self):
        new_window = MainWindow()
        new_window.show()
        self.new_window = new_window

    def fileSave(self):
        file, ok = QFileDialog.getSaveFileName(self, "Save File", "", self.supportFileType)
        if ok:
            with open(file, 'w') as f:
                f.write(self.ui.textEdit.toPlainText())
            self.ui.statusBar.showMessage(file)

    def fileSaveAs(self):
        file, ok = QFileDialog.getSaveFileName(self, "Save File As", "", self.supportFileType)
        if ok:
            with open(file, 'w') as f:
                f.write(self.ui.textEdit.toPlainText())
            self.ui.statusBar.showMessage(file)

    def fileMoveTo(self):
        sourceFile, ok = QFileDialog.getOpenFileName(self, "Select File", "", self.supportFileType)
        if ok:
            destinationFolder = QFileDialog.getExistingDirectory(self, "Select Destination Folder", "")
            if destinationFolder:
                destinationFile = shutil.move(sourceFile, destinationFolder)
                self.ui.statusBar.showMessage(destinationFile)

    def editFind(self):
        text, ok = QInputDialog.getText(self, 'Find', 'Enter text:')
        if ok:
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

    def editJumpToTop(self):
        cursor = self.ui.textEdit.textCursor()
        cursor.movePosition(QTextCursor.Start)
        self.ui.textEdit.setTextCursor(cursor)
    
    def editJumpToBottom(self):
        cursor = self.ui.textEdit.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.ui.textEdit.setTextCursor(cursor)

    def editJumpToSelection(self):
        cursor = self.ui.textEdit.textCursor()
        if cursor.hasSelection():
            start_pos = cursor.selectionStart()
            cursor.setPosition(start_pos)
            self.ui.textEdit.setTextCursor(cursor)
    
    def editJumpToLineStart(self):
        cursor = self.ui.textEdit.textCursor()
        cursor.movePosition(QTextCursor.StartOfLine)
        self.ui.textEdit.setTextCursor(cursor)

    def editJumpToLineEnd(self):
        cursor = self.ui.textEdit.textCursor()
        cursor.movePosition(QTextCursor.EndOfLine)
        self.ui.textEdit.setTextCursor(cursor)

    def compileLaTeX(self):
        filePath = self.ui.textEdit.toPlainText()
        directory, file  = os.path.split(filePath)
        baseName, ext = os.path.splitext(file)

        if ext.lower() != '.tex':
            QMessageBox.warning(self, "Warning", "The file is not a LaTeX file.")
            return
        
        command = [
            'pdflatex',
            '-interaction=nonstopmode',
            file
        ]

        try:
            process = subprocess.Popen(command, cwd=directory)
            process.wait()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def compileTypst(self):
        filePath = self.ui.textEdit.toPlainText()
        directory, file = os.path.split(filePath)
        baseName, ext = os.path.splitext(file)

        if ext.lower() != '.typ':
            QMessageBox.warning(self, "Warning", "The file is not a Typst file.")
            return
        
        command = ['typst', 'compile', file]

        try:
            process = subprocess.Popen(command, cwd=directory)
            process.wait()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def editReplace(self):
        cursor = self.ui.textEdit.textCursor()
        if cursor.hasSelection():
            text, ok = QInputDialog.getText(self, 'Replace Text', 'Enter new text:')
            if ok:
                cursor.insertText(text)
                self.ui.textEdit.setTextCursor(cursor)
    
    def helpAbout(self):
        QMessageBox.about(self, "About", "This is a software create by BFmHNO3.\n\nVersion: 1.0.0")

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
        self.ui.editCopy.triggered.connect(self.ui.textEdit.cut)
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
        self.ui.complileTypst.triggered.connect(self.compileTypst)

        self.ui.helpAbout.triggered.connect(self.helpAbout)

        # self.ui.webEngineView.load(QUrl.fromLocalFile(filePath))
