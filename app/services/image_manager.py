"""
ImageManager
Verwaltet die Liste der Bilddateien eines Ordners und den aktuellen Index.
Enthält keinerlei UI-Code — reine Anwendungslogik.
"""

import os
from pathlib import Path

# Alle Dateierweiterungen, die als Bilder behandelt werden
SUPPORTED_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".tif", ".webp"
}


class ImageManager:
    def __init__(self):
        self._files: list[Path] = []
        self._index: int = -1

    # ------------------------------------------------------------------ #
    # Öffentliche API
    # ------------------------------------------------------------------ #

    def load_directory(self, filepath: str) -> None:
        """
        Lädt alle Bilder aus dem Ordner der angegebenen Datei
        und setzt den Index auf diese Datei.
        """
        path = Path(filepath)
        directory = path.parent

        self._files = sorted(
            [
                f for f in directory.iterdir()
                if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
            ],
            key=lambda f: f.name.lower(),
        )

        # Index auf die ursprünglich geöffnete Datei setzen
        try:
            self._index = self._files.index(path)
        except ValueError:
            self._index = 0

    def current(self) -> Path | None:
        """Gibt die aktuell ausgewählte Bilddatei zurück."""
        if not self._files:
            return None
        return self._files[self._index]

    def next(self) -> Path | None:
        """Wechselt zum nächsten Bild und gibt es zurück."""
        if not self._files:
            return None
        self._index = (self._index + 1) % len(self._files)
        return self.current()

    def previous(self) -> Path | None:
        """Wechselt zum vorherigen Bild und gibt es zurück."""
        if not self._files:
            return None
        self._index = (self._index - 1) % len(self._files)
        return self.current()

    def select(self, index: int) -> Path | None:
        """Wählt ein Bild per Index aus und gibt es zurück."""
        if not self._files or not (0 <= index < len(self._files)):
            return None
        self._index = index
        return self.current()

    @property
    def files(self) -> list[Path]:
        """Alle Bilddateien im aktuellen Ordner."""
        return self._files

    @property
    def current_index(self) -> int:
        """Index des aktuell angezeigten Bildes."""
        return self._index

    @property
    def count(self) -> int:
        """Anzahl der Bilder im Ordner."""
        return len(self._files)

    def has_previous(self) -> bool:
        return self.count > 1

    def has_next(self) -> bool:
        return self.count > 1