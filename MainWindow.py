# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QStatusBar, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.resize(1000, 618)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.fileNew = QAction(MainWindow)
        self.fileNew.setObjectName(u"fileNew")
        self.fileNewWindow = QAction(MainWindow)
        self.fileNewWindow.setObjectName(u"fileNewWindow")
        self.fileOpen = QAction(MainWindow)
        self.fileOpen.setObjectName(u"fileOpen")
        self.fileOpenFolder = QAction(MainWindow)
        self.fileOpenFolder.setObjectName(u"fileOpenFolder")
        self.fileOpenRecent = QAction(MainWindow)
        self.fileOpenRecent.setObjectName(u"fileOpenRecent")
        self.fileSave = QAction(MainWindow)
        self.fileSave.setObjectName(u"fileSave")
        self.fileSaveAs = QAction(MainWindow)
        self.fileSaveAs.setObjectName(u"fileSaveAs")
        self.fileMoveTo = QAction(MainWindow)
        self.fileMoveTo.setObjectName(u"fileMoveTo")
        self.actionSave_All = QAction(MainWindow)
        self.actionSave_All.setObjectName(u"actionSave_All")
        self.editUndo = QAction(MainWindow)
        self.editUndo.setObjectName(u"editUndo")
        self.editRedo = QAction(MainWindow)
        self.editRedo.setObjectName(u"editRedo")
        self.editCut = QAction(MainWindow)
        self.editCut.setObjectName(u"editCut")
        self.editCopy = QAction(MainWindow)
        self.editCopy.setObjectName(u"editCopy")
        self.editPaste = QAction(MainWindow)
        self.editPaste.setObjectName(u"editPaste")
        self.editSelectAll = QAction(MainWindow)
        self.editSelectAll.setObjectName(u"editSelectAll")
        self.editJumpToTop = QAction(MainWindow)
        self.editJumpToTop.setObjectName(u"editJumpToTop")
        self.editJumpToSelection = QAction(MainWindow)
        self.editJumpToSelection.setObjectName(u"editJumpToSelection")
        self.editJumpToBottom = QAction(MainWindow)
        self.editJumpToBottom.setObjectName(u"editJumpToBottom")
        self.editJumpToLineStart = QAction(MainWindow)
        self.editJumpToLineStart.setObjectName(u"editJumpToLineStart")
        self.editJumpToLineEnd = QAction(MainWindow)
        self.editJumpToLineEnd.setObjectName(u"editJumpToLineEnd")
        self.actionFind_and_Replace = QAction(MainWindow)
        self.actionFind_and_Replace.setObjectName(u"actionFind_and_Replace")
        self.editFind = QAction(MainWindow)
        self.editFind.setObjectName(u"editFind")
        self.editFindNext = QAction(MainWindow)
        self.editFindNext.setObjectName(u"editFindNext")
        self.editFindPrevious = QAction(MainWindow)
        self.editFindPrevious.setObjectName(u"editFindPrevious")
        self.editReplace = QAction(MainWindow)
        self.editReplace.setObjectName(u"editReplace")
        self.helpAbout = QAction(MainWindow)
        self.helpAbout.setObjectName(u"helpAbout")
        self.compileLaTeX = QAction(MainWindow)
        self.compileLaTeX.setObjectName(u"compileLaTeX")
        self.complileTypst = QAction(MainWindow)
        self.complileTypst.setObjectName(u"complileTypst")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy1)
        self.textEdit.setFrameShape(QFrame.NoFrame)
        self.textEdit.setLineWidth(0)

        self.verticalLayout.addWidget(self.textEdit)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1000, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuSelection = QMenu(self.menuEdit)
        self.menuSelection.setObjectName(u"menuSelection")
        self.menuFind_and_Replace = QMenu(self.menuEdit)
        self.menuFind_and_Replace.setObjectName(u"menuFind_and_Replace")
        self.menuCompile = QMenu(self.menubar)
        self.menuCompile.setObjectName(u"menuCompile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuCompile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.fileNew)
        self.menuFile.addAction(self.fileNewWindow)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.fileOpen)
        self.menuFile.addAction(self.fileOpenFolder)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.fileOpenRecent)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.fileSave)
        self.menuFile.addAction(self.fileSaveAs)
        self.menuFile.addAction(self.fileMoveTo)
        self.menuEdit.addAction(self.editUndo)
        self.menuEdit.addAction(self.editRedo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.editCut)
        self.menuEdit.addAction(self.editCopy)
        self.menuEdit.addAction(self.editPaste)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.menuSelection.menuAction())
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.menuFind_and_Replace.menuAction())
        self.menuSelection.addAction(self.editSelectAll)
        self.menuSelection.addSeparator()
        self.menuSelection.addAction(self.editJumpToTop)
        self.menuSelection.addAction(self.editJumpToSelection)
        self.menuSelection.addAction(self.editJumpToBottom)
        self.menuSelection.addSeparator()
        self.menuSelection.addAction(self.editJumpToLineStart)
        self.menuSelection.addAction(self.editJumpToLineEnd)
        self.menuSelection.addSeparator()
        self.menuFind_and_Replace.addAction(self.editFind)
        self.menuFind_and_Replace.addAction(self.editFindNext)
        self.menuFind_and_Replace.addAction(self.editFindPrevious)
        self.menuFind_and_Replace.addSeparator()
        self.menuFind_and_Replace.addAction(self.editReplace)
        self.menuCompile.addAction(self.compileLaTeX)
        self.menuCompile.addAction(self.complileTypst)
        self.menuHelp.addAction(self.helpAbout)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Mast", None))
        self.fileNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
