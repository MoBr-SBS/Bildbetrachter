"""
ThumbnailBar

Zeigt Vorschaubilder als 2-spaltiges Raster in der Sidebar.
"""

from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QScrollArea,
    QWidget,
    QGridLayout,
    QFrame,
    QLabel,
    QVBoxLayout,
)


THUMB_SIZE = 64
THUMB_COLUMNS = 2


class ClickableThumbnail(QFrame):
    clicked = pyqtSignal(int)

    def __init__(self, index: int, image_path: str, parent=None):
        super().__init__(parent)
        self.index = index

        self.setObjectName("ThumbnailItem")
        self.setProperty("active", False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(THUMB_SIZE, THUMB_SIZE)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(0)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFixedSize(THUMB_SIZE - 4, THUMB_SIZE - 4)

        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(
                THUMB_SIZE - 8,
                THUMB_SIZE - 8,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.label.setPixmap(pixmap)

        layout.addWidget(self.label)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.index)
        super().mousePressEvent(event)


class ThumbnailBar(QScrollArea):
    thumbnail_clicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("ThumbnailBar")
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setFrameShape(QScrollArea.Shape.NoFrame)

        self.container = QWidget()
        self.container.setObjectName("ThumbnailBarContainer")

        self.grid = QGridLayout(self.container)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setHorizontalSpacing(8)
        self.grid.setVerticalSpacing(8)

        self.setWidget(self.container)

        self._items: list[ClickableThumbnail] = []

    def load_thumbnails(self, files: list[Path], active_index: int = 0) -> None:
        self.clear()

        for index, file_path in enumerate(files):
            item = ClickableThumbnail(index, str(file_path))
            item.clicked.connect(self.thumbnail_clicked.emit)

            row = index // THUMB_COLUMNS
            col = index % THUMB_COLUMNS

            self.grid.addWidget(item, row, col)
            self._items.append(item)

        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 1)

        self.set_active(active_index)

    def set_active(self, index: int) -> None:
        for i, item in enumerate(self._items):
            item.setProperty("active", i == index)
            item.style().unpolish(item)
            item.style().polish(item)
            item.update()

    def clear(self) -> None:
        while self.grid.count():
            child = self.grid.takeAt(0)
            widget = child.widget()
            if widget is not None:
                widget.deleteLater()
        self._items.clear()
