from typing import List

from mutagen.flac import FLAC

from song.Song import Song


class FlacSong(Song):
    _flac: FLAC
    _track_number_tags: List[str] = [
        'TRACKTOTAL',
        'TRACKNUMBER',
    ]
    _disc_number_tags: List[str] = [
        'DISCTOTAL',
        'DISCNUMBER',
    ]

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

    def set_title(self, title: str):
        self._flac['TITLE'] = [title]
        self._flac.save()

    def get_artists(self) -> List[str]:
        return self._flac.get('ARTIST')

    def set_artists(self, artists: List[str]):
        self._flac['ARTIST'] = artists

    def get_album(self) -> str:
        return self._flac.get('ALBUM')[0]

    def get_length(self) -> int:
        return self._flac.info.length

    def has_bpm(self) -> bool:
        return self._flac.get('BPM') is not None

    def set_bpm(self, bpm: int) -> None:
        self._flac['BPM'] = str(bpm)
        self._flac.save()

    def pad_track_numbers(self) -> None:
        for tag in self._track_number_tags:
            [value] = self._flac.get(tag)
            self._flac[tag] = [f'{int(value):02d}']
        self._flac.save()

    def pad_disc_numbers(self) -> None:
        for tag in self._track_number_tags:
            [value] = self._flac.get(tag)
            self._flac[tag] = [f'{int(value):02d}']
        self._flac.save()

    def fix_track_number_tags(self) -> None:
        if values := self._flac.get('totaldiscs'):
            self._flac['totaldiscs'] = []
            self._flac['DISCTOTAL'] = values
        if values := self._flac.get('discnumber'):
            self._flac['discnumber'] = []
            self._flac['DISCNUMBER'] = values
        if values := self._flac.get('totaltracks'):
            self._flac['totaltracks'] = []
            self._flac['TRACKTOTAL'] = values
        self._flac.save()
