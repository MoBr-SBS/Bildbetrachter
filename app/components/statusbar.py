"""
ImageStatusBar
Zeigt Dateiname und aktuellen Zoom-Faktor in der Statusleiste an.
"""

from PyQt6.QtWidgets import QStatusBar, QLabel
from PyQt6.QtCore import Qt


class ImageStatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        self._lbl_file = QLabel("Kein Bild geladen")
        self.addWidget(self._lbl_file, stretch=1)

        self._lbl_zoom = QLabel("100 %")
        self._lbl_zoom.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.addPermanentWidget(self._lbl_zoom)

    # ------------------------------------------------------------------ #
    # Öffentliche API
    # ------------------------------------------------------------------ #

    def set_filename(self, metadata: dict):
        self._lbl_file.setText(metadata.get("filename", "—"))

    def set_zoom(self, factor: float):
        self._lbl_zoom.setText(f"{round(factor * 100)} %")