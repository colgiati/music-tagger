from abc import ABC, abstractmethod
from typing import Optional


class LyricSource(ABC):

    @abstractmethod
    def get_lyrics(self, title: str, artist: str, album: str, duration: int) -> Optional[str]:
        pass


