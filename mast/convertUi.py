"""
模块名称：convertUi.py
模块描述：将 .ui 文件转换为 .py 文件，实现操作逻辑和界面的分离。可以批量进行转换。
作者：JoeAndMark
时间：2024-5-1
"""
# 导入标准库
import os
import os.path

# 导入第三方库


# 导入自定义库

class Converter:
    """
    先留着，事情有点多，以后再写……
    """
    def __init__(self):
        pass

def currentDir():
    dir = os.getcwd()
    if 'mast' not in dir:
        dir += '\\mast'
    
    return dir


# 列出当前文件下所有 .ui 文件
def listUiFile():
    lst = []
    dir = currentDir()
    files = os.listdir(dir)
    for filename in files:
        if os.path.splitext(filename)[1] == '.ui':
            lst.append(filename)
    
    return lst


# 重命名 .ui 文件
def transPyFile(filename):
    return os.path.splitext(filename)[0] + '.py'


# 将 .ui 文件转换为 .py 文件
def main():
    list = listUiFile()
    dir = currentDir()

    for uiFile in list:
        pyFile = transPyFile(uiFile)
        pyFilePath = dir + f'\\{pyFile}'
        uiFilePath = dir + f'\\{uiFile}'
        cmd = f'pyside6-uic.exe -o {pyFilePath} {uiFilePath}'
        print(cmd) # 如果终端报错，就复制一下命令手动执行。更新了一次vscode就出了bug，不知道为什么……
        try:
            os.system(cmd)
        except OSError as e:
            print(f"转换失败: {uiFile} 到 {e}")


if __name__ == '__main__':
    main()