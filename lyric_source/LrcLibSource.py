from typing import Optional

from requests import get

from lyric_source.LyricSource import LyricSource


class LrcLibSource(LyricSource):
    _base_url: str = 'https://lrclib.net/api/get'

    def get_lyrics(self, title: str, artist: str, album: str, duration: int) -> Optional[str]:
        params = {
            'track_name': title,
            'artist_name': artist,
            'album_name': album,
            'duration': duration,
        }
        response = get(self._base_url, params=params)
        body = response.json()

        if 'error' not in body and 'statusCode' not in body:
            if lyrics := body['syncedLyrics']:
                return lyrics
