"""
模块名称：main.py
模块描述：本模块为主窗口模块，提供了主窗口的实现。
作者：JoeAndMark
版本：1.0
日期：2024-5-1
"""

# 导入标准库
import os
import shutil
import subprocess

# 导入第三方库
from PySide6.QtCore import QDir, QUrl
from PySide6.QtWidgets import *
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor, QTextDocument, QCloseEvent
from markdown import markdown

# 导入自定义库
from mast.gui import Ui_MainWindow
from highlighter.Markdown import MarkdownHighlighter as mdh

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.customCSS = ""
        self.rendering = False

        # 属性
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.model = QFileSystemModel()

        # 设置 Splitter 控件的初始大小
        self.ui.splitter.setSizes([50, 550, 400])

        # 与文件操作有关的全局变量
        ## 支持的文件类型
        self.supportFileType = """
            Text Files (*.txt);;
            Markdown Files (*.md);;
            LaTeX Files (*.tex);;
            Typst Files (*.typ)
        """

        self.isSaved = True # 标志位，用来判断文本框中的文本是否保存，默认已经保存

        self.defaultFileDir = os.path.expanduser("~\\Documents") # 默认文件夹
        self.currentFileDir = self.defaultFileDir # 当前文件夹
        self.currentFilePath = None # 当前文件的路径，默认没有打开文件，所以路径为 None

        # 展示文件目录结构
        self.model.setRootPath(self.currentFileDir)
        self.ui.treeView.setModel(self.model)
        self.ui.treeView.setRootIndex(self.model.index(self.model.rootPath()))
        # 隐藏不需要的栏
        self.ui.treeView.setColumnHidden(1, True)
        self.ui.treeView.setColumnHidden(2, True)
        self.ui.treeView.setColumnHidden(3, True)

        # 语法高亮
        self.hightlighter = mdh(self.ui.textEdit)

        self.connectSlot()

        self.loadCustomCSS()

    def connectSlot(self):
        """
        连接信号与槽函数
        """
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

        self.ui.textEdit.textChanged.connect(self._fileIsChanged) # 更新标志位
        self.ui.textEdit.textChanged.connect(self.renderMarkdown) # 实时渲染 Markdown

        self.ui.compileLaTeX.triggered.connect(self.compileLaTeX)
        self.ui.compileTypst.triggered.connect(self.compileTypst)

        self.ui.helpAbout.triggered.connect(self.helpAbout)

        self.ui.treeView.doubleClicked.connect(self.treeViewDoubleClicked)

    def fileOpen(self):
        filePath, ok = QFileDialog.getOpenFileName(
            self,
            "打开",
            self.currentFileDir,
            self.supportFileType
        )

        if ok:
            self.currentFilePath = filePath

            with open(filePath, 'r') as f:
                content = f.read()
            
            self.ui.textEdit.setText(content)

            self.renderMarkdown()
            # self.ui.webEngineView.setHtml(markdown(content))

            self.ui.statusBar.showMessage(f"Opened: {filePath}")
            self._fileIsSaved()

    def fileNew(self):
        file, ok = QFileDialog.getSaveFileName(
            self,
            "新建",
            self.defaultFileDir,
            self.supportFileType
        )

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
        file, ok = QFileDialog.getSaveFileName(
            self,
            "Save File As",
            "",
            self.supportFileType
        )
        if ok:
            self.currentFilePath = file
            with open(file, 'w') as f:
                f.write(self.ui.textEdit.toPlainText())
            self.ui.statusBar.showMessage(f"Saved As: {file}")

    def fileOpenFolder(self):
        """
        打开文件夹
        """
        folder = QFileDialog.getExistingDirectory(
            self,
            "Open Folder",
            self.currentFileDir
        )

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
        QMessageBox.about(
            self,
            "About",
            """
            这是我的第一个软件。
            我不想参加Python期末考试，所以我设计了她！
            第一次开发软件，希望大家多多包涵！
            版本：0.90
            （因为今年西农建校90周年）
            """
        )

    def _fileIsChanged(self):
        """
        文件内容发生改变
        """
        self.isSaved = False
        return self.isSaved # 返回当前文件的状态
    
    def _fileIsSaved(self):
        """
        文件内容已经保存
        """
        self.isSaved = True
        return self.isSaved

    def _notSaveWarning(self):
        """
        文件被修改但未保存，弹出警告
        """
        event = QCloseEvent()
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
            self.currentFilePath = filePath

            with open(filePath, 'r') as f:
                content = f.read()
            
            self.ui.textEdit.setText(content)

            self.renderMarkdown()
            # self.ui.webEngineView.setHtml(markdown(content))

            self.ui.statusBar.showMessage(f"Opened: {filePath}")
            self._fileIsSaved()

    def loadCustomCSS(self):
        """
        加载自定义 CSS 文件内容
        """
        css_path = "./mast/resources/themes/default.css"
        if os.path.exists(css_path):
            with open(css_path, "r") as file:
                self.customCSS = file.read()
        else:
            self.customCSS = ""

    def applyTemplate(self, html):
        """
        将 HTML 内容插入模板
        """
        with open("./mast/resources/templates/template.html", "r") as file:
            template = file.read()

        # 添加自定义 CSS 到模板中的 <style> 标签
        template = template.replace("/* Add custom CSS here */", self.customCSS)

        # 插入渲染后的 HTML 内容
        return template.replace("{content}", html)

    def renderMarkdown(self):
        """
        渲染 Markdown
        """
        # 使用的扩展的缩写
        abbr = [
            'extra', # 扩展语法，用来处理汉字
            'codehilite', # 代码高亮
            'toc', # 生成目录
            'tables', # 表格
            'fenced_code', # 代码块
            'footnotes', # 脚注
            'attr_list', # 允许在块级元素和内联元素上添加属性
            'sane_lists' # 改进列表处理
        ]

        extensions = [
            f'markdown.extensions.{ext}' for ext in abbr
        ]

        content = self.ui.textEdit.toPlainText()
        html = markdown(content, extensions=extensions)
        self.ui.webEngineView.setHtml(self.applyTemplate(html))
