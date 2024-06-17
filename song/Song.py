from abc import ABC, abstractmethod
from typing import List


class Song(ABC):
    _path: str

    def __init__(self, path: str):
        self._path = path

    @property
    def path(self) -> str:
        return self._path

    @abstractmethod
    def has_lyrics(self) -> bool:
        pass

    @abstractmethod
    def set_lyrics(self, lyrics: str) -> None:
        pass

    @abstractmethod
    def get_title(self) -> str:
        pass

    @abstractmethod
    def set_title(self, title: str):
        pass

    @abstractmethod
    def get_artists(self) -> List[str]:
        pass

    @abstractmethod
    def set_artists(self, artists: List[str]):
        pass

    @abstractmethod
    def get_album(self) -> str:
        pass

    @abstractmethod
    def get_length(self) -> int:
        pass

    @abstractmethod
    def has_bpm(self) -> bool:
        pass

    @abstractmethod
    def set_bpm(self, bpm: int) -> None:
        pass
