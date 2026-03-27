"""
ThumbnailBar
Horizontale Leiste am unteren Rand, die Vorschaubilder des aktuellen
Ordners anzeigt. Ein Klick auf ein Thumbnail wählt das Bild aus.
"""

from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QScrollArea, QHBoxLayout, QLabel, QSizePolicy, QFrame
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal

THUMB_SIZE = 72      # Breite & Höhe eines Thumbnails in px
BAR_HEIGHT = 96      # Gesamthöhe der Leiste


class ThumbnailBar(QScrollArea):
    # Wird ausgelöst, wenn der Nutzer ein Thumbnail anklickt
    thumbnail_clicked = pyqtSignal(int)  # Index in der Dateiliste

    def __init__(self, parent=None):
        super().__init__(parent)
        self._thumbnails: list[_ThumbnailItem] = []
        self._active_index: int = -1
        self._build_ui()

    # ------------------------------------------------------------------ #
    # UI-Aufbau
    # ------------------------------------------------------------------ #

    def _build_ui(self):
        self.setFixedHeight(BAR_HEIGHT)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setObjectName("ThumbnailBar")

        self._container = QWidget()
        self._container.setObjectName("ThumbnailBarContainer")
        self._layout = QHBoxLayout(self._container)
        self._layout.setContentsMargins(8, 8, 8, 8)
        self._layout.setSpacing(6)
        self._layout.addStretch()

        self.setWidget(self._container)

    # ------------------------------------------------------------------ #
    # Öffentliche API
    # ------------------------------------------------------------------ #

    def load_thumbnails(self, files: list[Path], active_index: int) -> None:
        """Befüllt die Leiste mit Thumbnails für alle übergebenen Dateien."""
        self._clear()
        self._active_index = active_index

        for i, filepath in enumerate(files):
            item = _ThumbnailItem(filepath, i, active=(i == active_index))
            item.clicked.connect(self._on_thumbnail_clicked)
            # Stretch am Ende entfernen, Item einfügen, Stretch wieder anhängen
            self._layout.insertWidget(self._layout.count() - 1, item)
            self._thumbnails.append(item)

    def set_active(self, index: int) -> None:
        """Markiert das Thumbnail am gegebenen Index als aktiv."""
        if self._active_index == index:
            return
        # Altes aktives Thumbnail deaktivieren
        if 0 <= self._active_index < len(self._thumbnails):
            self._thumbnails[self._active_index].set_active(False)
        # Neues aktivieren und in den sichtbaren Bereich scrollen
        if 0 <= index < len(self._thumbnails):
            self._thumbnails[index].set_active(True)
            self.ensureWidgetVisible(self._thumbnails[index])
        self._active_index = index

    # ------------------------------------------------------------------ #
    # Slots
    # ------------------------------------------------------------------ #

    def _on_thumbnail_clicked(self, index: int) -> None:
        self.set_active(index)
        self.thumbnail_clicked.emit(index)

    # ------------------------------------------------------------------ #
    # Hilfsmethoden
    # ------------------------------------------------------------------ #

    def _clear(self) -> None:
        """Entfernt alle vorhandenen Thumbnails aus dem Layout."""
        for item in self._thumbnails:
            self._layout.removeWidget(item)
            item.deleteLater()
        self._thumbnails.clear()


class _ThumbnailItem(QFrame):
    """Einzelnes Thumbnail-Widget mit Klick-Signal."""
    clicked = pyqtSignal(int)  # Index

    def __init__(self, filepath: Path, index: int, active: bool = False):
        super().__init__()
        self._index = index
        self._active = False
        self._build_ui(filepath)
        self.set_active(active)

    def _build_ui(self, filepath: Path):
        self.setFixedSize(THUMB_SIZE, THUMB_SIZE)
        self.setObjectName("ThumbnailItem")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)

        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        # Pixmap laden und skalieren
        pixmap = QPixmap(str(filepath))
        if not pixmap.isNull():
            scaled = pixmap.scaled(
                THUMB_SIZE - 4, THUMB_SIZE - 4,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            label.setPixmap(scaled)
        else:
            label.setText("?")

        layout.addWidget(label)

    def set_active(self, active: bool) -> None:
        self._active = active
        # Aktivzustand über Property im QSS steuerbar machen
        self.setProperty("active", active)
        self.style().unpolish(self)
        self.style().polish(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self._index)
        super().mousePressEvent(event)