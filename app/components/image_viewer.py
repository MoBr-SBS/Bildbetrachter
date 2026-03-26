"""
ImageViewer
Zuständig für die Anzeige, den Zoom und die Rotation des Bildes.
Kapselt die gesamte Bildlogik — MainWindow kennt nur die öffentliche API.
"""

import os
from PyQt6.QtWidgets import QScrollArea, QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtCore import Qt, pyqtSignal

ZOOM_STEP = 0.15
ZOOM_MIN  = 0.05
ZOOM_MAX  = 10.0


class ImageViewer(QScrollArea):
    image_loaded = pyqtSignal(dict)
    zoom_changed = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._pixmap_original: QPixmap | None = None
        self._rotation: int = 0
        self._zoom: float = 1.0

        self._build_ui()

    # ------------------------------------------------------------------ #
    # UI-Aufbau
    # ------------------------------------------------------------------ #

    def _build_ui(self):
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._label = QLabel("Keine Datei geöffnet.\nStrg+O oder Toolbar nutzen.")
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label.setObjectName("viewer_placeholder")
        self._label.setSizePolicy(
            QSizePolicy.Policy.Ignored,
            QSizePolicy.Policy.Ignored,
        )
        self._label.setScaledContents(False)

        self.setWidget(self._label)
        self.setWidgetResizable(True)

    # ------------------------------------------------------------------ #
    # Öffentliche API
    # ------------------------------------------------------------------ #

    def load_image(self, filepath: str):
        """Lädt eine Bilddatei und zeigt sie an."""
        pixmap = QPixmap(filepath)
        if pixmap.isNull():
            self._label.setText(f"Fehler: Datei konnte nicht geladen werden.\n{filepath}")
            return

        self._pixmap_original = pixmap
        self._rotation = 0
        self._zoom = 1.0

        self._render()
        self.image_loaded.emit(self._build_metadata(filepath))
        self.zoom_changed.emit(self._zoom)

    def zoom_in(self):
        self._set_zoom(self._zoom + ZOOM_STEP)

    def zoom_out(self):
        self._set_zoom(self._zoom - ZOOM_STEP)

    def fit_to_window(self):
        """Skaliert das Bild so, dass es ins Fenster passt."""
        if self._pixmap_original is None:
            return
        available = self.viewport().size()
        pixmap = self._rotated_pixmap()
        scale_w = available.width() / pixmap.width()
        scale_h = available.height() / pixmap.height()
        self._set_zoom(min(scale_w, scale_h))

    def rotate(self, degrees: int = 90):
        if self._pixmap_original is None:
            return
        self._rotation = (self._rotation + degrees) % 360
        self._render()

    # ------------------------------------------------------------------ #
    # Interne Hilfsmethoden
    # ------------------------------------------------------------------ #

    def _set_zoom(self, factor: float):
        self._zoom = max(ZOOM_MIN, min(ZOOM_MAX, factor))
        self._render()
        self.zoom_changed.emit(self._zoom)

    def _rotated_pixmap(self) -> QPixmap:
        transform = QTransform().rotate(self._rotation)
        return self._pixmap_original.transformed(
            transform, Qt.TransformationMode.SmoothTransformation
        )

    def _render(self):
        if self._pixmap_original is None:
            return
        pixmap = self._rotated_pixmap()
        w = int(pixmap.width() * self._zoom)
        h = int(pixmap.height() * self._zoom)
        scaled = pixmap.scaled(
            w, h,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self._label.setPixmap(scaled)
        self._label.resize(scaled.size())
        self.setWidgetResizable(False)

    def _build_metadata(self, filepath: str) -> dict:
        size_bytes = os.path.getsize(filepath)
        return {
            "filename": os.path.basename(filepath),
            "filepath": filepath,
            "width":    self._pixmap_original.width(),
            "height":   self._pixmap_original.height(),
            "size_kb":  round(size_bytes / 1024, 1),
        }