from typing import List

from mutagen.flac import FLAC

from song.Song import Song


class FlacSong(Song):
    _flac: FLAC

    def __init__(self, path: str):
        super().__init__(path)
        self._flac = FLAC(path)

    def has_lyrics(self) -> bool:
        return self._flac.get('LYRICS') is not None

    def set_lyrics(self, lyrics: str) -> None:
        self._flac['LYRICS'] = lyrics
        self._flac.save()

    def get_title(self) -> str:
        return self._flac.get('TITLE')[0]

    def get_artists(self) -> List[str]:
        return self._flac.get('ARTIST')

    def get_album(self) -> str:
        return self._flac.get('ALBUM')[0]

    def get_length(self) -> int:
        return self._flac.info.length
