"""
模块名称：makrdownRender.py
模块描述：用来渲染 markdown 文件
作者：JoeAndMark
时间：2024-5-1
"""

# 导入标准库
import os

# 导入第三方库


# 导入自定义库
import markdown

class MarkdownRender:
    def __init__(self):
        pass

    def treeViewDoubleClicked(self):
        """
        目录结构视图下双击文件操作
        """
        filePath = self.model.filePath(self.ui.treeView.currentIndex())
        if os.path.isfile(filePath): # 进行文件操作
            self._notSaveWarning()
            self.fileOpen(filePath)

    def loadCustomCSS(self):
        """
        加载自定义 CSS 文件内容
        """
        css_path = "./mast/resources/themes/default.css"
        if os.path.exists(css_path):
            with open(css_path, "r") as file:
                self.customCSS = file.read()
        else:
            self.customCSS = ""

    def applyTemplate(self, html):
        """
        将 HTML 内容插入模板
        """
        with open("./mast/resources/templates/template.html", "r") as file:
            template = file.read()

        # 添加自定义 CSS 到模板中的 <style> 标签
        template = template.replace("/* Add custom CSS here */", self.customCSS)

        # 插入渲染后的 HTML 内容
        return template.replace("{content}", html)

    def renderMarkdown(self):
        """
        渲染 Markdown
        """
        # 使用的扩展缩写
        abbr = [
            'extra', # 扩展语法，用来处理汉字
            'codehilite', # 代码高亮
            'toc', # 生成目录
            'tables', # 表格
            'fenced_code', # 代码块
            'footnotes', # 脚注
            'attr_list', # 允许在块级元素和内联元素上添加属性
            'nl2br', # 将换行符转换为 <br> 标签
            'sane_lists' # 改进列表处理
        ]

        extensions = [
            f'markdown.extensions.{ext}' for ext in abbr
        ]

        content = self.ui.textEdit.toPlainText()
        html = markdown(content, extensions=extensions)
        self.ui.webEngineView.setHtml(self.applyTemplate(html))
