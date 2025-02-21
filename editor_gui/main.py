from PySide6.QtWidgets import QApplication
import sys
from .main_window import EditorWindow


def main():
    app = QApplication(sys.argv)

    window = EditorWindow()
    window.show()

    app.exec()
