"""
stylesheet.py
Zentrales QSS-Stylesheet der Anwendung (Dark Theme).

Farbpalette:
    --bg-deep:      #1a1a2e   Tiefstes Hintergrund (Fenster)
    --bg-surface:   #16213e   Oberflächen (Toolbar, Sidebar, Statusbar)
    --bg-raised:    #0f3460   Erhöhte Elemente (Buttons, Hover)
    --accent:       #e94560   Akzentfarbe (Fokus, aktive Elemente)
    --text-primary: #eaeaea   Haupttext
    --text-muted:   #8892a4   Gedämpfter Text (Labels, Hints)
    --border:       #2a2a4a   Subtile Trennlinien
"""

from PyQt6.QtWidgets import QApplication


STYLESHEET = """

/* ── Basis-Fenster ─────────────────────────────────────────────────── */

QMainWindow, QWidget {
    background-color: #1a1a2e;
    color: #eaeaea;
    font-family: "Segoe UI", "Inter", "Helvetica Neue", sans-serif;
    font-size: 13px;
}


/* ── Toolbar ───────────────────────────────────────────────────────── */

QToolBar {
    background-color: #16213e;
    border-bottom: 1px solid #2a2a4a;
    padding: 4px 8px;
    spacing: 4px;
}

QToolBar::separator {
    background-color: #2a2a4a;
    width: 1px;
    margin: 4px 6px;
}

QToolButton {
    background-color: transparent;
    color: #eaeaea;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 5px 12px;
    font-size: 13px;
}

QToolButton:hover {
    background-color: #0f3460;
    border-color: #2a2a4a;
}

QToolButton:pressed {
    background-color: #e94560;
    border-color: #e94560;
    color: #ffffff;
}


/* ── Scroll-Area (Bildanzeige) ─────────────────────────────────────── */

QScrollArea {
    border: none;
    background-color: #12122a;
}

QLabel#viewer_placeholder {
    color: #8892a4;
    font-size: 14px;
}

QScrollBar:vertical {
    background: #1a1a2e;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #2a2a4a;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #e94560;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background: #1a1a2e;
    height: 8px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal {
    background: #2a2a4a;
    border-radius: 4px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background: #e94560;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0px;
}


/* ── Sidebar ───────────────────────────────────────────────────────── */

/* Sidebar-Widget bekommt eine eigene Klasse via setObjectName */
QWidget#Sidebar {
    background-color: #16213e;
    border-left: 1px solid #2a2a4a;
}

QLabel#sidebar_title {
    color: #eaeaea;
    font-size: 13px;
    font-weight: 600;
    padding-bottom: 4px;
}

QLabel#sidebar_key {
    color: #8892a4;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

QLabel#sidebar_value {
    color: #eaeaea;
    font-size: 12px;
    padding-bottom: 6px;
}

QFrame#sidebar_separator {
    color: #2a2a4a;
}


/* ── Statusleiste ──────────────────────────────────────────────────── */

QStatusBar {
    background-color: #16213e;
    border-top: 1px solid #2a2a4a;
    color: #8892a4;
    font-size: 12px;
    padding: 0 8px;
}

QStatusBar QLabel {
    color: #8892a4;
    padding: 3px 0;
}


/* ── Datei-Dialog ──────────────────────────────────────────────────── */

QFileDialog {
    background-color: #1a1a2e;
    color: #eaeaea;
}

QFileDialog QListView,
QFileDialog QTreeView {
    background-color: #16213e;
    color: #eaeaea;
    border: 1px solid #2a2a4a;
    border-radius: 6px;
}

QFileDialog QPushButton {
    background-color: #0f3460;
    color: #eaeaea;
    border: 1px solid #2a2a4a;
    border-radius: 6px;
    padding: 5px 16px;
}

QFileDialog QPushButton:hover {
    background-color: #e94560;
    border-color: #e94560;
}


/* ── Allgemeine Schaltflächen ──────────────────────────────────────── */

QPushButton {
    background-color: #0f3460;
    color: #eaeaea;
    border: 1px solid #2a2a4a;
    border-radius: 6px;
    padding: 5px 16px;
}

QPushButton:hover {
    background-color: #e94560;
    border-color: #e94560;
}

QPushButton:pressed {
    background-color: #c73652;
}


/* ── Tooltips ──────────────────────────────────────────────────────── */

QToolTip {
    background-color: #0f3460;
    color: #eaeaea;
    border: 1px solid #2a2a4a;
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 12px;
}


/* ── Thumbnail-Leiste ──────────────────────────────────────────────── */

QScrollArea#ThumbnailBar {
    background-color: #16213e;
    border-top: 1px solid #2a2a4a;
    border-bottom: none;
    border-left: none;
    border-right: none;
}

QWidget#ThumbnailBarContainer {
    background-color: #16213e;
}

QFrame#ThumbnailItem {
    background-color: #1a1a2e;
    border: 1px solid #2a2a4a;
    border-radius: 4px;
}

QFrame#ThumbnailItem:hover {
    border: 1px solid #8892a4;
    background-color: #0f3460;
}

QFrame#ThumbnailItem[active=true] {
    border: 2px solid #e94560;
    background-color: #0f3460;
}

"""


def apply_stylesheet(app: QApplication) -> None:
    """Wendet das Stylesheet auf die gesamte Anwendung an."""
    app.setStyleSheet(STYLESHEET)