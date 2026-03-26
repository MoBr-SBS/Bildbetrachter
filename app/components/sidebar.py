"""
Sidebar

Kompakte rechte Seitenleiste:
- DATEIINFO oben
- Werte direkt rechts neben den Labels
- VORSCHAU darunter als 2-spaltiges Raster
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QGridLayout,
    QFrame,
    QSizePolicy,
)

from .thumbnail_bar import ThumbnailBar


class Sidebar(QWidget):
    FIXED_WIDTH = 220

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("Sidebar")
        self.setFixedWidth(self.FIXED_WIDTH)
        self.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Expanding,
        )

        self._build_ui()

    def _build_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(12, 12, 12, 12)
        outer_layout.setSpacing(10)

        self.info_title = QLabel("DATEIINFO")
        self.info_title.setObjectName("sidebar_section_header")
        outer_layout.addWidget(self.info_title)

        info_frame = QFrame()
        info_frame.setObjectName("sidebar_info_frame")
        outer_layout.addWidget(info_frame)

        info_grid = QGridLayout(info_frame)
        info_grid.setContentsMargins(0, 0, 0, 0)
        info_grid.setHorizontalSpacing(10)
        info_grid.setVerticalSpacing(4)

        self.lbl_name_key = self._make_key_label("Name")
        self.lbl_size_key = self._make_key_label("Größe")
        self.lbl_width_key = self._make_key_label("Breite")
        self.lbl_height_key = self._make_key_label("Höhe")

        self.lbl_name_val = self._make_value_label("—")
        self.lbl_size_val = self._make_value_label("—")
        self.lbl_width_val = self._make_value_label("—")
        self.lbl_height_val = self._make_value_label("—")

        info_grid.addWidget(self.lbl_name_key, 0, 0)
        info_grid.addWidget(self.lbl_name_val, 0, 1)

        info_grid.addWidget(self.lbl_size_key, 1, 0)
        info_grid.addWidget(self.lbl_size_val, 1, 1)

        info_grid.addWidget(self.lbl_width_key, 2, 0)
        info_grid.addWidget(self.lbl_width_val, 2, 1)

        info_grid.addWidget(self.lbl_height_key, 3, 0)
        info_grid.addWidget(self.lbl_height_val, 3, 1)

        info_grid.setColumnStretch(0, 0)
        info_grid.setColumnStretch(1, 1)

        self.preview_title = QLabel("VORSCHAU")
        self.preview_title.setObjectName("sidebar_section_header")
        outer_layout.addWidget(self.preview_title)

        self.thumbnail_bar = ThumbnailBar()
        self.thumbnail_bar.setObjectName("SidebarThumbnailBar")
        outer_layout.addWidget(self.thumbnail_bar, stretch=1)

    def update_info(self, metadata: dict):
        filename = metadata.get("filename", "—")
        size_kb = metadata.get("size_kb", "—")
        width = metadata.get("width", "—")
        height = metadata.get("height", "—")

        self.lbl_name_val.setText(str(filename))
        self.lbl_size_val.setText(f"{size_kb} KB")
        self.lbl_width_val.setText(f"{width} px")
        self.lbl_height_val.setText(f"{height} px")

    @staticmethod
    def _make_key_label(text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("sidebar_key")
        return label

    @staticmethod
    def _make_value_label(text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("sidebar_value")
        label.setWordWrap(True)
        return label
