"""
stylesheet.py
Zentrales QSS-Stylesheet der Anwendung — neutrales Dunkelgrau-Theme.

Farbpalette:
    --bg-deep:      #1a1a1a   Tiefstes Hintergrund (Viewer)
    --bg-base:      #1e1e1e   Fensterhintergrund
    --bg-surface:   #252525   Toolbar, Sidebar, Statusbar
    --bg-raised:    #2e2e2e   Buttons, Felder
    --bg-hover:     #383838   Hover-Zustand
    --bg-active:    #444444   Aktive Elemente
    --accent:       #a0a0a0   Akzent (Slider-Thumb, aktive Borders)
    --text-primary: #e0e0e0   Haupttext
    --text-muted:   #888888   Gedämpfter Text
    --border:       #333333   Subtile Trennlinien
    --border-hover: #555555   Hover-Border
"""

from PyQt6.QtWidgets import QApplication


STYLESHEET = """

/* ── Basis ──────────────────────────────────────────────────────────── */

QMainWindow, QWidget {
    background-color: #1e1e1e;
    color: #e0e0e0;
    font-family: "Segoe UI", "Inter", "Helvetica Neue", sans-serif;
    font-size: 13px;
}


/* ── Toolbar ─────────────────────────────────────────────────────────── */

QToolBar {
    background-color: #252525;
    border-bottom: 1px solid #333333;
    padding: 4px 8px;
    spacing: 4px;
}

QToolBar::separator {
    background-color: #333333;
    width: 1px;
    margin: 4px 6px;
}

QToolButton {
    background-color: transparent;
    color: #e0e0e0;
    border: 1px solid transparent;
    border-radius: 5px;
    padding: 5px 12px;
    font-size: 13px;
}

QToolButton:hover {
    background-color: #2e2e2e;
    border-color: #444444;
}

QToolButton:pressed {
    background-color: #444444;
    border-color: #666666;
    color: #ffffff;
}

QToolButton:disabled {
    color: #505050;
}


/* ── Scroll-Area (Bildanzeige) ───────────────────────────────────────── */

QScrollArea {
    border: none;
    background-color: #1a1a1a;
}

QScrollBar:vertical {
    background: #1e1e1e;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #3a3a3a;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #606060;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background: #1e1e1e;
    height: 8px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal {
    background: #3a3a3a;
    border-radius: 4px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background: #606060;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0px;
}


/* ── Viewer Placeholder ──────────────────────────────────────────────── */

QLabel#viewer_placeholder {
    color: #505050;
    font-size: 14px;
}


/* ── Sidebar ─────────────────────────────────────────────────────────── */

QWidget#Sidebar {
    background-color: #222222;
    border-left: 1px solid #333333;
}

QWidget#SidebarSection {
    background-color: #222222;
}

QLabel#sidebar_title {
    color: #a0a0a0;
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding-bottom: 2px;
}

QLabel#sidebar_key {
    color: #606060;
    font-size: 11px;
}

QLabel#sidebar_value {
    color: #cccccc;
    font-size: 12px;
    padding-bottom: 4px;
}

QFrame#sidebar_separator {
    background-color: #333333;
    max-height: 1px;
    border: none;
}

QScrollArea#ThumbScroll {
    background-color: transparent;
    border: none;
}

QScrollArea#ThumbScroll > QWidget > QWidget {
    background-color: transparent;
}


/* ── Thumbnail-Kacheln ───────────────────────────────────────────────── */

QFrame#ThumbCell {
    background-color: #2a2a2a;
    border: 1px solid #333333;
    border-radius: 4px;
}

QFrame#ThumbCell:hover {
    background-color: #333333;
    border-color: #606060;
}

QFrame#ThumbCell[active=true] {
    border: 2px solid #a0a0a0;
    background-color: #303030;
}


/* ── Statusleiste ────────────────────────────────────────────────────── */

QStatusBar {
    background-color: #252525;
    border-top: 1px solid #333333;
    color: #888888;
    font-size: 12px;
    padding: 0 8px;
}

QStatusBar QLabel {
    color: #888888;
    padding: 3px 0;
}

QLabel#zoom_label {
    color: #aaaaaa;
    font-size: 12px;
    font-weight: 500;
    min-width: 44px;
}


/* ── Zoom-Slider ─────────────────────────────────────────────────────── */

QSlider#zoom_slider::groove:horizontal {
    height: 4px;
    background: #3a3a3a;
    border-radius: 2px;
}

QSlider#zoom_slider::handle:horizontal {
    width: 12px;
    height: 12px;
    background: #a0a0a0;
    border-radius: 6px;
    margin: -4px 0;
}

QSlider#zoom_slider::handle:horizontal:hover {
    background: #cccccc;
}

QSlider#zoom_slider::sub-page:horizontal {
    background: #666666;
    border-radius: 2px;
}


/* ── Zoom +/- Buttons ────────────────────────────────────────────────── */

QPushButton#zoom_btn {
    background-color: #2e2e2e;
    color: #cccccc;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    font-size: 15px;
    font-weight: 400;
    padding: 0;
}

QPushButton#zoom_btn:hover {
    background-color: #3a3a3a;
    border-color: #606060;
    color: #ffffff;
}

QPushButton#zoom_btn:pressed {
    background-color: #505050;
}


/* ── Allgemeine Buttons ──────────────────────────────────────────────── */

QPushButton {
    background-color: #2e2e2e;
    color: #e0e0e0;
    border: 1px solid #3a3a3a;
    border-radius: 5px;
    padding: 5px 14px;
}

QPushButton:hover {
    background-color: #383838;
    border-color: #555555;
}

QPushButton:pressed {
    background-color: #444444;
}


/* ── Datei-Dialog ────────────────────────────────────────────────────── */

QFileDialog {
    background-color: #1e1e1e;
    color: #e0e0e0;
}

QFileDialog QListView,
QFileDialog QTreeView {
    background-color: #252525;
    color: #e0e0e0;
    border: 1px solid #333333;
    border-radius: 5px;
}

QFileDialog QPushButton {
    background-color: #2e2e2e;
    color: #e0e0e0;
    border: 1px solid #3a3a3a;
    border-radius: 5px;
    padding: 5px 14px;
}

QFileDialog QPushButton:hover {
    background-color: #383838;
    border-color: #555555;
}


/* ── Tooltips ────────────────────────────────────────────────────────── */

QToolTip {
    background-color: #2e2e2e;
    color: #e0e0e0;
    border: 1px solid #444444;
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 12px;
}

"""


def apply_stylesheet(app: QApplication) -> None:
    """Wendet das Stylesheet auf die gesamte Anwendung an."""
    app.setStyleSheet(STYLESHEET)