"""
Sidebar
Zwei Abschnitte:
  1. Dateiinfo  — ein-/ausklappbar per Toggle-Button
  2. Vorschau   — dynamische Spaltenanzahl, anpassbare Thumbnail-Größe,
                  Lazy Loading (nur sichtbare Thumbnails werden geladen)
"""

from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QSizePolicy, QScrollArea, QGridLayout, QPushButton
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal, QTimer

THUMB_SIZE_MIN     = 56
THUMB_SIZE_MAX     = 160
THUMB_SIZE_STEP    = 16
THUMB_SIZE_DEFAULT = 56
THUMB_SPACING      = 4
SECTION_PADDING    = 12

# Millisekunden nach einem Rebuild bevor Lazy Load startet
LAZY_LOAD_DELAY_MS = 80


class Sidebar(QWidget):
    MINIMUM_WIDTH = 190

    thumbnail_clicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(self.MINIMUM_WIDTH)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        self._thumb_widgets: list[_ThumbCell] = []
        self._thumb_files:   list[Path]       = []
        self._active_index:  int              = -1
        self._thumb_size:    int              = THUMB_SIZE_DEFAULT
        self._info_visible:  bool             = True

        # Timer verzögert das Laden nach Resize/Scroll leicht
        self._lazy_timer = QTimer(self)
        self._lazy_timer.setSingleShot(True)
        self._lazy_timer.setInterval(LAZY_LOAD_DELAY_MS)
        self._lazy_timer.timeout.connect(self._load_visible_thumbs)

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
        self._info_header = self._make_section_header(
            "Dateiinfo", toggle_callback=self._toggle_info
        )
        root.addWidget(self._info_header)

        self._info_body = QWidget()
        self._info_body.setObjectName("SidebarSection")
        info_layout = QVBoxLayout(self._info_body)
        info_layout.setContentsMargins(SECTION_PADDING, 6, SECTION_PADDING, 10)
        info_layout.setSpacing(4)

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

        root.addWidget(self._info_body)
        root.addWidget(self._make_divider())

        # ── Abschnitt 2: Vorschau ─────────────────────────────────────── #
        preview_header = self._make_section_header(
            "Vorschau", size_controls=True
        )
        root.addWidget(preview_header)

        preview_body = QWidget()
        preview_body.setObjectName("SidebarSection")
        preview_layout = QVBoxLayout(preview_body)
        preview_layout.setContentsMargins(SECTION_PADDING, 6, SECTION_PADDING, 10)
        preview_layout.setSpacing(6)

        self._scroll = QScrollArea()
        self._scroll.setObjectName("ThumbScroll")
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)
        # Beim Scrollen Lazy Load auslösen
        self._scroll.verticalScrollBar().valueChanged.connect(
            lambda _: self._lazy_timer.start()
        )

        self._grid_widget = QWidget()
        self._grid_layout = QGridLayout(self._grid_widget)
        self._grid_layout.setContentsMargins(0, 0, 0, 0)
        self._grid_layout.setSpacing(THUMB_SPACING)
        self._grid_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self._scroll.setWidget(self._grid_widget)

        preview_layout.addWidget(self._scroll, stretch=1)

        self._lbl_count = QLabel("")
        self._lbl_count.setObjectName("sidebar_key")
        self._lbl_count.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.addWidget(self._lbl_count)

        root.addWidget(preview_body, stretch=1)

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
        self._thumb_files  = files
        self._active_index = active_index
        self._rebuild_grid()

    def set_active_thumbnail(self, index: int):
        if 0 <= self._active_index < len(self._thumb_widgets):
            self._thumb_widgets[self._active_index].set_active(False)
        if 0 <= index < len(self._thumb_widgets):
            self._thumb_widgets[index].set_active(True)
        self._active_index = index
        self._update_count_label()

    # ------------------------------------------------------------------ #
    # Resize — Grid und Lazy Load neu auslösen
    # ------------------------------------------------------------------ #

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._thumb_files:
            self._rebuild_grid()

    # ------------------------------------------------------------------ #
    # Slots
    # ------------------------------------------------------------------ #

    def _on_thumb_clicked(self, index: int):
        self.set_active_thumbnail(index)
        self.thumbnail_clicked.emit(index)

    def _toggle_info(self):
        self._info_visible = not self._info_visible
        self._info_body.setVisible(self._info_visible)
        self._info_header.setProperty("collapsed", not self._info_visible)
        self._info_header.style().unpolish(self._info_header)
        self._info_header.style().polish(self._info_header)
        arrow = self._info_header.findChild(QLabel, "toggle_arrow")
        if arrow:
            arrow.setText("▶" if not self._info_visible else "▼")

    def _on_thumb_size_increase(self):
        if self._thumb_size < THUMB_SIZE_MAX:
            self._thumb_size = min(self._thumb_size + THUMB_SIZE_STEP, THUMB_SIZE_MAX)
            self._rebuild_grid()

    def _on_thumb_size_decrease(self):
        if self._thumb_size > THUMB_SIZE_MIN:
            self._thumb_size = max(self._thumb_size - THUMB_SIZE_STEP, THUMB_SIZE_MIN)
            self._rebuild_grid()

    # ------------------------------------------------------------------ #
    # Grid-Logik
    # ------------------------------------------------------------------ #

    def _rebuild_grid(self):
        """Räumt den Grid auf und platziert leere Zellen. Pixmaps folgen lazy."""
        self._clear_thumbnails()

        available = self._scroll.viewport().width() - 2
        cols = max(1, available // (self._thumb_size + THUMB_SPACING))

        for i, filepath in enumerate(self._thumb_files):
            cell = _ThumbCell(filepath, i, self._thumb_size,
                              active=(i == self._active_index))
            cell.clicked.connect(self._on_thumb_clicked)
            row, col = divmod(i, cols)
            self._grid_layout.addWidget(cell, row, col)
            self._thumb_widgets.append(cell)

        self._update_count_label()
        # Kurz warten bis das Layout gesetzt ist, dann sichtbare laden
        self._lazy_timer.start()

    def _load_visible_thumbs(self):
        """Lädt Pixmaps nur für Zellen die gerade im Viewport sichtbar sind."""
        viewport_rect = self._scroll.viewport().rect()

        for cell in self._thumb_widgets:
            if cell.is_loaded():
                continue
            # Position der Zelle relativ zum Viewport
            cell_pos = cell.mapTo(self._scroll.viewport(), cell.rect().topLeft())
            cell_rect = cell.rect().translated(cell_pos)
            if viewport_rect.intersects(cell_rect):
                cell.load_pixmap()

    def _clear_thumbnails(self):
        for cell in self._thumb_widgets:
            self._grid_layout.removeWidget(cell)
            cell.deleteLater()
        self._thumb_widgets.clear()

    def _update_count_label(self):
        total = len(self._thumb_widgets)
        if total == 0:
            self._lbl_count.setText("")
            return
        self._lbl_count.setText(f"{self._active_index + 1} / {total} Bilder")

    # ------------------------------------------------------------------ #
    # UI-Hilfsmethoden
    # ------------------------------------------------------------------ #

    def _make_section_header(
        self,
        title: str,
        toggle_callback=None,
        size_controls: bool = False,
    ) -> QWidget:
        header = QWidget()
        header.setObjectName("SidebarHeader")
        layout = QHBoxLayout(header)
        layout.setContentsMargins(SECTION_PADDING, 8, 8, 8)
        layout.setSpacing(4)

        if toggle_callback:
            arrow = QLabel("▼")
            arrow.setObjectName("toggle_arrow")
            layout.addWidget(arrow)

        lbl = QLabel(title)
        lbl.setObjectName("sidebar_title")
        layout.addWidget(lbl)
        layout.addStretch()

        if size_controls:
            for symbol, slot, tip in [
                ("−", self._on_thumb_size_decrease, "Vorschau verkleinern"),
                ("+", self._on_thumb_size_increase, "Vorschau vergrößern"),
            ]:
                btn = QPushButton(symbol)
                btn.setObjectName("thumb_size_btn")
                btn.setFixedSize(20, 20)
                btn.setToolTip(tip)
                btn.clicked.connect(slot)
                layout.addWidget(btn)

        if toggle_callback:
            header.mousePressEvent = lambda _: toggle_callback()
            header.setCursor(Qt.CursorShape.PointingHandCursor)

        return header

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


# ------------------------------------------------------------------ #
# Internes Thumbnail-Widget mit Lazy Loading
# ------------------------------------------------------------------ #

class _ThumbCell(QFrame):
    clicked = pyqtSignal(int)

    def __init__(self, filepath: Path, index: int, size: int, active: bool = False):
        super().__init__()
        self._index    = index
        self._filepath = filepath
        self._size     = size
        self._loaded   = False

        self.setObjectName("ThumbCell")
        self.setFixedSize(size, size)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)

        self._lbl = QLabel()
        self._lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Platzhalter-Farbe bis das Bild geladen wird
        self._lbl.setStyleSheet("background: transparent;")
        layout.addWidget(self._lbl)

        self.set_active(active)

    def is_loaded(self) -> bool:
        return self._loaded

    def load_pixmap(self):
        """Lädt die Pixmap — wird nur aufgerufen wenn die Zelle sichtbar ist."""
        if self._loaded:
            return
        pixmap = QPixmap(str(self._filepath))
        if not pixmap.isNull():
            inner = self._size - 4
            scaled = pixmap.scaled(
                inner, inner,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self._lbl.setPixmap(scaled)
        else:
            self._lbl.setText("?")
        self._loaded = True

    def set_active(self, active: bool):
        self.setProperty("active", active)
        self.style().unpolish(self)
        self.style().polish(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self._index)
        super().mousePressEvent(event)