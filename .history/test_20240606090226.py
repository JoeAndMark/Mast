import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from tempfile import NamedTemporaryFile

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

        # Define absolute paths with file:/// prefix and ensure forward slashes
        base_dir = os.path.dirname(os.path.abspath(__file__))
        katex_css_path = os.path.join(base_dir, "libs/katex/katex.min.css").replace("\\", "/")
        katex_js_path = os.path.join(base_dir, "libs/katex/katex.min.js").replace("\\", "/")
        auto_render_js_path = os.path.join(base_dir, "libs/katex/auto-render.min.js").replace("\\", "/")

        # HTML content with KaTeX rendering
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>KaTeX Example</title>
            <link rel="stylesheet" href="file:///{katex_css_path}">
            <script src="file:///{katex_js_path}"></script>
            <script src="file:///{auto_render_js_path}"></script>
            <script>
                document.addEventListener("DOMContentLoaded", function() {
                    if (typeof renderMathInElement === 'undefined') {
                        console.error('renderMathInElement is not defined');
                    } else {
                        console.log('renderMathInElement is defined');
                        renderMathInElement(document.body, {{
                            delimiters: [
                                {{left: "$$", right: "$$", display: true}},
                                {{left: "$", right: "$", display: false}}
                            ]
                        }});
                    }
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

        # Write the HTML content to a temporary file
        with NamedTemporaryFile('w', delete=False, suffix='.html') as temp_file:
            temp_file.write(html_content)
            temp_file_path = temp_file.name

        # Load the temporary HTML file into QWebEngineView
        self.web_view.setUrl(f'file:///{temp_file_path.replace("\\", "/")}')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
