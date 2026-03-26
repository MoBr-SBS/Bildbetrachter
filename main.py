"""
Bildbetrachter — Einstiegspunkt
Startet die Qt-Anwendung und öffnet das Hauptfenster.
"""

import sys
from PyQt6.QtWidgets import QApplication
from app.main_window import MainWindow
from app.style import apply_stylesheet


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Bildbetrachter")
    apply_stylesheet(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()