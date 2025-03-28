from abc import ABC, abstractmethod
from typing import Optional


class LyricSource(ABC):

    @abstractmethod
    def get_lyrics(self, title: str, artist: str, album: str, duration: int) -> Optional[str]:
        pass

    @classmethod
    def _transform_time(cls, time_ms: int) -> str:
        ms = time_ms % 1000
        time_s = time_ms // 1000
        s = time_s % 60
        m = time_s // 60
        return f'[{m:02d}:{s:02d}.{ms:03d}]'


