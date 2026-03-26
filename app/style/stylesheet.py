"""
stylesheet.py

Kompakter, dunkler Stil passend zur Referenz:
schmale rechte Infoleiste mit nüchterner Dateiinfo.
"""

from PyQt6.QtWidgets import QApplication


STYLESHEET = """
QMainWindow,
QWidget {
    background-color: #2f2f2f;
    color: #e8e8e8;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 12px;
}

/* Hauptbereich */
QWidget#CentralWidget,
QWidget#ContentRow {
    background-color: #2f2f2f;
}

/* Toolbar */
QToolBar {
    background-color: #2f2f2f;
    border: none;
    border-bottom: 1px solid #3b3b3b;
    spacing: 4px;
    padding: 4px 6px;
}

QToolButton {
    background-color: #3a3a3a;
    color: #f0f0f0;
    border: 1px solid #4a4a4a;
    border-radius: 4px;
    padding: 4px 8px;
}

QToolButton:hover {
    background-color: #454545;
    border: 1px solid #5d5d5d;
}

QToolButton:pressed {
    background-color: #2b2b2b;
}

/* Viewer */
QScrollArea {
    background-color: #262626;
    border: 1px solid #3b3b3b;
}

/* Sidebar */
QWidget#Sidebar {
    background-color: #2f2f2f;
    border-left: 1px solid #3b3b3b;
}

QLabel#sidebar_section_header {
    color: #d7d7d7;
    font-size: 13px;
    font-weight: 700;
    padding: 0;
    margin: 0;
}

QFrame#sidebar_info_frame {
    background-color: transparent;
    border: none;
}

QLabel#sidebar_key {
    color: #d0d0d0;
    font-size: 12px;
    font-weight: 600;
    padding: 0;
    margin: 0;
}

QLabel#sidebar_value {
    color: #ffffff;
    font-size: 12px;
    font-weight: 700;
    padding: 0;
    margin: 0;
}

/* Statusbar */
QStatusBar {
    background-color: #2f2f2f;
    color: #f0f0f0;
    border-top: 1px solid #3b3b3b;
}

QStatusBar::item {
    border: none;
}

/* Scrollbars */
QScrollBar:vertical {
    background: #2f2f2f;
    width: 10px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #5a5a5a;
    min-height: 20px;
    border-radius: 4px;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: transparent;
}

QScrollBar:horizontal {
    background: #2f2f2f;
    height: 10px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background: #5a5a5a;
    min-width: 20px;
    border-radius: 4px;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0;
}

QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {
    background: transparent;
}

/* Thumbnail-Bereich */
QScrollArea#SidebarThumbnailBar,
QScrollArea#ThumbnailBar {
    background-color: transparent;
    border: none;
}

QWidget#ThumbnailBarContainer {
    background-color: transparent;
}

QFrame#ThumbnailItem {
    background-color: #111111;
    border: 1px solid #3a3a3a;
    border-radius: 2px;
}

QFrame#ThumbnailItem:hover {
    border: 1px solid #4d94ff;
}

QFrame#ThumbnailItem[active=true] {
    border: 1px solid #2f8cff;
}

/* Buttons allgemein */
QPushButton {
    background-color: #3a3a3a;
    color: #f0f0f0;
    border: 1px solid #4a4a4a;
    border-radius: 4px;
    padding: 4px 8px;
}

QPushButton:hover {
    background-color: #454545;
}
"""


def apply_stylesheet(app: QApplication) -> None:
    app.setStyleSheet(STYLESHEET)
