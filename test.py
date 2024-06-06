import os
import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import re
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
import sys

class EChartsExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(EChartsPreprocessor(md), 'echarts', 175)

class EChartsPreprocessor(Preprocessor):
    ECHARTS_RE = re.compile(r'```echarts\s+(.*?)\s+```', re.DOTALL)

    def run(self, lines):
        text = "\n".join(lines)
        while True:
            m = self.ECHARTS_RE.search(text)
            if not m:
                break
            chart_code = m.group(1)
            chart_id = f"echarts_{hash(chart_code)}"
            chart_div = f'<div id="{chart_id}" style="width: 600px; height: 400px;"></div>'
            chart_script = f'''
            <script type="text/javascript">
                var chart = echarts.init(document.getElementById('{chart_id}'));
                var option = {chart_code};
                chart.setOption(option);
            </script>
            '''
            replacement = chart_div + chart_script
            text = text[:m.start()] + replacement + text[m.end():]
        return text.split("\n")

def markdown_to_html(md_text):
    md = markdown.Markdown(extensions=[EChartsExtension()])
    return md.convert(md_text)

class MainWindow(QMainWindow):
    def __init__(self, html_content):
        super().__init__()
        self.setWindowTitle('ECharts Example')

        # Create QWebEngineView
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        # Load HTML content
        self.browser.setHtml(html_content)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Read the markdown content
    with open('example.md', 'r', encoding='utf-8') as file:
        md_content = file.read()

    # Convert markdown to HTML with ECharts
    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>ECharts Example</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/echarts/5.2.1/echarts.min.js"></script>
    </head>
    <body>
        {markdown_to_html(md_content)}
    </body>
    </html>
    '''

    # Create and show the main window
    window = MainWindow(html_content)
    window.show()

    sys.exit(app.exec())
