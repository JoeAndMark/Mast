# API 文档

## 描述

`mast` 库向外提供的 API 位于 `mast` 库中的 `utils.py` 模块。该模块包含了多种实用功能，包括文件处理、编辑框中的文本处理、帮助系统等。

这些 API 旨在简化开发者的插件实现流程，使得插件开发更加高效和便捷。

通过提供统一和简洁的接口，`utils.py` 模块能够满足不同插件在处理文件、操作文本和提供用户帮助等方面的需求。

无论是处理复杂的文件操作，还是对编辑框中的文本进行精细化处理，亦或是集成和调用帮助系统，这些 API 都能为开发者提供强有力的支持，从而提高插件的开发效率和质量。

## 命名约定

本项目所有代码遵循以下命名约定：

+ 类的命名使用**大驼峰命名法**
+ 函数、方法和变量的命名使用**小驼峰命名法**
+ 私有方法和私有属性以单下划线 `_` 开头
+ 所有 `handler` 类的方法以相应**前缀**开头，如与 `FileHandler` 有关的方法 `fileOpen`、`fileNew`、`fileSave` 等

## 如何使用

1. 导入对应模块：

```python
from mast import utils
```

2. 实例化：

```python
handler = utils.FileHandler()
```

```python
handler = utils.CompileHandler()
```

```python
handler = utils.HelpHandler()
```

## 类及其方法说明

### 1. `FileHandler` 类

#### 描述
`FileHandler` 类提供了处理文件相关的操作，包括文件的打开、保存、另存为、新建文件、移动文件等功能。

#### 初始化方法
```python
def __init__(self, textEdit, statusBar=None)
```
- `textEdit`: 文本编辑控件
- `statusBar` (可选): 状态栏控件

#### 方法

##### `readFile`
读取当前文件的内容。

```python
def readFile(self)
```
- **返回**: 文件内容

##### `fileOpen`
打开文件。

```python
def fileOpen(self)
```
- **返回**: 打开文件的路径和状态

##### `fileNew`
创建新文件，并清空文本框中的内容。

```python
def fileNew(self, textEdit, statusBar=None)
```
- `textEdit`: 文本编辑控件
- `statusBar` (可选): 状态栏控件
- **返回**: 新建文件的路径和状态

##### `fileSave`
保存文件。

```python
def fileSave(self, textEdit, statusBar=None)
```
- `textEdit`: 文本编辑控件
- `statusBar` (可选): 状态栏控件
- **返回**: 保存文件的路径和状态

##### `fileSaveAs`
文件另存为。

```python
def fileSaveAs(self, textEdit, statusBar=None)
```
- `textEdit`: 文本编辑控件
- `statusBar` (可选): 状态栏控件
- **返回**: 另存为文件的路径和状态

##### `fileOpenFolder`
打开文件夹。

```python
def fileOpenFolder(self, model, treeView, statusBar=None)
```
- `model`: 文件系统模型
- `treeView`: 文件树视图
- `statusBar` (可选): 状态栏控件

##### `fileMoveTo`
移动文件。

```python
def fileMoveTo(self, textEdit, statusBar=None)
```
- `textEdit`: 文本编辑控件
- `statusBar` (可选): 状态栏控件
- **返回**: 移动文件的路径和状态

##### 私有方法

###### `_updateFileState`
更新文件状态。

```python
def _updateFileState(self, status)
```
- `status`: 文件状态（`True` 表示已保存，`False` 表示未保存）
- **返回**: 当前文件的状态

###### `_fileIsChanged`
标记文件内容已更改。

```python
def _fileIsChanged(self)
```
- **返回**: 当前文件的状态

###### `_fileIsSaved`
标记文件内容已保存。

```python
def _fileIsSaved(self)
```
- **返回**: 当前文件的状态

###### `_getFileState`
获取当前文件的状态。

```python
def _getFileState(self)
```
- **返回**: 文件状态（`True` 表示已保存，`False` 表示未保存）

###### `_updateFilePath`
更新文件路径。

```python
def _updateFilePath(self, filePath)
```
- `filePath`: 文件路径
- **返回**: 当前文件路径

