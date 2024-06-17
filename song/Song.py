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
    def set_bpm(self, bpm: int):
        pass

    @abstractmethod
    def pad_track_numbers(self) -> None:
        pass

    @abstractmethod
    def pad_disc_numbers(self) -> None:
        pass

    @abstractmethod
    def fix_track_number_tags(self) -> None:
        pass

    @abstractmethod
    def get_track_number(self) -> str:
        pass

    @abstractmethod
    def get_disc_number(self) -> str:
        pass
