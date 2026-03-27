"""
ImageViewer
Zuständig für die Anzeige, den Zoom und die Rotation des Bildes.
Kapselt die gesamte Bildlogik — MainWindow kennt nur die öffentliche API.
"""

import os
from PyQt6.QtWidgets import QScrollArea, QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtCore import Qt, pyqtSignal, QTimer

ZOOM_STEP          = 0.15
ZOOM_MIN           = 0.05
ZOOM_MAX           = 10.0
SMOOTH_DELAY_MS    = 200   # ms bis zum hochqualitativen Re-Render


class ImageViewer(QScrollArea):
    image_loaded = pyqtSignal(dict)
    zoom_changed = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._pixmap_original: QPixmap | None = None
        self._pixmap_rotated:  QPixmap | None = None   # Cache für rotierte Pixmap
        self._rotation: int   = 0
        self._zoom:     float = 1.0

        # Feuert nach kurzer Ruhezeit für den hochqualitativen Re-Render
        self._smooth_timer = QTimer(self)
        self._smooth_timer.setSingleShot(True)
        self._smooth_timer.setInterval(SMOOTH_DELAY_MS)
        self._smooth_timer.timeout.connect(self._render_smooth)

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
        self._pixmap_rotated  = pixmap   # Rotation = 0, Cache = Original
        self._rotation = 0
        self._zoom     = 1.0

        self._render_smooth()
        self.image_loaded.emit(self._build_metadata(filepath))
        self.zoom_changed.emit(self._zoom)

    def zoom_in(self):
        self._set_zoom(self._zoom + ZOOM_STEP)

    def zoom_out(self):
        self._set_zoom(self._zoom - ZOOM_STEP)

    def set_zoom(self, factor: float):
        """Wird vom Statusleisten-Slider aufgerufen — nutzt Fast-Render während Drag."""
        new_zoom = max(ZOOM_MIN, min(ZOOM_MAX, factor))
        if new_zoom == self._zoom:
            return
        self._zoom = new_zoom
        self._render_fast()                  # sofortiger günstiger Render
        self._smooth_timer.start()           # hochwertiger Render nach Pause
        self.zoom_changed.emit(self._zoom)

    def fit_to_window(self):
        if self._pixmap_original is None:
            return
        available = self.viewport().size()
        pixmap = self._get_rotated_pixmap()
        scale_w = available.width()  / pixmap.width()
        scale_h = available.height() / pixmap.height()
        self._set_zoom(min(scale_w, scale_h))

    def rotate(self, degrees: int = 90):
        if self._pixmap_original is None:
            return
        self._rotation = (self._rotation + degrees) % 360
        self._pixmap_rotated = None          # Cache invalidieren
        self._render_smooth()

    # ------------------------------------------------------------------ #
    # Interne Render-Methoden
    # ------------------------------------------------------------------ #

    def _set_zoom(self, factor: float):
        """Für zoom_in / zoom_out — immer direkt smooth rendern."""
        self._zoom = max(ZOOM_MIN, min(ZOOM_MAX, factor))
        self._smooth_timer.stop()
        self._render_smooth()
        self.zoom_changed.emit(self._zoom)

    def _render_fast(self):
        """Schnelle Skalierung für flüssiges Slider-Feedback."""
        if self._pixmap_original is None:
            return
        pixmap = self._get_rotated_pixmap()
        w = int(pixmap.width()  * self._zoom)
        h = int(pixmap.height() * self._zoom)
        scaled = pixmap.scaled(
            w, h,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.FastTransformation,   # günstig
        )
        self._label.setPixmap(scaled)
        self._label.resize(scaled.size())
        self.setWidgetResizable(False)

    def _render_smooth(self):
        """Hochwertige Skalierung — wird nach Slider-Pause aufgerufen."""
        if self._pixmap_original is None:
            return
        pixmap = self._get_rotated_pixmap()
        w = int(pixmap.width()  * self._zoom)
        h = int(pixmap.height() * self._zoom)
        scaled = pixmap.scaled(
            w, h,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,  # hochwertig
        )
        self._label.setPixmap(scaled)
        self._label.resize(scaled.size())
        self.setWidgetResizable(False)

    def _get_rotated_pixmap(self) -> QPixmap:
        """Gibt die rotierte Pixmap zurück — berechnet nur bei Bedarf neu."""
        if self._pixmap_rotated is None:
            transform = QTransform().rotate(self._rotation)
            self._pixmap_rotated = self._pixmap_original.transformed(
                transform, Qt.TransformationMode.SmoothTransformation
            )
        return self._pixmap_rotated

    def _build_metadata(self, filepath: str) -> dict:
        size_bytes = os.path.getsize(filepath)
        return {
            "filename": os.path.basename(filepath),
            "filepath": filepath,
            "width":    self._pixmap_original.width(),
            "height":   self._pixmap_original.height(),
            "size_kb":  round(size_bytes / 1024, 1),
        }