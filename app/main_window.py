"""
MainWindow
Hauptfenster der Anwendung. Orchestriert alle Komponenten:
Toolbar, Bildanzeige, Sidebar, Statusleiste und Thumbnail-Leiste.
"""

from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout

from app.components import ImageToolbar, ImageViewer, Sidebar, ImageStatusBar, ThumbnailBar
from app.services import ImageManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bildbetrachter")
        self.resize(1000, 700)
        self._image_manager = ImageManager()
        self._build_ui()
        self._connect_signals()

    # ------------------------------------------------------------------ #
    # UI-Aufbau
    # ------------------------------------------------------------------ #

    def _build_ui(self):
        # Toolbar (oben)
        self.toolbar = ImageToolbar(self)
        self.addToolBar(self.toolbar)

        # Statusleiste (unten)
        self.status_bar = ImageStatusBar(self)
        self.setStatusBar(self.status_bar)

        # Bildanzeige + Sidebar nebeneinander
        self.viewer = ImageViewer()
        self.sidebar = Sidebar()

        viewer_row = QWidget()
        viewer_layout = QHBoxLayout(viewer_row)
        viewer_layout.setContentsMargins(0, 0, 0, 0)
        viewer_layout.setSpacing(0)
        viewer_layout.addWidget(self.viewer, stretch=1)
        viewer_layout.addWidget(self.sidebar)

        # Thumbnail-Leiste unterhalb der Bildanzeige
        self.thumbnail_bar = ThumbnailBar()

        # Alles in eine vertikale Anordnung
        central = QWidget()
        central_layout = QVBoxLayout(central)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)
        central_layout.addWidget(viewer_row, stretch=1)
        central_layout.addWidget(self.thumbnail_bar)

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

        # Viewer → Statusleiste & Sidebar
        self.viewer.image_loaded.connect(self.sidebar.update_info)
        self.viewer.image_loaded.connect(self.status_bar.set_filename)
        self.viewer.zoom_changed.connect(self.status_bar.set_zoom)

        # Thumbnail-Leiste → Bildwechsel
        self.thumbnail_bar.thumbnail_clicked.connect(self._on_thumbnail_selected)

    # ------------------------------------------------------------------ #
    # Slots
    # ------------------------------------------------------------------ #

    def _on_open_requested(self, filepath: str):
        """Datei öffnen: Ordner einlesen, Thumbnails laden, Bild anzeigen."""
        self._image_manager.load_directory(filepath)
        self.thumbnail_bar.load_thumbnails(
            self._image_manager.files,
            self._image_manager.current_index,
        )
        self.toolbar.enable_navigation(self._image_manager.count > 1)
        self._show_current()

    def _on_previous(self):
        self._image_manager.previous()
        self.thumbnail_bar.set_active(self._image_manager.current_index)
        self._show_current()

    def _on_next(self):
        self._image_manager.next()
        self.thumbnail_bar.set_active(self._image_manager.current_index)
        self._show_current()

    def _on_thumbnail_selected(self, index: int):
        self._image_manager.select(index)
        self._show_current()

    def _show_current(self):
        """Lädt das aktuell im ImageManager ausgewählte Bild in den Viewer."""
        current = self._image_manager.current()
        if current:
            self.viewer.load_image(str(current))