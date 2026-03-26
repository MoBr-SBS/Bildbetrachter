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


class ClickableThumbnail(QFrame):
    clicked = pyqtSignal(int)

    def __init__(self, index: int, image_path: str, parent=None):
        super().__init__(parent)
        self.index = index
        self.setObjectName("ThumbnailItem")
        self.setProperty("active", False)
        self.setFixedSize(66, 66)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(0)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFixedSize(62, 62)

        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(
                58,
                58,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.label.setPixmap(pixmap)

        layout.addWidget(self.label)

    def mousePressEvent(self, event):
        self.clicked.emit(self.index)
        super().mousePressEvent(event)


class ThumbnailBar(QScrollArea):
    thumbnail_clicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("ThumbnailBar")
        self.setWidgetResizable(True)

        self.container = QWidget()
        self.container.setObjectName("ThumbnailBarContainer")
        self.grid = QGridLayout(self.container)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setHorizontalSpacing(8)
        self.grid.setVerticalSpacing(8)

        self.setWidget(self.container)

        self._items = []

    def load_thumbnails(self, files, active_index=0):
        self.clear()

        for index, file_path in enumerate(files):
            item = ClickableThumbnail(index, str(file_path))
            item.clicked.connect(self.thumbnail_clicked.emit)

            row = index // 2
            col = index % 2
            self.grid.addWidget(item, row, col)
            self._items.append(item)

        self.set_active(active_index)

    def set_active(self, index: int):
        for i, item in enumerate(self._items):
            item.setProperty("active", i == index)
            item.style().unpolish(item)
            item.style().polish(item)
            item.update()

    def clear(self):
        while self.grid.count():
            child = self.grid.takeAt(0)
            widget = child.widget()
            if widget:
                widget.deleteLater()
        self._items.clear()
