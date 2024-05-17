from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont, QBrush, QPalette, QTextCursor, QTextLayout
import re

class LaTeXHighlighter(QSyntaxHighlighter):

    LATEX_KEYS_REGEX = {
        'Command': re.compile(r'\\[a-zA-Z]+'),
        'Environment': re.compile(r'\\begin\{.*?\}|\\end\{.*?\}'),
        'Math': re.compile(r'\$.*?\$|\\\(.+?\\\)|\\\[.+?\\\]'),
        'Comment': re.compile(r'%.*'),
        'Bold': re.compile(r'\\textbf\{.*?\}'),
        'Italic': re.compile(r'\\textit\{.*?\}'),
    }

    def __init__(self, document):
        super().__init__(document)
        self.formats = self.init_formats()

    def init_formats(self):
        formats = {}
        formats['Command'] = QTextCharFormat()
        formats['Command'].setForeground(QBrush(QColor('#0000FF')))
        formats['Environment'] = QTextCharFormat()
        formats['Environment'].setForeground(QBrush(QColor('#008000')))
        formats['Math'] = QTextCharFormat()
        formats['Math'].setForeground(QBrush(QColor('#FF0000')))
        formats['Comment'] = QTextCharFormat()
        formats['Comment'].setForeground(QBrush(QColor('#808080')))
        formats['Bold'] = QTextCharFormat()
        formats['Bold'].setFontWeight(QFont.Bold)
        formats['Italic'] = QTextCharFormat()
        formats['Italic'].setFontItalic(True)
        return formats

    def highlightBlock(self, text):
        for key, regex in self.LATEX_KEYS_REGEX.items():
            for match in regex.finditer(text):
                start, end = match.span()
                self.setFormat(start, end - start, self.formats[key])
