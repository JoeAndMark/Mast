import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
from markdown import markdown
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.codehilite import CodeHiliteExtension

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Markdown Editor')
        self.setGeometry(100, 100, 800, 600)

        self.editor = QTextEdit(self)
        self.preview = QTextEdit(self)
        self.preview.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.editor)
        layout.addWidget(self.preview)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.editor.textChanged.connect(self.update_preview)

    def update_preview(self):
        text = self.editor.toPlainText()
        html_content = markdown(text, extensions=[FencedCodeExtension(), CodeHiliteExtension(linenums=False)])
        html = self.render_template('template.html', content=html_content)
        self.preview.setHtml(html)

    def render_template(self, template_name, **context):
        with open(template_name, 'r', encoding='utf-8') as file:
            template = file.read()
        return template.replace('{{ content | safe }}', context.get('content', ''))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
