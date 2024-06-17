from abc import ABC, abstractmethod

from song import Song, FlacSong, Mp3Song


class TagComponent(ABC):
    _depth: int

    def tag(self, path: str, depth: int):
        self._depth = depth
        song = self._get_song(path)
        if song is not None:
            self._tag(song)

    @classmethod
    def _get_song(cls, path: str):
        if path.endswith('.flac'):
            return FlacSong(path)
        elif path.endswith('.mp3'):
            return Mp3Song(path)
        return None

    @abstractmethod
    def _tag(self, song: Song):
        pass
