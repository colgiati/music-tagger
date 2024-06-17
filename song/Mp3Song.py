from typing import List

from mutagen.id3 import USLT, SYLT, Encoding, TBPM
from mutagen.mp3 import MP3

from song import Song


class Mp3Song(Song):
    _mp3: MP3

    def __init__(self, path):
        super().__init__(path)
        self._mp3 = MP3(path)

    def has_lyrics(self) -> bool:
        for tag in self._mp3.tags:
            if type(self._mp3.get(tag)) in [USLT, SYLT]:
                return True
        return False

    def set_lyrics(self, lyrics: str) -> None:
        lyrics_tag = USLT(encoding=Encoding.UTF8, text=lyrics)
        self._mp3['ULST'] = lyrics_tag
        self._mp3.save()

    def get_title(self) -> str:
        return self._mp3.get('TIT2').text[0]

    def get_artists(self) -> List[str]:
        return self._mp3.get('TPE1').text[0]

    def get_album(self) -> str:
        return self._mp3.get('TALB').text[0]

    def get_length(self) -> int:
        return self._mp3.info.length

    def has_bpm(self) -> bool:
        for tag in self._mp3.tags:
            if type(self._mp3.get(tag)) == TBPM:
                return True
        return False

    def set_bpm(self, bpm: int) -> None:
        bpm_tag = TBPM(encoding=Encoding.UTF8, text=[bpm])
        self._mp3['TBPM'] = bpm_tag
        self._mp3.save()
