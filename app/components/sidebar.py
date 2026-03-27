"""
Sidebar
Zeigt zwei visuelle Abschnitte:
  1. Dateiinfo  — Name, Größe, Abmessungen
  2. Vorschau   — Thumbnail-Grid der Bilder im Ordner

Kommuniziert nach außen über Signale.
"""

from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame,
    QSizePolicy, QScrollArea, QGridLayout
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal

THUMB_SIZE = 56


class Sidebar(QWidget):
    FIXED_WIDTH = 190

    thumbnail_clicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(self.FIXED_WIDTH)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self._thumb_widgets: list[_ThumbCell] = []
        self._active_index: int = -1
        self._build_ui()

    # ------------------------------------------------------------------ #
    # UI-Aufbau
    # ------------------------------------------------------------------ #

    def _build_ui(self):
        self.setObjectName("Sidebar")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Abschnitt 1: Dateiinfo ────────────────────────────────────── #
        info_widget = QWidget()
        info_widget.setObjectName("SidebarSection")
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(12, 10, 12, 10)
        info_layout.setSpacing(4)
        info_layout.addWidget(self._make_section_title("Dateiinfo"))

        self._lbl_name = self._make_value_label("—")
        self._lbl_size = self._make_value_label("—")
        self._lbl_dims = self._make_value_label("—")

        for key, lbl in [
            ("Name",        self._lbl_name),
            ("Dateigröße",  self._lbl_size),
            ("Abmessungen", self._lbl_dims),
        ]:
            info_layout.addWidget(self._make_key_label(key))
            info_layout.addWidget(lbl)

        root.addWidget(info_widget)
        root.addWidget(self._make_divider())

        # ── Abschnitt 2: Vorschau ─────────────────────────────────────── #
        preview_widget = QWidget()
        preview_widget.setObjectName("SidebarSection")
        preview_layout = QVBoxLayout(preview_widget)
        preview_layout.setContentsMargins(12, 10, 12, 10)
        preview_layout.setSpacing(6)
        preview_layout.addWidget(self._make_section_title("Vorschau"))

        scroll = QScrollArea()
        scroll.setObjectName("ThumbScroll")
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        self._grid_widget = QWidget()
        self._grid_layout = QGridLayout(self._grid_widget)
        self._grid_layout.setContentsMargins(0, 0, 0, 0)
        self._grid_layout.setSpacing(4)
        scroll.setWidget(self._grid_widget)

        preview_layout.addWidget(scroll, stretch=1)

        self._lbl_count = QLabel("")
        self._lbl_count.setObjectName("sidebar_key")
        self._lbl_count.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.addWidget(self._lbl_count)

        root.addWidget(preview_widget, stretch=1)

    # ------------------------------------------------------------------ #
    # Öffentliche API
    # ------------------------------------------------------------------ #

    def update_info(self, metadata: dict):
        self._lbl_name.setText(metadata.get("filename", "—"))
        self._lbl_size.setText(f"{metadata.get('size_kb', '—')} KB")
        w = metadata.get("width", "?")
        h = metadata.get("height", "?")
        self._lbl_dims.setText(f"{w} × {h} px")

    def load_thumbnails(self, files: list[Path], active_index: int):
        self._clear_thumbnails()
        self._active_index = active_index
        cols = 2

        for i, filepath in enumerate(files):
            cell = _ThumbCell(filepath, i, active=(i == active_index))
            cell.clicked.connect(self._on_thumb_clicked)
            row, col = divmod(i, cols)
            self._grid_layout.addWidget(cell, row, col)
            self._thumb_widgets.append(cell)

        total = len(files)
        pos = active_index + 1 if total > 0 else 0
        self._lbl_count.setText(f"{pos} / {total} Bilder")

    def set_active_thumbnail(self, index: int):
        if 0 <= self._active_index < len(self._thumb_widgets):
            self._thumb_widgets[self._active_index].set_active(False)
        if 0 <= index < len(self._thumb_widgets):
            self._thumb_widgets[index].set_active(True)
        self._active_index = index
        total = len(self._thumb_widgets)
        self._lbl_count.setText(f"{index + 1} / {total} Bilder")

    # ------------------------------------------------------------------ #
    # Slots
    # ------------------------------------------------------------------ #

    def _on_thumb_clicked(self, index: int):
        self.set_active_thumbnail(index)
        self.thumbnail_clicked.emit(index)

    # ------------------------------------------------------------------ #
    # Hilfsmethoden
    # ------------------------------------------------------------------ #

    def _clear_thumbnails(self):
        for cell in self._thumb_widgets:
            self._grid_layout.removeWidget(cell)
            cell.deleteLater()
        self._thumb_widgets.clear()

    @staticmethod
    def _make_section_title(text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("sidebar_title")
        return lbl

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
    def _make_divider() -> QFrame:
        line = QFrame()
        line.setObjectName("sidebar_separator")
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Plain)
        return line


class _ThumbCell(QFrame):
    clicked = pyqtSignal(int)

    def __init__(self, filepath: Path, index: int, active: bool = False):
        super().__init__()
        self._index = index
        self.setObjectName("ThumbCell")
        self.setFixedSize(THUMB_SIZE, THUMB_SIZE)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)

        lbl = QLabel()
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap(str(filepath))
        if not pixmap.isNull():
            scaled = pixmap.scaled(
                THUMB_SIZE - 4, THUMB_SIZE - 4,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            lbl.setPixmap(scaled)
        else:
            lbl.setText("?")

        layout.addWidget(lbl)
        self.set_active(active)

    def set_active(self, active: bool):
        self.setProperty("active", active)
        self.style().unpolish(self)
        self.style().polish(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self._index)
        super().mousePressEvent(event)