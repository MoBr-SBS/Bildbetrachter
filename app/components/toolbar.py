"""
ImageToolbar
Werkzeugleiste mit allen Aktionsschaltflächen.
"""

from PyQt6.QtWidgets import QToolBar, QFileDialog
from PyQt6.QtGui import QAction
from PyQt6.QtCore import pyqtSignal

IMAGE_FILTER = (
    "Bilder (*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp);;"
    "Alle Dateien (*)"
)


class ImageToolbar(QToolBar):
    open_requested     = pyqtSignal(str)
    fit_requested      = pyqtSignal()
    rotate_requested   = pyqtSignal(int)
    previous_requested = pyqtSignal()
    next_requested     = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__("Werkzeuge", parent)
        self.setMovable(False)
        self._build_actions()

    # ------------------------------------------------------------------ #
    # Aufbau
    # ------------------------------------------------------------------ #

    def _build_actions(self):
        act_open = QAction("📂 Öffnen", self)
        act_open.setToolTip("Bilddatei öffnen (Strg+O)")
        act_open.setShortcut("Ctrl+O")
        act_open.triggered.connect(self._on_open)
        self.addAction(act_open)

        self.addSeparator()

        self._act_prev = QAction("◀ Zurück", self)
        self._act_prev.setToolTip("Vorheriges Bild (←)")
        self._act_prev.setShortcut("Left")
        self._act_prev.setEnabled(False)
        self._act_prev.triggered.connect(self.previous_requested)
        self.addAction(self._act_prev)

        self._act_next = QAction("Weiter ▶", self)
        self._act_next.setToolTip("Nächstes Bild (→)")
        self._act_next.setShortcut("Right")
        self._act_next.setEnabled(False)
        self._act_next.triggered.connect(self.next_requested)
        self.addAction(self._act_next)

        self.addSeparator()

        act_fit = QAction("⤢ Anpassen", self)
        act_fit.setToolTip("Bild ans Fenster anpassen (F)")
        act_fit.setShortcut("F")
        act_fit.triggered.connect(self.fit_requested)
        self.addAction(act_fit)

        self.addSeparator()

        act_rotate_ccw = QAction("↺ Links", self)
        act_rotate_ccw.setToolTip("90° gegen Uhrzeigersinn drehen (L)")
        act_rotate_ccw.setShortcut("L")
        act_rotate_ccw.triggered.connect(lambda: self.rotate_requested.emit(-90))
        self.addAction(act_rotate_ccw)

        act_rotate_cw = QAction("↻ Rechts", self)
        act_rotate_cw.setToolTip("90° im Uhrzeigersinn drehen (R)")
        act_rotate_cw.setShortcut("R")
        act_rotate_cw.triggered.connect(lambda: self.rotate_requested.emit(90))
        self.addAction(act_rotate_cw)

    def enable_navigation(self, enabled: bool) -> None:
        """Aktiviert oder deaktiviert die Vor/Zurück-Buttons."""
        self._act_prev.setEnabled(enabled)
        self._act_next.setEnabled(enabled)

    # ------------------------------------------------------------------ #
    # Slots
    # ------------------------------------------------------------------ #

    def _on_open(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Bild öffnen", "", IMAGE_FILTER
        )
        if filepath:
            self.open_requested.emit(filepath)