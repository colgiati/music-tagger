from typing import Optional

from requests import get

from lyric_source import LyricSource


class MusixmatchSource(LyricSource):
    _base_url = 'https://kerollosy.vercel.app'

    def get_lyrics(self, title: str, artist: str, album: str, duration: int) -> Optional[str]:
        params = {
            'artist': artist,
            'track': title,
        }
        response = get(f'{self._base_url}/full', params=params)
        if not response.ok:
            return None
        json = response.json()
        if json['hasSyncedLyrics']:
            return json['syncedLyrics']['lyrics']
        return None
