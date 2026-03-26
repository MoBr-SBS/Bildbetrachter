"""
Sidebar
Zeigt Metadaten des aktuell geladenen Bildes an.
Empfängt ein Dict via update_info() — kennt keine anderen Komponenten.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QSizePolicy
)


class Sidebar(QWidget):
    FIXED_WIDTH = 180

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(self.FIXED_WIDTH)
        self.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Expanding,
        )
        self._build_ui()

    # ------------------------------------------------------------------ #
    # UI-Aufbau
    # ------------------------------------------------------------------ #

    def _build_ui(self):
        self.setObjectName("Sidebar")   # Ziel für QWidget#Sidebar im QSS

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)

        title = QLabel("Dateiinfo")
        title.setObjectName("sidebar_title")
        layout.addWidget(title)
        layout.addWidget(self._make_separator())

        self._lbl_name = self._make_value_label("—")
        self._lbl_size = self._make_value_label("—")
        self._lbl_dims = self._make_value_label("—")

        for key, lbl in [
            ("Name",         self._lbl_name),
            ("Dateigröße",   self._lbl_size),
            ("Abmessungen",  self._lbl_dims),
        ]:
            layout.addWidget(self._make_key_label(key))
            layout.addWidget(lbl)

        layout.addStretch()

    # ------------------------------------------------------------------ #
    # Öffentliche API
    # ------------------------------------------------------------------ #

    def update_info(self, metadata: dict):
        """Aktualisiert die angezeigten Metadaten."""
        self._lbl_name.setText(metadata.get("filename", "—"))
        self._lbl_size.setText(f"{metadata.get('size_kb', '—')} KB")
        w = metadata.get("width", "?")
        h = metadata.get("height", "?")
        self._lbl_dims.setText(f"{w} × {h} px")

    # ------------------------------------------------------------------ #
    # Hilfsmethoden
    # ------------------------------------------------------------------ #

    @staticmethod
    def _make_key_label(text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("sidebar_key")
        return lbl

    @staticmethod
    def _make_value_label(text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("sidebar_value")
        lbl.setWordWrap(True)
        return lbl

    @staticmethod
    def _make_separator() -> QFrame:
        line = QFrame()
        line.setObjectName("sidebar_separator")
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        return line