"""
ImageStatusBar
Zeigt Dateiname (links) und einen Zoom-Regler (rechts) an.
Der Zoom-Regler besteht aus einem QSlider sowie + / − Schaltflächen.
Kommuniziert über Signale — keine Abhängigkeit zu anderen Komponenten.
"""

from PyQt6.QtWidgets import (
    QStatusBar, QLabel, QSlider, QPushButton, QWidget, QHBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSignal

ZOOM_MIN_PCT = 5      # 5 %
ZOOM_MAX_PCT = 1000   # 1000 %
ZOOM_STEP    = 15     # Schrittweite für + / −


class ImageStatusBar(QStatusBar):
    # Wird ausgelöst, wenn der Nutzer den Slider oder +/- bewegt
    zoom_requested = pyqtSignal(float)   # Faktor (z.B. 1.5 für 150 %)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizeGripEnabled(False)
        self._build_ui()

    # ------------------------------------------------------------------ #
    # UI-Aufbau
    # ------------------------------------------------------------------ #

    def _build_ui(self):
        # Linke Seite: Dateiname
        self._lbl_file = QLabel("Kein Bild geladen")
        self._lbl_file.setObjectName("status_file")
        self.addWidget(self._lbl_file, stretch=1)

        # Rechte Seite: Zoom-Steuerung als eigenes Widget
        zoom_widget = QWidget()
        zoom_widget.setObjectName("ZoomControl")
        zoom_layout = QHBoxLayout(zoom_widget)
        zoom_layout.setContentsMargins(0, 0, 0, 0)
        zoom_layout.setSpacing(4)

        self._btn_minus = QPushButton("−")
        self._btn_minus.setObjectName("zoom_btn")
        self._btn_minus.setFixedSize(22, 22)
        self._btn_minus.clicked.connect(self._on_zoom_out)

        self._slider = QSlider(Qt.Orientation.Horizontal)
        self._slider.setObjectName("zoom_slider")
        self._slider.setMinimum(ZOOM_MIN_PCT)
        self._slider.setMaximum(ZOOM_MAX_PCT)
        self._slider.setValue(100)
        self._slider.setFixedWidth(110)
        self._slider.setToolTip("Zoom")
        self._slider.valueChanged.connect(self._on_slider_changed)

        self._btn_plus = QPushButton("+")
        self._btn_plus.setObjectName("zoom_btn")
        self._btn_plus.setFixedSize(22, 22)
        self._btn_plus.clicked.connect(self._on_zoom_in)

        self._lbl_zoom = QLabel("100 %")
        self._lbl_zoom.setObjectName("zoom_label")
        self._lbl_zoom.setFixedWidth(44)
        self._lbl_zoom.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        zoom_layout.addWidget(self._btn_minus)
        zoom_layout.addWidget(self._slider)
        zoom_layout.addWidget(self._btn_plus)
        zoom_layout.addWidget(self._lbl_zoom)

        self.addPermanentWidget(zoom_widget)

    # ------------------------------------------------------------------ #
    # Öffentliche API
    # ------------------------------------------------------------------ #

    def set_filename(self, metadata: dict):
        """Aktualisiert die Dateinamen-Anzeige."""
        self._lbl_file.setText(metadata.get("filename", "—"))

    def set_zoom(self, factor: float):
        """Synchronisiert Slider und Label mit dem Viewer-Zoom."""
        pct = round(factor * 100)
        # Slider blockieren damit kein Rückkopplungsloop entsteht
        self._slider.blockSignals(True)
        self._slider.setValue(pct)
        self._slider.blockSignals(False)
        self._lbl_zoom.setText(f"{pct} %")

    # ------------------------------------------------------------------ #
    # Slots
    # ------------------------------------------------------------------ #

    def _on_slider_changed(self, value: int):
        self._lbl_zoom.setText(f"{value} %")
        self.zoom_requested.emit(value / 100.0)

    def _on_zoom_in(self):
        new_val = min(self._slider.value() + ZOOM_STEP, ZOOM_MAX_PCT)
        self._slider.setValue(new_val)

    def _on_zoom_out(self):
        new_val = max(self._slider.value() - ZOOM_STEP, ZOOM_MIN_PCT)
        self._slider.setValue(new_val)