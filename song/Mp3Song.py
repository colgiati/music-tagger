from typing import List

from mutagen.id3 import USLT, SYLT, Encoding, TBPM, TIT2, TPE1, TPOS, TRCK, TXXX
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

    def set_title(self, title: str):
        title_tag = TIT2(Encoding.UTF8, text=[title])
        self._mp3['TIT2'] = title_tag
        self._mp3.save()

    def get_artists(self) -> List[str]:
        return self._mp3.get('TPE1').text

    def set_artists(self, artists: List[str]):
        artists_tag = TPE1(encoding=Encoding.UTF8, text=artists)
        self._mp3['TPE1'] = artists_tag
        self._mp3.save()

    def get_album(self) -> str:
        return self._mp3.get('TALB').text[0]

    def get_length(self) -> int:
        return self._mp3.info.length

    def has_bpm(self) -> bool:
        for tag in self._mp3.tags:
            if type(self._mp3.get(tag)) == TBPM:
                return True
        return False

    def set_bpm(self, bpm: int):
        bpm_tag = TBPM(encoding=Encoding.UTF8, text=[bpm])
        self._mp3['TBPM'] = bpm_tag
        self._mp3.save()

    def pad_track_numbers(self) -> None:
        track_numbers = self._mp3.get('TRCK').text[0]
        [current, total] = track_numbers.split('/')
        disc_number_tag = TRCK(encoding=Encoding.UTF8, text=[f'{int(current):02d}/{int(total):02d}'])
        self._mp3['TRCK'] = disc_number_tag
        self._mp3.save()

    def pad_disc_numbers(self) -> None:
        disc_numbers = self._mp3.get('TPOS').text[0]
        [current, total] = disc_numbers.split('/')
        disc_number_tag = TPOS(encoding=Encoding.UTF8, text=[f'{int(current):02d}/{int(total):02d}'])
        self._mp3['TPOS'] = disc_number_tag
        if self._mp3.get('TXXX:DISCTOTAL'):
            total_disc_number = self._mp3.get('TXXX:DISCTOTAL').text[0]
            total_disc_number_tag = TXXX(encoding=Encoding.UTF8, desc='DISCTOTAL',
                                         text=[f'{int(total_disc_number):02d}'])
            self._mp3['TXXX:DISCTOTAL'] = total_disc_number_tag
        self._mp3.save()

    def fix_track_number_tags(self) -> None:
        pass

    def get_track_number(self) -> str:
        track_numbers = self._mp3.get('TRCK').text[0]
        [current, _] = track_numbers.split('/')
        return current

    def get_disc_number(self) -> str:
        disc_numbers = self._mp3.get('TPOS').text[0]
        [current, _] = disc_numbers.split('/')
        return current
