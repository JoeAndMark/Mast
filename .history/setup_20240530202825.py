# Python
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from markdown2 import markdown

class MarkdownEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.textEdit = QTextEdit(self)
        self.textEdit.setPlainText("# Example\n\nThis is a **Markdown** editor with KaTeX support.\n\n$$E = mc^2$$")
        self.textEdit.textChanged.connect(self.update_preview)

        self.webView = QWebEngineView(self)

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.webView)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Markdown Editor with KaTeX')

        self.update_preview()
        self.show()

    def update_preview(self):
        text = self.textEdit.toPlainText()
        html = markdown(text)
        html = self.wrap_with_katex(html)
        self.webView.setHtml(html)

    def wrap_with_katex(self, html):
        katex_header = """
        <link rel="stylesheet" href="libs/katex/katex.min.css">
        <script defer src="libs/katex/katex.min.js"></script>
        <script defer src="libs/katex/auto-render.min.js"></script>
        <script>
            document.addEventListener("DOMContentLoaded", function() {
                renderMathInElement(document.body, {
                    delimiters: [
                        {left: "$$", right: "$$", display: true},
                        {left: "\\(", right: "\\)", display: false}
                    ]
                });
            });
        </script>
        """
        return f"""
        <html>
        <head>{katex_header}</head>
        <body>{html}</body>
        </html>
        """

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MarkdownEditor()
    sys.exit(app.exec_())
