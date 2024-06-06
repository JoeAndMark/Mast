"""
模块名称：utils.py
模块描述：本模块为通用工具模块，提供了一些通用的工具类。这些工具类是为了工具栏的功能而设计的。
作者：JoeAndMark
版本：1.0
日期：2024-5-1
"""

# 导入标准库
import os
import shutil

# 导入第三方库
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtGui import QCloseEvent

# 导入自定义库


class FileHandler:
    def __init__(self, textEdit, statusBar = None):
        # 需要维护的常量
        ## 支持的文件类型
        self.SUPPORT_FILE_TYPE = """
            Text Files (*.txt);;
            Markdown Files (*.md);;
            LaTeX Files (*.tex);;
            Typst Files (*.typ)
        """
        ## 默认文件夹
        self.DEFAULT_FILE_DIR = os.path.expanduser("~\\Documents")

        self._textEdit = textEdit
        self._statusBar = statusBar

        # 标志位，用来判断文本框中的文本是否保存，默认已经保存
        self._isSaved = True

        # 当前文件夹
        self._currentFileDir = self.DEFAULT_FILE_DIR
        # 当前文件的路径，默认没有打开文件，所以路径为 None
        self._currentFilePath = None

    def readFile(self):
        """
        读取文件内容
        Returns:
            返回文件的内容
        """

        with open(self._getCurrentFilePath(), 'r') as f:
            content = f.read()
        
        return content


    def fileOpen(self):
        """
        打开文件，此函数不对文件进行操作，只更新currentFilePath的值。
        同时将isSaved标志位设置为True，表示默认情况下文件已保存。
        Returns:
            返回打开文件的路径和状态
        """
        filePath, ok = QFileDialog.getOpenFileName(
            self,
            "打开",
            self.currentFileDir,
            self.SUPPORT_FILE_TYPE
        )

        if ok:
            self._updateCurrentFileDir(filePath) # 更新当前文件路径
            self._updateFileState(True) # 打开的文件默认已保存

            if self._statusBar != None:
                self._statusBar.showMessage(f"已打开: {filePath}")

        return self._getCurrentFilePath(), self._getFileState()

    def fileNew(self, textEdit, statusBar = None):
        """
        创建新文件，此函数会在指定目录下创建一个新文件，同时刷新currentFilePath的值。
        此函数会清空文本框中的文本
        Args:
            textEdit: 当前选择的文本框，用于清空文本框中的文本
            statusBar: 状态栏控件
        Returns:
            返回新建文件的路径和状态
        """
        file, ok = QFileDialog.getSaveFileName(
            self,
            "新建",
            "",
            self.SUPPORT_FILE_TYPE
        )

        if ok:
            # 创建新文件
            with open(file, 'w') as f:
                f.write('')

            if self._getCurrentFilePath() != None: # 如果打开了文件
                if self._getFileState() == True: # 如果打开的文件已保存
                    textEdit.clear() # 清空文本框中的内容
                else: # 打开的文件被修改而且没保存
                    decision = self._notSaveWarning() # 弹出警告
                    if decision == True: # 选择保存
                        self.fileSave(textEdit, statusBar)
                    elif decision == False:
                        textEdit.clear()
                    elif decision == None:
                        return None

            if statusBar != None:
                statusBar.showMessage(f"已创建: {file}") # 状态栏打印信息
            
            self._updateFilePath(file) # 更新当前文件路径
            return self._getCurrentFilePath(), self._getFileState()

    def fileSave(self, textEdit, statusBar = None):
        """
        保存文件
        Args:
            textEdit: 当前选择的文本框控件，用来获取文本框中的文本
            statusBar: 状态栏控件
        Returns:
            返回保存的文件的路径和状态
        """
        if self._getCurrentFilePath() != None: # 如果已经打开了文件
            with open(self._getCurrentFilePath(), 'w') as f:
                f.write(textEdit.toPlainText())
            if statusBar != None:
                statusBar.showMessage(f"已保存: {self._getCurrentFilePath()}")
            self._updateFileState(True)

            return self._getCurrentFilePath(), self._getFileState()
        else: # 如果没有打开文件
            if textEdit.toPlainText() == '': # 如果文本框中没有文本
                # QMessageBox.warning(self, "警告", "没有可保存的内容！")
                self.fileNew(textEdit, statusBar)
            else: # 如果文本框中有文本
                return self.fileSaveAs(textEdit, statusBar)

    def fileSaveAs(self, textEdit, statusBar = None):
        """
        文件另存为
        Args:
            textEdit: 当前选择的文本框控件，用来获取文本框中的文本
            statusBar: 状态栏控件
        Returns:
            返回另存为的文件路径和状态
        """
        file, ok = QFileDialog.getSaveFileName(
            self,
            "另存为",
            self.DEFAULT_FILE_DIR,
            self.SUPPORT_FILE_TYPE
        )

        if ok:
            with open(file, 'w') as f:
                f.write(textEdit.toPlainText())
            if statusBar != None:
                statusBar.showMessage(f"另存为: {file}")
            
            self._updateFileState(True)
            self._updateFilePath(file)

            return self._getCurrentFilePath(), self._getFileState()

    def fileOpenFolder(self, model, treeView, statusBar = None):
        """
        打开文件夹
        """
        folder = QFileDialog.getExistingDirectory(
            self,
            "选择文件夹",
            self.currentFileDir
        )

        if folder:
            self.currentFileDir = folder
            model.setRootPath(folder)
            treeView.setRootIndex(model.index(folder))
            if statusBar != None:
                statusBar.showMessage(f"已打开文件夹: {folder}")

    def fileMoveTo(self, textEdit, statusBar = None):
        """
        文件移动。没有打开文件时，新建一个文件并保存；打开文件时，将文件另存到指定文件夹。
        Args:
            textEdit: 当前选择的文本框控件，用来获取文本框中的文本
            statusBar: 状态栏控件
        Returns:
            返回移动文件的路径和状态
        """
        if self._getCurrentFilePath() == None: # 未打开文件
            filePath, state = self.fileNew(textEdit, statusBar)
        else:
            filePath, state = self.fileSaveAs(textEdit, statusBar)
        
        if statusBar != None:
            statusBar.showMessage(f"已移动到: {filePath}")

        return filePath, state
        

    def _updateFileState(self, status):
        """
        更新文件状态

        Args:
            status: 当前文件状态
                True: 文件已保存
                False:文件发生改变
        Returns:
            返回当前文件的状态
        """
        self.isSaved = status

        return self.isSaved
        
    def _fileIsChanged(self):
        """
        文件内容发生改变
        该api被_updateFileState()覆写，暂时未更改
        """
        self.isSaved = False
        return self.isSaved # 返回当前文件的状态
    
    def _fileIsSaved(self):
        """
        文件内容已经保存
        该api被_updateFileState()覆写，暂时未更改
        """
        self.isSaved = True
        return self.isSaved
    
    def _getFileState(self):
        """
        获取当前函数的状态

        Returns:
            True: 文件已保存
            False: 文件未保存
        """
        return self.isSaved

    def _updateFilePath(self, filePath):
        """
        更新文件路径
        Args:
            filePath: 文件路径
        Returns:
            返回当前文件路径
        """

        self.currentFilePath = filePath
        return self.currentFilePath
    
    def _getCurrentFilePath(self):
        """
        获取当前文件路径
        Returns:
            返回当前文件路径
                None: 表示没打开文件
        """
        return self.currentFilePath
    
    def _updateCurrentFileDir(self, fileDir):
        """
        更新当前文件所在的文件夹
        """
        self.currentFileDir = fileDir
        return self.currentFileDir
    
    def _getCurrentFileDir(self):
        """
        获取当前文件所在的文件夹
        """
        return self.currentFileDir
    
    def _notSaveWarning(self):
        """
        文件被修改但未保存，弹出警告
        Returns:
            True: 保存文件
            False: 不保存文件
            Cancel: 取消操作
        """
        reply = QMessageBox.question(
            self, 'Message',
            "You have unsaved changes. Do you want to save before exiting?",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Cancel
        )

        if reply == QMessageBox.Yes:
            return True
        elif reply == QMessageBox.No:
            return False
        elif reply == QMessageBox.Cancel:
            return None



class EditHandler:
    def __init__(self):
        pass


class CompileHandler:
    def __init__(self):
        pass
