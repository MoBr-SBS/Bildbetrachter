"""
Sidebar

Zeigt Metadaten des aktuell geladenen Bildes an und enthält die
Vorschaubilder rechts unterhalb der Dateiinfos.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QSizePolicy,
)

from .thumbnail_bar import ThumbnailBar


class Sidebar(QWidget):
    FIXED_WIDTH = 300

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
        self.setObjectName("Sidebar")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Titel
        title = QLabel("Dateiinfo")
        title.setObjectName("sidebar_title")
        layout.addWidget(title)

        subtitle = QLabel("Informationen zur aktuellen Datei")
        subtitle.setObjectName("sidebar_subtitle")
        layout.addWidget(subtitle)

        layout.addWidget(self._make_separator())

        # Infoblock
        self._lbl_name = self._make_value_label("—")
        self._lbl_size = self._make_value_label("—")
        self._lbl_dims = self._make_value_label("—")

        for key, lbl in [
            ("Name", self._lbl_name),
            ("Dateigröße", self._lbl_size),
            ("Abmessungen", self._lbl_dims),
        ]:
            layout.addWidget(self._make_key_label(key))
            layout.addWidget(lbl)

        layout.addSpacing(8)

        # Vorschau-Titel
        preview_title = QLabel("Bildvorschau")
        preview_title.setObjectName("sidebar_section_title")
        layout.addWidget(preview_title)

        preview_hint = QLabel("Alle Bilder im aktuellen Ordner")
        preview_hint.setObjectName("sidebar_section_hint")
        layout.addWidget(preview_hint)

        # Thumbnail-Bar jetzt rechts in der Sidebar
        self.thumbnail_bar = ThumbnailBar()
        self.thumbnail_bar.setObjectName("SidebarThumbnailBar")
        layout.addWidget(self.thumbnail_bar, stretch=1)

    # ------------------------------------------------------------------ #
    # Öffentliche API
    # ------------------------------------------------------------------ #
    def update_info(self, metadata: dict):
        """Aktualisiert die angezeigten Metadaten."""
        self._lbl_name.setText(metadata.get("filename", "—"))
        self._lbl_size.setText(f"{metadata.get('size_kb', '—')} KB")

        width = metadata.get("width", "?")
        height = metadata.get("height", "?")
        self._lbl_dims.setText(f"{width} × {height} px")

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
        line.setFrameShadow(QFrame.Shadow.Plain)
        return line
