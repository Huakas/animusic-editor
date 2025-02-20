from PySide6.QtWidgets import QApplication
import sys
from main_window import EditorWindow

app = QApplication(sys.argv)

window = EditorWindow()
window.show()

app.exec()
