"""
convertUi.py

This modules provides functionality for converting a batch .ui files. 
"""

import os
import os.path


def currentDir():
    dir = os.getcwd()
    if 'mast' not in dir:
        dir += '\\mast'
    
    return dir


# List all .ui files at current directory.
def listUiFile():
    lst = []
    dir = currentDir()
    files = os.listdir(dir)
    for filename in files:
        if os.path.splitext(filename)[1] == '.ui':
            lst.append(filename)
    
    return lst


# rename .ui files
def transPyFile(filename):
    return os.path.splitext(filename)[0] + '.py'


# translate .ui to .py
def main():
    list = listUiFile()
    dir = currentDir()

    for uiFile in list:
        pyFile = transPyFile(uiFile)
        pyFilePath = dir + f'\\{pyFile}'
        uiFilePath = dir + f'\\{uiFile}'
        cmd = f'pyside6-uic.exe -o {pyFilePath} {uiFilePath}'
        print(cmd) # 如果终端报错，就复制一下命令手动执行。不知道为什么……
        try:
            os.system(cmd)
        except OSError as e:
            print(f"转换失败: {uiFile} 到 {e}")


if __name__ == '__main__':
    main()