#if QT_CONFIG(tooltip)
        self.fileNew.setToolTip(QCoreApplication.translate("MainWindow", u"Create new file.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.fileNew.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.fileNewWindow.setText(QCoreApplication.translate("MainWindow", u"New Window", None))
#if QT_CONFIG(shortcut)
        self.fileNewWindow.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+N", None))
#endif // QT_CONFIG(shortcut)
        self.fileOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(shortcut)
        self.fileOpen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.fileOpenFolder.setText(QCoreApplication.translate("MainWindow", u"Open Folder", None))
#if QT_CONFIG(tooltip)
        self.fileOpenFolder.setToolTip(QCoreApplication.translate("MainWindow", u"Open a Folder instead of file.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.fileOpenFolder.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+O", None))
#endif // QT_CONFIG(shortcut)
        self.fileOpenRecent.setText(QCoreApplication.translate("MainWindow", u"Open Recent", None))
        self.fileSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.fileSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.fileSaveAs.setText(QCoreApplication.translate("MainWindow", u"Save As", None))
#if QT_CONFIG(shortcut)
        self.fileSaveAs.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+S", None))
#endif // QT_CONFIG(shortcut)
        self.fileMoveTo.setText(QCoreApplication.translate("MainWindow", u"Move To", None))
        self.actionSave_All.setText(QCoreApplication.translate("MainWindow", u"Save All", None))
        self.editUndo.setText(QCoreApplication.translate("MainWindow", u"Undo", None))
#if QT_CONFIG(shortcut)
        self.editUndo.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Z", None))
#endif // QT_CONFIG(shortcut)
        self.editRedo.setText(QCoreApplication.translate("MainWindow", u"Redo", None))
#if QT_CONFIG(shortcut)
        self.editRedo.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Y", None))
#endif // QT_CONFIG(shortcut)
        self.editCut.setText(QCoreApplication.translate("MainWindow", u"Cut", None))
#if QT_CONFIG(shortcut)
        self.editCut.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+X", None))
#endif // QT_CONFIG(shortcut)
        self.editCopy.setText(QCoreApplication.translate("MainWindow", u"Copy", None))
#if QT_CONFIG(shortcut)
        self.editCopy.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+C", None))
#endif // QT_CONFIG(shortcut)
        self.editPaste.setText(QCoreApplication.translate("MainWindow", u"Paste", None))
#if QT_CONFIG(shortcut)
        self.editPaste.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+V", None))
#endif // QT_CONFIG(shortcut)
        self.editSelectAll.setText(QCoreApplication.translate("MainWindow", u"Select All", None))
#if QT_CONFIG(shortcut)
        self.editSelectAll.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+A", None))
#endif // QT_CONFIG(shortcut)
        self.editJumpToTop.setText(QCoreApplication.translate("MainWindow", u"Jump to Top", None))
#if QT_CONFIG(shortcut)
        self.editJumpToTop.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Home", None))
#endif // QT_CONFIG(shortcut)
        self.editJumpToSelection.setText(QCoreApplication.translate("MainWindow", u"Jump to Selection", None))
#if QT_CONFIG(shortcut)
        self.editJumpToSelection.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+J", None))
#endif // QT_CONFIG(shortcut)
        self.editJumpToBottom.setText(QCoreApplication.translate("MainWindow", u"Jump to Bottom", None))
#if QT_CONFIG(shortcut)
        self.editJumpToBottom.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+End", None))
#endif // QT_CONFIG(shortcut)
        self.editJumpToLineStart.setText(QCoreApplication.translate("MainWindow", u"Jump to Line Start", None))
        self.editJumpToLineEnd.setText(QCoreApplication.translate("MainWindow", u"Jump to Line End", None))
        self.actionFind_and_Replace.setText(QCoreApplication.translate("MainWindow", u"Find and Replace", None))
        self.editFind.setText(QCoreApplication.translate("MainWindow", u"Find", None))
#if QT_CONFIG(shortcut)
        self.editFind.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+F", None))
#endif // QT_CONFIG(shortcut)
        self.editFindNext.setText(QCoreApplication.translate("MainWindow", u"Find Next", None))
#if QT_CONFIG(shortcut)
        self.editFindNext.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Right", None))
#endif // QT_CONFIG(shortcut)
        self.editFindPrevious.setText(QCoreApplication.translate("MainWindow", u"Find Previous", None))
#if QT_CONFIG(shortcut)
        self.editFindPrevious.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Left", None))
#endif // QT_CONFIG(shortcut)
        self.editReplace.setText(QCoreApplication.translate("MainWindow", u"Replace", None))
#if QT_CONFIG(shortcut)
        self.editReplace.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+R", None))
#endif // QT_CONFIG(shortcut)
        self.helpAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.compileLaTeX.setText(QCoreApplication.translate("MainWindow", u"LaTeX/TeX", None))
        self.complileTypst.setText(QCoreApplication.translate("MainWindow", u"Typst", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuSelection.setTitle(QCoreApplication.translate("MainWindow", u"Selection", None))
        self.menuFind_and_Replace.setTitle(QCoreApplication.translate("MainWindow", u"Find and Replace", None))
        self.menuCompile.setTitle(QCoreApplication.translate("MainWindow", u"Compile", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

