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
