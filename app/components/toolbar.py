"""
ImageToolbar

Moderne Werkzeugleiste für den Bildbetrachter.
"""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QFileDialog, QToolBar


IMAGE_FILTER = (
    "Bilder (*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp);;"
    "Alle Dateien (*)"
)


class ImageToolbar(QToolBar):
    open_requested = pyqtSignal(str)
    zoom_in_requested = pyqtSignal()
    zoom_out_requested = pyqtSignal()
    fit_requested = pyqtSignal()
    rotate_requested = pyqtSignal(int)
    previous_requested = pyqtSignal()
    next_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__("Werkzeuge", parent)

        self.setObjectName("MainToolbar")
        self.setMovable(False)
        self.setFloatable(False)

        self._build_actions()

    def _build_actions(self) -> None:
        self._act_open = QAction("Öffnen", self)
        self._act_open.setToolTip("Bilddatei öffnen (Strg+O)")
        self._act_open.setShortcut("Ctrl+O")
        self._act_open.triggered.connect(self._on_open)
        self.addAction(self._act_open)

        self.addSeparator()

        self._act_prev = QAction("Zurück", self)
        self._act_prev.setToolTip("Vorheriges Bild")
        self._act_prev.setShortcut("Left")
        self._act_prev.setEnabled(False)
        self._act_prev.triggered.connect(self.previous_requested.emit)
        self.addAction(self._act_prev)

        self._act_next = QAction("Weiter", self)
        self._act_next.setToolTip("Nächstes Bild")
        self._act_next.setShortcut("Right")
        self._act_next.setEnabled(False)
        self._act_next.triggered.connect(self.next_requested.emit)
        self.addAction(self._act_next)

        self.addSeparator()

        self._act_zoom_in = QAction("Zoom +", self)
        self._act_zoom_in.setToolTip("Vergrößern")
        self._act_zoom_in.setShortcut("+")
        self._act_zoom_in.triggered.connect(self.zoom_in_requested.emit)
        self.addAction(self._act_zoom_in)

        self._act_zoom_out = QAction("Zoom -", self)
        self._act_zoom_out.setToolTip("Verkleinern")
        self._act_zoom_out.setShortcut("-")
        self._act_zoom_out.triggered.connect(self.zoom_out_requested.emit)
        self.addAction(self._act_zoom_out)

        self._act_fit = QAction("Anpassen", self)
        self._act_fit.setToolTip("Bild ans Fenster anpassen")
        self._act_fit.setShortcut("F")
        self._act_fit.triggered.connect(self.fit_requested.emit)
        self.addAction(self._act_fit)

        self.addSeparator()

        self._act_rotate = QAction("Drehen", self)
        self._act_rotate.setToolTip("90° drehen")
        self._act_rotate.setShortcut("R")
        self._act_rotate.triggered.connect(
            lambda: self.rotate_requested.emit(90)
        )
        self.addAction(self._act_rotate)

    def enable_navigation(self, enabled: bool) -> None:
        self._act_prev.setEnabled(enabled)
        self._act_next.setEnabled(enabled)

    def _on_open(self) -> None:
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Bild öffnen",
            "",
            IMAGE_FILTER,
        )
        if filepath:
            self.open_requested.emit(filepath)
