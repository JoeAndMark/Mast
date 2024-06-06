import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Set up the main window
        self.setWindowTitle("KaTeX Renderer")
        self.setGeometry(200, 200, 800, 600)

        # Create a central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Create a QWebEngineView instance
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        # Define relative paths
        katex_css_path = "libs/katex/katex.min.css"
        katex_js_path = "libs/katex/katex.min.js"
        auto_render_js_path = "libs/katex/auto-render.min.js"

        # HTML content with KaTeX rendering
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>KaTeX Example</title>
            <link rel="stylesheet" href="{katex_css_path}">
            <script src="{katex_js_path}"></script>
            <script src="{auto_render_js_path}"></script>
            <script>
                document.addEventListener("DOMContentLoaded", function() {
                    renderMathInElement(document.body, {{
                        delimiters: [
                            {{left: "$$", right: "$$", display: true}},
                            {{left: "$", right: "$", display: false}}
                        ]
                    }});
                });
            </script>
        </head>
        <body>
            <h1>KaTeX Rendering Example</h1>
            <p>This is an inline formula: $E = mc^2$</p>
            <p>This is a block formula: $$\\int_0^\\infty x^2 dx$$</p>
        </body>
        </html>
        """

        # Set the HTML content to the QWebEngineView
        self.web_view.setHtml(html_content)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
