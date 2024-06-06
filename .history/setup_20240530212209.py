from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QFont, QColor, QPainter
from PyQt5.QtWidgets import QWidget
class LineNumberArea(QWidget):
    def __init__(self, editor):
        QWidget.__init__(self, editor)
        self.editor = editor
        self.editor.blockCountChanged.connect(self.update_width)
        self.editor.updateRequest.connect(self.update_contents)
        self.font = QFont()
        self.numberBarColor = QColor("#e8e8e8")

    def paintEvent(self, event):
        # Override paintEvent to draw the line numbers
        painter = QPainter(self)
        painter.fillRect(event.rect(), self.numberBarColor)

        block = self.editor.firstVisibleBlock()

        # Iterate over all visible text blocks in the document.
        while block.isValid():
            block_number = block.blockNumber()
            block_top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()

            # Check if the position of the block is outside the visible area.
            if not block.isVisible() or block_top >= event.rect().bottom():
                break

            # We want the line number for the selected line to be bold.
            if block_number == self.editor.textCursor().blockNumber():
                self.font.setBold(True)
                painter.setPen(QColor("#000000"))
            else:
                self.font.setBold(False)
                painter.setPen(QColor("#717171"))
            painter.setFont(self.font)

            # Draw the line number right justified at the position of the line.
            paint_rect = QRect(0, int(block_top), self.width(), self.editor.fontMetrics().height())
            painter.drawText(paint_rect, Qt.AlignRight, str(block_number + 1))

            block = block.next()

        painter.end()

        QWidget.paintEvent(self, event)

    # 根据文档的总行数来计算宽度
    def get_width(self):
        count = self.editor.blockCount()
        width = self.fontMetrics().width(str(count)) + 10
        return width

    # 设置宽度
    def update_width(self):
        width = self.get_width()
        if self.width() != width:
            self.setFixedWidth(width)
            self.editor.setViewportMargins(width, 0, 0, 0);

    # 更行内容
    def update_contents(self, rect, scroll):
        if scroll:
            self.scroll(0, scroll)
        else:
            self.update(0, rect.y(), self.width(), rect.height())

        if rect.contains(self.editor.viewport().rect()):
            font_size = self.editor.currentCharFormat().font().pointSize()
            self.font.setPointSize(font_size)
            self.font.setStyle(QFont.StyleNormal)
            self.update_width()

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QFont,  QTextFormat
from PyQt5.QtWidgets import QPlainTextEdit, QTextEdit
class QCodeEditor(QPlainTextEdit):
    def __init__(self, display_line_numbers=True, highlight_current_line=True,
                 syntax_high_lighter=None, *args):
        """
        Parameters
        ----------
        display_line_numbers : bool
            switch on/off the presence of the lines number bar
        highlight_current_line : bool
            switch on/off the current line highlighting
        syntax_high_lighter : QSyntaxHighlighter
            should be inherited from QSyntaxHighlighter

        """
        super(QCodeEditor, self).__init__()

        self.setFont(QFont("Microsoft YaHei UI Light", 11))
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

        self.DISPLAY_LINE_NUMBERS = display_line_numbers

        if display_line_numbers:
            self.number_bar = self.LineNumberArea(self)

        if highlight_current_line:
            self.currentLineNumber = None
            self.currentLineColor = self.palette().alternateBase()
            # self.currentLineColor = QColor("#e8e8e8")
            self.cursorPositionChanged.connect(self.highlight_current_line)

        if syntax_high_lighter is not None:  # add highlighter to text document
            self.highlighter = syntax_high_lighter(self.document())

    def resizeEvent(self, *e):
        """overload resizeEvent handler"""

        if self.DISPLAY_LINE_NUMBERS:  # resize LineNumberArea widget
            cr = self.contentsRect()
            rec = QRect(cr.left(), cr.top(), self.number_bar.get_width(), cr.height())
            self.number_bar.setGeometry(rec)

        QPlainTextEdit.resizeEvent(self, *e)

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


if __name
