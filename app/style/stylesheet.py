"""
stylesheet.py

Zentrales Stylesheet für den Bildbetrachter.
Dunkles, kompaktes UI mit:
- ruhiger Toolbar
- klarer rechter Sidebar
- Thumbnail-Raster rechts
- sauberer Statusbar
"""

from PyQt6.QtWidgets import QApplication


STYLESHEET = """
/* ---------------------------------------------------------- */
/* Basis */
/* ---------------------------------------------------------- */

QMainWindow,
QWidget {
    background-color: #262626;
    color: #e8e8e8;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 12px;
}

QWidget#CentralWidget,
QWidget#ContentRow {
    background-color: #262626;
}


/* ---------------------------------------------------------- */
/* Toolbar */
/* ---------------------------------------------------------- */

QToolBar#MainToolbar {
    background-color: #2b2b2b;
    border: none;
    border-bottom: 1px solid #3a3a3a;
    spacing: 6px;
    padding: 6px 8px;
}

QToolBar#MainToolbar::separator {
    width: 10px;
    background: transparent;
}

QToolBar#MainToolbar QToolButton {
    background-color: #343434;
    color: #f2f2f2;
    border: 1px solid #474747;
    border-radius: 5px;
    padding: 5px 12px;
    min-height: 26px;
    font-weight: 600;
}

QToolBar#MainToolbar QToolButton:hover {
    background-color: #404040;
    border: 1px solid #5e5e5e;
}

QToolBar#MainToolbar QToolButton:pressed {
    background-color: #262626;
    border: 1px solid #6a6a6a;
}

QToolBar#MainToolbar QToolButton:disabled {
    color: #8c8c8c;
    background-color: #303030;
    border: 1px solid #404040;
}


/* ---------------------------------------------------------- */
/* Viewer */
/* ---------------------------------------------------------- */

QScrollArea {
    background-color: #202020;
    border: 1px solid #343434;
}

QLabel#viewer_placeholder {
    color: #9c9c9c;
    font-size: 14px;
    padding: 20px;
}


/* ---------------------------------------------------------- */
/* Sidebar */
/* ---------------------------------------------------------- */

QWidget#Sidebar {
    background-color: #2b2b2b;
    border-left: 1px solid #3a3a3a;
}

QLabel#sidebar_section_header {
    color: #d8d8d8;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.3px;
    padding: 0;
    margin: 0;
}

QFrame#sidebar_info_frame {
    background-color: transparent;
    border: none;
}

QLabel#sidebar_key {
    color: #cfcfcf;
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


/* ---------------------------------------------------------- */
/* Thumbnail-Bereich */
/* ---------------------------------------------------------- */

QScrollArea#ThumbnailBar,
QScrollArea#SidebarThumbnailBar {
    background-color: transparent;
    border: none;
}

QWidget#ThumbnailBarContainer {
    background-color: transparent;
}

QFrame#ThumbnailItem {
    background-color: #111111;
    border: 1px solid #3d3d3d;
    border-radius: 2px;
}

QFrame#ThumbnailItem:hover {
    border: 1px solid #4d94ff;
}

QFrame#ThumbnailItem[active="true"] {
    border: 1px solid #2f8cff;
    background-color: #161616;
}


/* ---------------------------------------------------------- */
/* Statusbar */
/* ---------------------------------------------------------- */

QStatusBar {
    background-color: #2a2a2a;
    color: #f0f0f0;
    border-top: 1px solid #3b3b3b;
}

QStatusBar::item {
    border: none;
}


/* ---------------------------------------------------------- */
/* Scrollbars */
/* ---------------------------------------------------------- */

QScrollBar:vertical {
    background: #292929;
    width: 10px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #5d5d5d;
    min-height: 24px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #727272;
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
    background: #292929;
    height: 10px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background: #5d5d5d;
    min-width: 24px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal:hover {
    background: #727272;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0;
}

QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {
    background: transparent;
}


/* ---------------------------------------------------------- */
/* Allgemeine Buttons */
/* ---------------------------------------------------------- */

QPushButton {
    background-color: #343434;
    color: #f0f0f0;
    border: 1px solid #474747;
    border-radius: 4px;
    padding: 4px 10px;
}

QPushButton:hover {
    background-color: #404040;
    border: 1px solid #5c5c5c;
}

QPushButton:pressed {
    background-color: #2a2a2a;
}


/* ---------------------------------------------------------- */
/* Tooltip */
/* ---------------------------------------------------------- */

QToolTip {
    background-color: #303030;
    color: #f5f5f5;
    border: 1px solid #4c4c4c;
    padding: 4px 6px;
}
"""


def apply_stylesheet(app: QApplication) -> None:
    app.setStyleSheet(STYLESHEET)
