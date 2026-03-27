import sys
import ctypes

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from app.main_window import MainWindow
from app.style import apply_stylesheet

myappid = 'Bildbetrachter.MB.version1'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Bildbetrachter")
    apply_stylesheet(app)

    window = MainWindow()
    window.setWindowIcon(QIcon("icon.png"))
    window.show()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()