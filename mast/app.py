import sys
import subprocess
import os
import shutil
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor, QTextDocument


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # # Markdown 语法高亮
        # self.highlighter = MarkdownHighlighter.MarkdownHighlighter(self.ui.textEdit)

        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())
        self.ui.treeView.setModel(self.model)
        self.ui.treeView.setRootIndex(self.model.index(self.model.rootPath()))

        self.actions = MenuBarActions()

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
        
        # 测试加载pdf
        filePath = os.path.abspath("test.pdf")
        self.ui.webEngineView.load(QUrl.fromLocalFile(r"E:\Downloads\GitRepo\Github\Mast\test.pdf"))
    
    def fileOpen(self):
        file, ok = QFileDialog.getOpenFileName(self, "Open", "E:\Downloads\GitRepo\Github\Mast", \
                                                "Markdown Files (*.md);;Text Files (*.txt);;\
                                                LaTeX Files (*.tex);;Typst Files (*.typ)")
        if ok:
            with open(file, 'r') as f:
                content = f.read()
            self.ui.textEdit.setText(content)
        self.ui.statusBar.showMessage(file) # 在状态栏中显示文件地址

    def fileOpenFolder(self):
        folder = QFileDialog.getExistingDirectory(self, "Open Folder", "E:\Downloads\GitRepo\Github\Mast")
        self.ui.statusBar.showMessage(folder)  # 在状态栏中显示文件夹地址
    
    def fileNew(self):
        """
        创建新文件
        """
        file, ok = QFileDialog.getSaveFileName(self, "New File", "", "Markdowm Files (*.md)")
        if ok:
            with open(file, 'w') as f:
                f.write('')  # 创建一个空文件
            self.ui.statusBar.showMessage(file)  # 在状态栏中显示新文件的地址
    
    def fileNewWindow(self):
        """
        新建窗口
        """
        new_window = MainWindow()  # 假设 MainWindow 是你的窗口类
        new_window.show()
        self.new_window = new_window

    def fileSave(self):
        """
        保存
        """
        file, ok = QFileDialog.getSaveFileName(self, "Save File", "",\
                                                "Markdown Files (*.md);;Text Files (*.txt);;\
                                                LaTeX Files (*.tex);;Typst Files (*.typ)")
        if ok:
            with open(file, 'w') as f:
                f.write(self.ui.textEdit.toPlainText())  # 将文本编辑器中的内容保存到文件中
            self.ui.statusBar.showMessage(file)  # 在状态栏中显示保存的文件地址

    def fileSaveAs(self):
        """
        另存为
        """
        file, ok = QFileDialog.getSaveFileName(self, "Save File As", "", "Markdown Files(*.md);;Text Files (*.txt);;LaTeX Files (*.tex);;Typst Files (*.typ)")
        if ok:
            with open(file, 'w') as f:
                f.write(self.ui.textEdit.toPlainText())  # 将文本编辑器中的内容保存到新的文件中
            self.ui.statusBar.showMessage(file)  # 在状态栏中显示保存的文件地址

    def fileMoveTo(self):
        """
        移动文件
        """
        sourceFile, ok = QFileDialog.getOpenFileName(self, "Select File", "", "Markdown Files(*.md);;Text Files (*.txt);;LaTeX Files (*.tex);;Typst Files (*.typ)")
        if ok:
            destinationFolder = QFileDialog.getExistingDirectory(self, "Select Destination Folder", "")
            if destinationFolder:
                destinationFile = shutil.move(sourceFile, destinationFolder)  # 将文件移动到新的文件夹
                self.ui.statusBar.showMessage(destinationFile)  # 在状态栏中显示移动后的文件地址

    def editFind(self):
        """
        文本查找功能
        有点问题
        """
        text, ok = QInputDialog.getText(self, 'Find', 'Enter text:')
        if ok:
            cursor = self.ui.textEdit.textCursor()
            format = QTextCharFormat()
            format.setBackground(QColor('yellow'))  # 设置高亮颜色为黄色
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
        """
        跳转到文本的开头
        """
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
        cursor = self.ui.textEdit.textCursor()  # 获取当前的文本光标
        cursor.movePosition(QTextCursor.StartOfLine)  # 将光标移动到当前行的开始位置
        self.ui.textEdit.setTextCursor(cursor)  # 设置文本光标

    def editJumpToLineEnd(self):
        cursor = self.ui.textEdit.textCursor()  # 获取当前的文本光标
        cursor.movePosition(QTextCursor.EndOfLine)  # 将光标移动到当前行的结束位置
        self.ui.textEdit.setTextCursor(cursor)  # 设置文本光标

    def compileLaTeX(self):
        """
        编译 tex 文件
        """
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
        """
        编译 typst 文件
        """
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
        """
        替代
        """
        cursor = self.ui.textEdit.textCursor()
        if cursor.hasSelection():
            text, ok = QInputDialog.getText(self, 'Replace Text', 'Enter new text:')
            if ok:
                cursor.insertText(text)
                self.ui.textEdit.setTextCursor(cursor)
    
    def helpAbout(self):
        """
        相关
        """
        QMessageBox.about(self, "About", "This is a software create by BFmHNO3.\n\nVersion: 1.0.0")




def main():
    app = QApplication(sys.argv)
    mast = MainWindow()
    mast.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()