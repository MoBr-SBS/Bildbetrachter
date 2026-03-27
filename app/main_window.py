"""
MainWindow
Hauptfenster der Anwendung. Orchestriert alle Komponenten:
Toolbar, Bildanzeige, Sidebar (mit Vorschau) und Statusleiste.
"""

from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from app.components import ImageToolbar, ImageViewer, Sidebar, ImageStatusBar
from app.services import ImageManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bildbetrachter")
        self.resize(1060, 680)
        self._image_manager = ImageManager()
        self._build_ui()
        self._connect_signals()

    # ------------------------------------------------------------------ #
    # UI-Aufbau
    # ------------------------------------------------------------------ #

    def _build_ui(self):
        self.toolbar = ImageToolbar(self)
        self.addToolBar(self.toolbar)

        self.status_bar = ImageStatusBar(self)
        self.setStatusBar(self.status_bar)

        self.viewer = ImageViewer()
        self.sidebar = Sidebar()

        central = QWidget()
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.viewer, stretch=1)
        layout.addWidget(self.sidebar)

        self.setCentralWidget(central)

    # ------------------------------------------------------------------ #
    # Signal-Verbindungen
    # ------------------------------------------------------------------ #

    def _connect_signals(self):
        # Toolbar → Aktionen
        self.toolbar.open_requested.connect(self._on_open_requested)
        self.toolbar.zoom_in_requested.connect(self.viewer.zoom_in)
        self.toolbar.zoom_out_requested.connect(self.viewer.zoom_out)
        self.toolbar.fit_requested.connect(self.viewer.fit_to_window)
        self.toolbar.rotate_requested.connect(self.viewer.rotate)
        self.toolbar.previous_requested.connect(self._on_previous)
        self.toolbar.next_requested.connect(self._on_next)

        # Viewer → Sidebar & Statusleiste
        self.viewer.image_loaded.connect(self.sidebar.update_info)
        self.viewer.image_loaded.connect(self.status_bar.set_filename)
        self.viewer.zoom_changed.connect(self.status_bar.set_zoom)

        # Statusleiste Zoom-Slider → Viewer
        self.status_bar.zoom_requested.connect(self.viewer.set_zoom)

        # Sidebar Vorschau → Bildwechsel
        self.sidebar.thumbnail_clicked.connect(self._on_thumbnail_selected)

    # ------------------------------------------------------------------ #
    # Slots
    # ------------------------------------------------------------------ #

    def _on_open_requested(self, filepath: str):
        self._image_manager.load_directory(filepath)
        self.sidebar.load_thumbnails(
            self._image_manager.files,
            self._image_manager.current_index,
        )
        self.toolbar.enable_navigation(self._image_manager.count > 1)
        self._show_current()

    def _on_previous(self):
        self._image_manager.previous()
        self.sidebar.set_active_thumbnail(self._image_manager.current_index)
        self._show_current()

    def _on_next(self):
        self._image_manager.next()
        self.sidebar.set_active_thumbnail(self._image_manager.current_index)
        self._show_current()

    def _on_thumbnail_selected(self, index: int):
        self._image_manager.select(index)
        self._show_current()

    def _show_current(self):
        current = self._image_manager.current()
        if current:
            self.viewer.load_image(str(current))