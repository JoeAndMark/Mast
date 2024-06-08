# `mast` 库描述

## 文件结构

```bash
Mast:.
|   codeEditor.py
|   convertUi.py
|   gui.py
|   g.ui
|   highlighter.py
|   main.py
|   markdownRender.py
|   pdfPreview.py
|   README.md
|   utils.py
|   __init__.py
|
+---resources
|   +---icons
|   |       mast.ico
|   |       mast.svg
|   +---styles
|   +---templates
|   |       template.html
|   \---themes
|           default.css
```

## 文件描述

+ `codeEditor.py`：自定义代码编辑器组件，目的现显示行号和高亮当前行的功能，暂未实现。

+ `convertUi.py`：将同目录下的所有 `.ui` 文件自动转换为 `.py` 文件，可以批量进行转换。

+ `gui.py`：由 `convertUi.py` 自动转换而来，不应该被手动修改。

+ `g.ui`：本项目的 GUI 设计文件，由 `QtDesigner` 自动生成，不应该被手动修改。

+ `highlighter.py`：原 `highlighter` 库的实现，现将其整合到 `mast` 库中。

+ `main.py`：本项目的 GUI 操作逻辑实现文件。

+ `markdownRender.py`：实现 Markdown 的实时预览，主要是实现 Markdown 转 HTML 的操作逻辑。

+ `pdfPreview.py`：`mast` 将来会支持 LaTeX 和 Typst，本模块将实现编译后预览 PDF 的功能（包括正方向跳转），暂未实现。

+ `utils.py`：本项目的通用模块，主要实现 GUI 的菜单栏的所有功能，以及提供 API。（说不定这个项目哪一天就火了，编写插件什么的需要提供 API）

+ `resources`：本项目的资源文件夹，主要用来存放软件图标以及用于 Markdown 渲染的 CSS 等。
  
  + `icons`：用于存放软件图标
  
  + `styles`：存放 GUI 主题文件
  
  + `templates`：存放模版文件，为实现 KaTeX 等的渲染。
  
  + `themes`：Markdown 渲染所用的 CSS 样式。
  
  


