"""
模块名称：highlighter.py
模块描述：代码编辑区，即文本框，实现语法高亮功能
作者：JoeAndMark
时间：2024-5-1
其他：MarkdownHighlighter 基于项目 https://github.com/rupeshk/MarkdownHighlighter 修改而来，感谢大佬！
"""

# 导入标准库
import re

# 导入第三方库
from PySide6.QtGui import QBrush, QSyntaxHighlighter, QTextCharFormat, QColor, QPalette, QFont, QTextCursor, QTextLayout
from PySide6.QtWidgets import QTextEdit

# 导入自定义库


class MarkdownHighlighter(QSyntaxHighlighter):

    MARKDOWN_KEYS_REGEX = {
        'Bold' : re.compile(u'(?P<delim>\*\*)(?P<text>.+)(?P=delim)'),
        'uBold': re.compile(u'(?P<delim>__)(?P<text>[^_]{2,})(?P=delim)'),
        'Italic': re.compile(u'(?P<delim>\*)(?P<text>[^*]{2,})(?P=delim)'),
        'uItalic': re.compile(u'(?P<delim>_)(?P<text>[^_]+)(?P=delim)'),
        'Link': re.compile(u'(?u)(^|(?P<pre>[^!]))\[.*?\]:?[ \t]*\(?[^)]+\)?'),
        'Image': re.compile(u'(?u)!\[.*?\]\(.+?\)'),
        'HeaderAtx': re.compile(u'(?u)^\#{1,6}(.*?)\#*(\n|$)'),
        'Header': re.compile(u'^(.+)[ \t]*\n(=+|-+)[ \t]*\n+'),
        'CodeBlock': re.compile(u'^([ ]{4,}|\t).*'),
        'UnorderedList': re.compile(u'(?u)^\s*(\* |\+ |- )+\s*'),
        'UnorderedListStar': re.compile(u'^\s*(\* )+\s*'),
        'OrderedList': re.compile(u'(?u)^\s*(\d+\. )\s*'),
        'BlockQuote': re.compile(u'(?u)^\s*>+\s*'),
        'BlockQuoteCount': re.compile(u'^[ \t]*>[ \t]?'),
        'CodeSpan': re.compile(u'(?P<delim>`+).+?(?P=delim)'),
        'HR': re.compile(u'(?u)^(\s*(\*|-)\s*){3,}$'),
        'eHR': re.compile(u'(?u)^(\s*(\*|=)\s*){3,}$'),
        'Html': re.compile(u'<.+?>')
    }

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.setTabStopDistance(self.parent.fontMetrics().horizontalAdvance(' ') * 8)

        self.defaultTheme = {
            "background-color": "white",
            "color": "#191970",
            "bold": {"color": "#859900", "font-weight": "bold", "font-style": "normal"},
            "emphasis": {"color": "#b58900", "font-weight": "bold", "font-style": "italic"},
            "link": {"color": "#cb4b16", "font-weight": "normal", "font-style": "normal"},
            "image": {"color": "#cb4b16", "font-weight": "normal", "font-style": "normal"},
            "header": {"color": "#2aa198", "font-weight": "bold", "font-style": "normal"},
            "unorderedlist": {"color": "#dc322f", "font-weight": "normal", "font-style": "normal"},
            "orderedlist": {"color": "#dc322f", "font-weight": "normal", "font-style": "normal"},
            "blockquote": {"color": "#dc322f", "font-weight": "normal", "font-style": "normal"},
            "codespan": {"color": "#dc322f", "font-weight": "normal", "font-style": "normal"},
            "codeblock": {"color": "#ff9900", "font-weight": "normal", "font-style": "normal"},
            "line": {"color": "#2aa198", "font-weight": "normal", "font-style": "normal"},
            "html": {"color": "#c000c0", "font-weight": "normal", "font-style": "normal"}
        }
        self.setTheme(self.defaultTheme)

    def setTheme(self, theme):
        self.theme = theme
        self.MARKDOWN_KWS_FORMAT = {}

        pal = self.parent.palette()
        pal.setColor(QPalette.Base, QColor(theme['background-color']))
        self.parent.setPalette(pal)
        self.parent.setTextColor(QColor(theme['color']))

        format = QTextCharFormat()
        format.setForeground(QBrush(QColor(theme['bold']['color'])))
        format.setFontWeight(QFont.Bold if theme['bold']['font-weight'] == 'bold' else QFont.Normal)
        format.setFontItalic(True if theme['bold']['font-style'] == 'italic' else False)
        self.MARKDOWN_KWS_FORMAT['Bold'] = format

        format = QTextCharFormat()
        format.setForeground(QBrush(QColor(theme['bold']['color'])))
        format.setFontWeight(QFont.Bold if theme['bold']['font-weight'] == 'bold' else QFont.Normal)
        format.setFontItalic(True if theme['bold']['font-style'] == 'italic' else False)
        self.MARKDOWN_KWS_FORMAT['uBold'] = format

        format = QTextCharFormat()
        format.setForeground(QBrush(QColor(theme['emphasis']['color'])))
        format.setFontWeight(QFont.Bold if theme['emphasis']['font-weight'] == 'bold' else QFont.Normal)
        format.setFontItalic(True if theme['emphasis']['font-style'] == 'italic' else False)
        self.MARKDOWN_KWS_FORMAT['Italic'] = format

        format = QTextCharFormat()
        format.setForeground(QBrush(QColor(theme['emphasis']['color'])))
        format.setFontWeight(QFont.Bold if theme['emphasis']['font-weight'] == 'bold' else QFont.Normal)
        format.setFontItalic(True if theme['emphasis']['font-style'] == 'italic' else False)
        self.MARKDOWN_KWS_FORMAT['uItalic'] = format

        format = QTextCharFormat()
        format.setForeground(QBrush(QColor(theme['link']['color'])))
        format.setFontWeight(QFont.Bold if theme['link']['font-weight'] == 'bold' else QFont.Normal)
        format.setFontItalic(True if theme['link']['font-style'] == 'italic' else False)
        self.MARKDOWN_KWS_FORMAT['Link'] = format

        format = QTextCharFormat()
        format.setForeground(QBrush(QColor(theme['image']['color'])))
        format.setFontWeight(QFont.Bold if theme['image']['font-weight'] == 'bold' else QFont.Normal)
        format.setFontItalic(True if theme['image']['font-style'] == 'italic' else False)
        self.MARKDOWN_KWS_FORMAT['Image'] = format

        format = QTextCharFormat()
        format.setForeground(QBrush(QColor(theme['header']['color'])))
        format.setFontWeight(QFont.Bold if theme['header']['font-weight'] == 'bold' else QFont.Normal)
        format.setFontItalic(True if theme['header']['font-style'] == 'italic' else False)
        self.MARKDOWN_KWS_FORMAT['Header'] = format

        format = QTextCharFormat()
        format.setForeground(QBrush(QColor(theme['header']['color'])))
        format.setFontWeight(QFont.Bold if theme['header']['font-weight'] == 'bold' else QFont.Normal)
        format.setFontItalic(True if theme['header']['font-style'] == 'italic' else False)
        self.MARKDOWN_KWS_FORMAT['HeaderAtx'] = format

        format = QTextCharFormat()
        format.setForeground(QBrush(QColor(theme['unorderedlist']['color'])))
        format.setFontWeight(QFont.Bold if theme['unorderedlist']['font-weight'] == 'bold' else QFont.Normal)
        format.setFontItalic(True if theme['unorderedlist']['font-style'] == 'italic' else False)
        self.MARKDOWN_KWS_FORMAT['UnorderedList'] = format

        format = QTextCharFormat()
        format.setForeground(QBrush(QColor(theme['orderedlist']['color'])))
        format.setFontWeight(QFont.Bold if theme['orderedlist']['font-weight'] == 'bold' else QFont.Normal)
        format.setFontItalic(True if theme['orderedlist']['font-style'] == 'italic' else False)
        self.MARKDOWN_KWS_FORMAT['OrderedList'] = format

        format = QTextCharFormat()
        format.setForeground(QBrush(QColor(theme['blockquote']['color'])))
        format.setFontWeight(QFont.Bold if theme['blockquote']['font-weight'] == 'bold' else QFont.Normal)
        format.setFontItalic(True if theme['blockquote']['font-style'] == 'italic' else False)
        self.MARKDOWN_KWS_FORMAT['BlockQuote'] = format

        format = QTextCharFormat()
        format.setForeground(QBrush(QColor(theme['codespan']['color'])))
        format.setFontWeight(QFont.Bold if theme['codespan']['font-weight'] == 'bold' else QFont.Normal)
        format.setFontItalic(True if theme['codespan']['font-style'] == 'italic' else False)
        self.MARKDOWN_KWS_FORMAT['CodeSpan'] = format

        format = QTextCharFormat()
        format.setForeground(QBrush(QColor(theme['codeblock']['color'])))
        format.setFontWeight(QFont.Bold if theme['codeblock']['font-weight'] == 'bold' else QFont.Normal)
        format.setFontItalic(True if theme['codeblock']['font-style'] == 'italic' else False)
        self.MARKDOWN_KWS_FORMAT['CodeBlock'] = format

        format = QTextCharFormat()
        format.setForeground(QBrush(QColor(theme['line']['color'])))
        format.setFontWeight(QFont.Bold if theme['line']['font-weight'] == 'bold' else QFont.Normal)
        format.setFontItalic(True if theme['line']['font-style'] == 'italic' else False)
        self.MARKDOWN_KWS_FORMAT['HR'] = format

        format = QTextCharFormat()
        format.setForeground(QBrush(QColor(theme['line']['color'])))
        format.setFontWeight(QFont.Bold if theme['line']['font-weight'] == 'bold' else QFont.Normal)
        format.setFontItalic(True if theme['line']['font-style'] == 'italic' else False)
        self.MARKDOWN_KWS_FORMAT['eHR'] = format

        format = QTextCharFormat()
        format.setForeground(QBrush(QColor(theme['html']['color'])))
        format.setFontWeight(QFont.Bold if theme['html']['font-weight'] == 'bold' else QFont.Normal)
        format.setFontItalic(True if theme['html']['font-style'] == 'italic' else False)
        self.MARKDOWN_KWS_FORMAT['HTML'] = format

        self.rehighlight()

    def highlightBlock(self, text):
        text = str(text)
        self.highlightMarkdown(text, 0)
        self.highlightHtml(text)

    def highlightMarkdown(self, text, strt):
        cursor = QTextCursor(self.document())
        bf = cursor.blockFormat()
        self.setFormat(0, len(text), QColor(self.theme['color']))

        self.highlightBlockQuote(text, cursor, bf, strt)

        if self.highlightEmptyLine(text, cursor, bf, strt):
            return

        if self.highlightHorizontalLine(text, cursor, bf, strt):
            return

        if self.highlightAtxHeader(text, cursor, bf, strt):
            return

        self.highlightList(text, cursor, bf, strt)

        self.highlightLink(text, cursor, bf, strt)

        self.highlightImage(text, cursor, bf, strt)

        self.highlightCodeSpan(text, cursor, bf, strt)

        self.highlightEmphasis(text, cursor, bf, strt)

        self.highlightBold(text, cursor, bf, strt)

        self.highlightCodeBlock(text, cursor, bf, strt)

    def highlightBlockQuote(self, text, cursor, bf, strt):
        found = False
        mo = re.search(self.MARKDOWN_KEYS_REGEX['BlockQuote'], text)
        if mo:
            self.setFormat(mo.start(), mo.end() - mo.start(), self.MARKDOWN_KWS_FORMAT['BlockQuote'])
            unquote = re.sub(self.MARKDOWN_KEYS_REGEX['BlockQuoteCount'], '', text)
            spcs = re.match(self.MARKDOWN_KEYS_REGEX['BlockQuoteCount'], text)
            spcslen = 0
            if spcs:
                spcslen = len(spcs.group(0))
            self.highlightMarkdown(unquote, spcslen)
            found = True
        return found

    def highlightEmptyLine(self, text, cursor, bf, strt):
        textAscii = str(text.replace(u'\u2029', '\n'))
        if textAscii.strip():
            return False
        else:
            return True

    def highlightHorizontalLine(self, text, cursor, bf, strt):
        found = False
        for mo in re.finditer(self.MARKDOWN_KEYS_REGEX['HR'], text):
            prevBlock = self.currentBlock().previous()
            prevCursor = QTextCursor(prevBlock)
            prev = prevBlock.text()
            prevAscii = str(prev.replace(u'\u2029', '\n'))
            if prevAscii.strip():
                prevCursor.select(QTextCursor.LineUnderCursor)
                formatRange = QTextLayout.FormatRange()
                formatRange.format = self.MARKDOWN_KWS_FORMAT['Header']
                formatRange.length = prevCursor.block().length()
                formatRange.start = 0
                prevCursor.block().layout().setAdditionalFormats([formatRange])
            self.setFormat(mo.start() + strt, mo.end() - mo.start(), self.MARKDOWN_KWS_FORMAT['HR'])

        for mo in re.finditer(self.MARKDOWN_KEYS_REGEX['eHR'], text):
            prevBlock = self.currentBlock().previous()
            prevCursor = QTextCursor(prevBlock)
            prev = prevBlock.text()
            prevAscii = str(prev.replace(u'\u2029', '\n'))
            if prevAscii.strip():
                prevCursor.select(QTextCursor.LineUnderCursor)
                formatRange = QTextLayout.FormatRange()
                formatRange.format = self.MARKDOWN_KWS_FORMAT['Header']
                formatRange.length = prevCursor.block().length()
                formatRange.start = 0
                prevCursor.block().layout().setAdditionalFormats([formatRange])
            self.setFormat(mo.start() + strt, mo.end() - mo.start(), self.MARKDOWN_KWS_FORMAT['HR'])
        return found

    def highlightAtxHeader(self, text, cursor, bf, strt):
        found = False
        for mo in re.finditer(self.MARKDOWN_KEYS_REGEX['HeaderAtx'], text):
            self.setFormat(mo.start() + strt, mo.end() - mo.start(), self.MARKDOWN_KWS_FORMAT['HeaderAtx'])
            found = True
        return found

    def highlightList(self, text, cursor, bf, strt):
        found = False
        for mo in re.finditer(self.MARKDOWN_KEYS_REGEX['UnorderedList'], text):
            self.setFormat(mo.start() + strt, mo.end() - mo.start() - strt, self.MARKDOWN_KWS_FORMAT['UnorderedList'])
            found = True

        for mo in re.finditer(self.MARKDOWN_KEYS_REGEX['OrderedList'], text):
            self.setFormat(mo.start() + strt, mo.end() - mo.start() - strt, self.MARKDOWN_KWS_FORMAT['OrderedList'])
            found = True
        return found

    def highlightLink(self, text, cursor, bf, strt):
        found = False
        for mo in re.finditer(self.MARKDOWN_KEYS_REGEX['Link'], text):
            self.setFormat(mo.start() + strt, mo.end() - mo.start() - strt, self.MARKDOWN_KWS_FORMAT['Link'])
            found = True
        return found

    def highlightImage(self, text, cursor, bf, strt):
        found = False
        for mo in re.finditer(self.MARKDOWN_KEYS_REGEX['Image'], text):
            self.setFormat(mo.start() + strt, mo.end() - mo.start() - strt, self.MARKDOWN_KWS_FORMAT['Image'])
            found = True
        return found

    def highlightCodeSpan(self, text, cursor, bf, strt):
        found = False
        for mo in re.finditer(self.MARKDOWN_KEYS_REGEX['CodeSpan'], text):
            self.setFormat(mo.start() + strt, mo.end() - mo.start() - strt, self.MARKDOWN_KWS_FORMAT['CodeSpan'])
            found = True
        return found

    def highlightBold(self, text, cursor, bf, strt):
        found = False
        for mo in re.finditer(self.MARKDOWN_KEYS_REGEX['Bold'], text):
            self.setFormat(mo.start() + strt, mo.end() - mo.start() - strt, self.MARKDOWN_KWS_FORMAT['Bold'])
            found = True

        for mo in re.finditer(self.MARKDOWN_KEYS_REGEX['uBold'], text):
            self.setFormat(mo.start() + strt, mo.end() - mo.start() - strt, self.MARKDOWN_KWS_FORMAT['uBold'])
            found = True
        return found

    def highlightEmphasis(self, text, cursor, bf, strt):
        found = False
        unlist = re.sub(self.MARKDOWN_KEYS_REGEX['UnorderedListStar'], '', text)
        spcs = re.match(self.MARKDOWN_KEYS_REGEX['UnorderedListStar'], text)
        spcslen = 0
        if spcs:
            spcslen = len(spcs.group(0))
        for mo in re.finditer(self.MARKDOWN_KEYS_REGEX['Italic'], unlist):
            self.setFormat(mo.start() + strt + spcslen, mo.end() - mo.start() - strt, self.MARKDOWN_KWS_FORMAT['Italic'])
            found = True
        for mo in re.finditer(self.MARKDOWN_KEYS_REGEX['uItalic'], text):
            self.setFormat(mo.start() + strt, mo.end() - mo.start() - strt, self.MARKDOWN_KWS_FORMAT['uItalic'])
            found = True
        return found

    def highlightCodeBlock(self, text, cursor, bf, strt):
        found = False
        for mo in re.finditer(self.MARKDOWN_KEYS_REGEX['CodeBlock'], text):
            stripped = text.lstrip()
            if stripped[0] not in ('*', '-', '+', '>'):
                self.setFormat(mo.start() + strt, mo.end() - mo.start(), self.MARKDOWN_KWS_FORMAT['CodeBlock'])
                found = True
        return found

    def highlightHtml(self, text):
        for mo in re.finditer(self.MARKDOWN_KEYS_REGEX['Html'], text):
            self.setFormat(mo.start(), mo.end() - mo.start(), self.MARKDOWN_KWS_FORMAT['HTML'])


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