###### `_getCurrentFilePath`
获取当前文件路径。

```python
def _getCurrentFilePath(self)
```
- **返回**: 当前文件路径（`None` 表示未打开文件）

###### `_updateCurrentFileDir`
更新当前文件所在的文件夹。

```python
def _updateCurrentFileDir(self, fileDir)
```
- `fileDir`: 文件夹路径
- **返回**: 当前文件夹路径

###### `_getCurrentFileDir`
获取当前文件夹路径。

```python
def _getCurrentFileDir(self)
```
- **返回**: 当前文件夹路径

###### `_notSaveWarning`
文件未保存时弹出警告对话框。

```python
def _notSaveWarning(self)
```
- **返回**: 用户的选择（`True` 表示保存，`False` 表示不保存，`None` 表示取消）

### 2. `EditHandler` 类

#### 描述
`EditHandler` 类提供了处理编辑框中的文本相关的操作，包括查找文本、替换文本、跳转到特定位置等功能。

#### 初始化方法
```python
def __init__(self, textEdit)
```
- `textEdit`: 文本编辑控件

#### 方法

##### `editFind`
在文本框中查找文本。

```python
def editFind(self)
```

##### `editReplace`
在文本框中替换选中的文本。

```python
def editReplace(self)
```

##### `editJumpToTop`
跳转到文本顶部。

```python
def editJumpToTop(self)
```

##### `editJumpToBottom`
跳转到文本底部。

```python
def editJumpToBottom(self)
```

##### `editJumpToSelection`
跳转到选中的文本区域。

```python
def editJumpToSelection(self)
```

##### `editJumpToLineStart`
跳转到当前行的行首。

```python
def editJumpToLineStart(self)
```

##### `editJumpToLineEnd`
跳转到当前行的行尾。

```python
def editJumpToLineEnd(self)
```

### 3. `CompileHandler` 类

#### 描述
`CompileHandler` 类提供了编译文件相关的操作，包括编译 LaTeX 文件和 Typst 文件。

#### 初始化方法
```python
def __init__(self, fileHandler)
```
- `fileHandler`: `FileHandler` 实例，用于获取当前文件路径等信息

#### 方法

##### `compileLaTeX`
编译 LaTeX 文件。

```python
def compileLaTeX(self)
```

##### `compileTypst`
编译 Typst 文件。

```python
def compileTypst(self)
```

### 4. `HelpHandler` 类

#### 描述
`HelpHandler` 类提供了帮助系统相关的操作，包括显示关于信息等。

#### 初始化方法
```python
def __init__(self)
```
- **属性**:
  - `_version`: 版本号
  - `_website`: 项目官网地址
  - `_email`: 联系邮箱

#### 方法

##### `helpAbout`
显示关于信息。

```python
def helpAbout(self)
```

## 示例

### 文件处理示例

```python
from mast import utils
from PySide6.QtWidgets import QTextEdit, QStatusBar

textEdit = QTextEdit()
statusBar = QStatusBar()

fileHandler = utils.FileHandler(textEdit, statusBar)

# 打开文件
filePath, state = fileHandler.fileOpen()

# 读取文件内容
content = fileHandler.readFile()
print(content)

# 保存文件
filePath, state = fileHandler.fileSave(textEdit, statusBar)
```

### 编辑框处理示例

```python
from mast import utils
from PySide6.QtWidgets import QTextEdit

textEdit = QTextEdit()
editHandler = utils.EditHandler(textEdit)

# 查找文本
editHandler.editFind()

# 替换文本
editHandler.editReplace()

# 跳转到文本顶部
editHandler.editJumpToTop()
```

### 编译处理示例

```python
from mast import utils

fileHandler = utils.FileHandler()
compileHandler = utils.CompileHandler(fileHandler)

# 编译 LaTeX 文件
compileHandler.compileLaTeX()

# 编译 Typst 文件
compileHandler.compileTypst()
```

### 帮助处理示例

```python
from mast import utils

helpHandler = utils.HelpHandler()

# 显示关于信息
helpHandler.helpAbout()
```
