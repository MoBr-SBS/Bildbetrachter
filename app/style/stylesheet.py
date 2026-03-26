"""
stylesheet.py

Zentrales QSS-Stylesheet der Anwendung.
Modernes Dark UI mit ruhigerem Layout und klareren Flächen.
"""

from PyQt6.QtWidgets import QApplication


STYLESHEET = """
/* --------------------------------------------------------------- */
/* Basis */
/* --------------------------------------------------------------- */

QMainWindow,
QWidget {
    background-color: #0f172a;
    color: #e5e7eb;
    font-family: "Segoe UI", "Inter", "Helvetica Neue", sans-serif;
    font-size: 13px;
}

QWidget#CentralWidget,
QWidget#ContentRow {
    background-color: #0f172a;
}

/* --------------------------------------------------------------- */
/* Toolbar */
/* --------------------------------------------------------------- */

QToolBar {
    background-color: #111827;
    border: none;
    border-bottom: 1px solid #1f2937;
    spacing: 6px;
    padding: 8px 10px;
}

QToolBar::separator {
    width: 1px;
    margin: 6px 8px;
    background-color: #243041;
}

QToolButton {
    background-color: #1f2937;
    color: #e5e7eb;
    border: 1px solid #2c3b50;
    border-radius: 10px;
    padding: 7px 14px;
    margin: 2px 0;
}

QToolButton:hover {
    background-color: #273449;
    border-color: #3b82f6;
}

QToolButton:pressed {
    background-color: #2563eb;
    border-color: #2563eb;
    color: white;
}

QToolButton:disabled {
    background-color: #17202d;
    color: #6b7280;
    border-color: #1f2937;
}

/* --------------------------------------------------------------- */
/* Bildbereich */
/* --------------------------------------------------------------- */

QScrollArea {
    border: none;
    background-color: #0b1220;
    border-radius: 18px;
}

QLabel#viewer_placeholder {
    color: #94a3b8;
    font-size: 15px;
    padding: 24px;
}

/* --------------------------------------------------------------- */
/* Sidebar */
/* --------------------------------------------------------------- */

QWidget#Sidebar {
    background-color: #111827;
    border: 1px solid #1f2937;
    border-radius: 18px;
}

QLabel#sidebar_title {
    font-size: 20px;
    font-weight: 700;
    color: #f8fafc;
    padding-top: 2px;
}

QLabel#sidebar_subtitle {
    font-size: 12px;
    color: #94a3b8;
    padding-bottom: 2px;
}

QLabel#sidebar_section_title {
    font-size: 15px;
    font-weight: 700;
    color: #f8fafc;
    margin-top: 4px;
}

QLabel#sidebar_section_hint {
    font-size: 12px;
    color: #94a3b8;
    margin-bottom: 2px;
}

QLabel#sidebar_key {
    color: #93c5fd;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 6px;
}

QLabel#sidebar_value {
    background-color: #0f172a;
    border: 1px solid #1f2937;
    border-radius: 10px;
    padding: 10px 12px;
    color: #e5e7eb;
}

QFrame#sidebar_separator {
    background-color: #243041;
    max-height: 1px;
    min-height: 1px;
    border: none;
    margin: 2px 0 4px 0;
}

/* --------------------------------------------------------------- */
/* Statusbar */
/* --------------------------------------------------------------- */

QStatusBar {
    background-color: #111827;
    color: #cbd5e1;
    border-top: 1px solid #1f2937;
}

QStatusBar::item {
    border: none;
}

/* --------------------------------------------------------------- */
/* Scrollbars */
/* --------------------------------------------------------------- */

QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 4px;
}

QScrollBar::handle:vertical {
    background: #334155;
    min-height: 30px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background: #475569;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: transparent;
}

QScrollBar:horizontal {
    background: transparent;
    height: 10px;
    margin: 4px;
}

QScrollBar::handle:horizontal {
    background: #334155;
    min-width: 30px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal:hover {
    background: #475569;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0px;
}

QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {
    background: transparent;
}

/* --------------------------------------------------------------- */
/* Thumbnail-Bar rechts */
/* --------------------------------------------------------------- */

QScrollArea#ThumbnailBar,
QScrollArea#SidebarThumbnailBar {
    background-color: #0f172a;
    border: 1px solid #1f2937;
    border-radius: 14px;
}

QWidget#ThumbnailBarContainer {
    background-color: #0f172a;
    border-radius: 14px;
}

QFrame#ThumbnailItem {
    background-color: #111827;
    border: 1px solid #243041;
    border-radius: 12px;
}

QFrame#ThumbnailItem:hover {
    background-color: #172131;
    border: 1px solid #3b82f6;
}

QFrame#ThumbnailItem[active=true] {
    background-color: #1d4ed8;
    border: 2px solid #60a5fa;
}

/* --------------------------------------------------------------- */
/* Allgemeine Buttons */
/* --------------------------------------------------------------- */

QPushButton {
    background-color: #1f2937;
    color: #e5e7eb;
    border: 1px solid #2c3b50;
    border-radius: 10px;
    padding: 7px 14px;
}

QPushButton:hover {
    background-color: #273449;
    border-color: #3b82f6;
}

QPushButton:pressed {
    background-color: #2563eb;
    border-color: #2563eb;
}

/* --------------------------------------------------------------- */
/* Tooltips */
/* --------------------------------------------------------------- */

QToolTip {
    background-color: #111827;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 6px 8px;
}
"""


def apply_stylesheet(app: QApplication) -> None:
    """Wendet das Stylesheet auf die gesamte Anwendung an."""
    app.setStyleSheet(STYLESHEET)
