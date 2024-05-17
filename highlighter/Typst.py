from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont, QBrush, QPalette, QTextCursor, QTextLayout
import re

class TypstHighlighter(QSyntaxHighlighter):

    TYPST_KEYS_REGEX = {
        'Function': re.compile(r'@.+?\{.*?\}'),
        'Bold': re.compile(r'\*\*.*?\*\*'),
        'Italic': re.compile(r'\*.*?\*'),
        'InlineMath': re.compile(r'\$.+?\$'),
        'BlockMath': re.compile(r'\$\$.+?\$\$'),
        'Comment': re.compile(r'//.*'),
    }

    def __init__(self, document):
        super().__init__(document)
        self.formats = self.init_formats()

    def init_formats(self):
        formats = {}
        formats['Function'] = QTextCharFormat()
        formats['Function'].setForeground(QBrush(QColor('#0000FF')))
        formats['Bold'] = QTextCharFormat()
        formats['Bold'].setFontWeight(QFont.Bold)
        formats['Italic'] = QTextCharFormat()
        formats['Italic'].setFontItalic(True)
        formats['InlineMath'] = QTextCharFormat()
        formats['InlineMath'].setForeground(QBrush(QColor('#FF0000')))
        formats['BlockMath'] = QTextCharFormat()
        formats['BlockMath'].setForeground(QBrush(QColor('#FF0000')))
        formats['Comment'] = QTextCharFormat()
        formats['Comment'].setForeground(QBrush(QColor('#808080')))
        return formats

    def highlightBlock(self, text):
        for key, regex in self.TYPST_KEYS_REGEX.items():
            for match in regex.finditer(text):
                start, end = match.span()
                self.setFormat(start, end - start, self.formats[key])
