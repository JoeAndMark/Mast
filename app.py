"""
文件名：app.py
文件描述：程序的入口文件。将程序封装成为一个模块，通过本文件调用。
作者：JoeAndMark
时间：2024-5-1
"""

import sys
from PySide6.QtWidgets import QApplication
from mast.main import MainWindow


def main():
    app = QApplication(sys.argv)
    mast = MainWindow()
    mast.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
