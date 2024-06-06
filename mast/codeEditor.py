from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QFont, QColor, QPainter, QTextFormat
from PySide6.QtWidgets import QWidget, QPlainTextEdit, QApplication, QTextEdit

import sys


class LineNumber(QWidget):
    """
    行号组件，用于显示行号，并高亮当前行
    """
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.editor.blockCountChanged.connect(self.update_width)
        self.editor.updateRequest.connect(self.update_contents)
        self.font = QFont()
        self.numberBarColor = QColor("#e8e8e8")

    def paintEvent(self, event):
        """
        重写paintEvent方法，用于绘制行号
        """
        painter = QPainter(self)
        painter.fillRect(event.rect(), self.numberBarColor)

        block = self.editor.firstVisibleBlock() # 获取当前编辑器中的文本块
        while block.isValid():
            lineNums = block.blockNumber() # 获取当前文本块的总行数
            block_top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
            if not block.isVisible() or block_top >= event.rect().bottom():
                break

            if lineNums == self.editor.textCursor().blockNumber():
                self.font.setBold(True)
                # painter.setPen(QColor("#000000"))
                painter.setPen(QColor('red'))
            else:
                self.font.setBold(False)
                # painter.setPen(QColor("#717171"))
                painter.setPen(QColor('black'))
            painter.setFont(self.font)

            paint_rect = QRect(0, int(block_top), self.width(), self.editor.fontMetrics().height())
            painter.drawText(paint_rect, Qt.AlignRight, str(lineNums + 1))

            block = block.next()

        painter.end()
        super().paintEvent(event)

    def get_width(self):
        count = self.editor.blockCount()
        rect = self.fontMetrics().boundingRect(str(count))
        width = rect.width() + 10
        return width

    def update_width(self):
        width = self.get_width()
        if self.width() != width:
            self.setFixedWidth(width)
            self.editor.setViewportMargins(width, 0, 0, 0)

    def update_contents(self, rect, scroll):
        if scroll:
            self.scroll(0, scroll)
        else:
            self.update(0, rect.y(), self.width(), rect.height())

        if rect.contains(self.editor.viewport().rect()):
            font_size = self.editor.currentCharFormat().font().pointSize()
            self.font.setPointSize(font_size)
            self.update_width()

class QCodeEditor(QPlainTextEdit):
    """
    代码编辑器组件，支持显示行号和高亮当前行
    """
    def __init__(self, display_line_numbers=True, highlight_current_line=True, syntax_high_lighter=None, *args):
        super().__init__()

        self.setFont(QFont("Lucida Console", 11))
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

        self.DISPLAY_LINE_NUMBERS = display_line_numbers
        if display_line_numbers:
            self.number_bar = LineNumber(self)

        if highlight_current_line:
            self.currentLineNumber = None
            self.currentLineColor = self.palette().alternateBase()
            self.cursorPositionChanged.connect(self.highlight_current_line)

        if syntax_high_lighter is not None:
            self.highlighter = syntax_high_lighter(self.document())

    def resizeEvent(self, e):
        if self.DISPLAY_LINE_NUMBERS:
            cr = self.contentsRect()
            rec = QRect(cr.left(), cr.top(), self.number_bar.get_width(), cr.height())
            self.number_bar.setGeometry(rec)
        super().resizeEvent(e)

    def highlight_current_line(self):
        new_current_line_number = self.textCursor().blockNumber()
        if new_current_line_number != self.currentLineNumber:
            self.currentLineNumber = new_current_line_number
            hi_selection = QTextEdit.ExtraSelection()
            hi_selection.format.setBackground(self.currentLineColor)
            hi_selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            hi_selection.cursor = self.textCursor()
            hi_selection.cursor.clearSelection()
            self.setExtraSelections([hi_selection])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = QCodeEditor()
    editor.show()
    sys.exit(app.exec())
