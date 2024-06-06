from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Echarts in PySide6")
        self.resize(800, 600)

        # 创建 QWebEngineView
        self.webview = QWebEngineView()

        # 创建主窗口的布局
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.webview)

        self.setCentralWidget(central_widget)

        # 加载 Echarts 图表
        self.load_chart()

    def load_chart(self):
        # 准备 HTML 内容
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <script src="file:///E:\Downloads\GitRepo\Github\Python\GUI\PySide\Mast\libs\echarts\echarts.min.js"></script>
        </head>
        <body>
            <div id="main" style="width: 600px;height:400px;"></div>
            <script type="text/javascript">
                var myChart = echarts.init(document.getElementById('main'));
                var option = {
                    title: {
                        text: 'ECharts example'
                    },
                    tooltip: {},
                    legend: {
                        data:['Sales']
                    },
                    xAxis: {
                        data: ["Shirt","Cardign","Chiffon Shirt","Pants","Heels","Socks"]
                    },
                    yAxis: {},
                    series: [{
                        name: 'Sales',
                        type: 'bar',
                        data: [5, 20, 36, 10, 10, 20]
                    }]
                };
                myChart.setOption(option);
            </script>
        </body>
        </html>
        """

        # 在 QWebEngineView 中加载 HTML 内容
        self.webview.setHtml(html_content)

if __name__ == '__main__':
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
