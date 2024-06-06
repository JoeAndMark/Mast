from PyQt5.QtWidgets import (QGraphicsProxyWidget, QMainWindow,
                             QGraphicsView, QGraphicsScene,
                             QGraphicsObject, QGraphicsItem, QWidget,
                             QHBoxLayout, QApplication)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QBrush
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys

class A(QGraphicsObject):
   def __init__(self, url=None):
      super().__init__()
      self.web_view = QWebEngineView()
      if url is None:
         url = QUrl(url)
         self.web_view.load(url)
      self.proxy = QGraphicsProxyWidget(parent=self)
      self.proxy.setWidget(self.web_view)
      self.web_view.show()
      
   def boundingRect(self):
      return self.childrenBoundingRect()
   
   def paint(self, painter, option, widget):
      pass

if __name__ == '__main__':
   app = QApplication([])
   
   window = QMainWindow()
   window.show()
   view = QGraphicsView()
   scene = QGraphicsScene()
   scene.setBackgroundBrush(QBrush(Qt.gray))
   view.setScene(scene)
   html = '''
   <!DOCTYPE html>
   <!-- KaTeX requires the use of the HTML5 doctype. Without it, KaTeX may not render properly -->
   <html>
       <head>
           <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.10.0-rc.1/dist/katex.min.css" integrity="sha384-D+9gmBxUQogRLqvARvNLmA9hS2x//eK1FhVb9PiU86gmcrBrJAQT8okdJ4LMp2uv" crossorigin="anonymous">
   
           <!-- The loading of KaTeX is deferred to speed up page rendering -->
           <script src="https://cdn.jsdelivr.net/npm/katex@0.10.0-rc.1/dist/katex.min.js" integrity="sha384-483A6DwYfKeDa0Q52fJmxFXkcPCFfnXMoXblOkJ4JcA8zATN6Tm78UNL72AKk+0O" crossorigin="anonymous"></script>
   
           <!-- To automatically render math in text elements, include the auto-render extension: -->
           <script defer src="https://cdn.jsdelivr.net/npm/katex@0.10.0-rc.1/dist/contrib/auto-render.min.js" integrity="sha384-yACMu8JWxKzSp/C1YV86pzGiQ/l1YUfE8oPuahJQxzehAjEt2GiQuy/BIvl9KyeF" crossorigin="anonymous"
           onload="renderMathInElement(document.body);"></script>
       </head>
       <body>
   
           <p id="IdentificatorForElement"></p>
   
           <script>
               katex.render("C", document.getElementById('IdentificatorForElement'), '
                   throwOnError: false
               });
           </script>
       </body>
   </html>
   '''
   #a = A("http://www.google.com")
   a = A()
   a.web_view.setHtml(html)
   scene.addItem(a)
   window.setCentralWidget(view)
   a.web_view.renderProcessTerminated.connect(a.update)   
   sys.exit(app.exec_())
