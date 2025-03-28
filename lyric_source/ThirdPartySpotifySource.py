from json import JSONDecodeError
from typing import Optional

from requests import get

from lyric_source import LyricSource


class ThirdPartySpotifySource(LyricSource):
    _base_url = 'https://lyrichub.vercel.app/api/spotify'

    def get_lyrics(self, title: str, artist: str, album: str, duration: int) -> Optional[str]:
        params = {
            'query': f'{title} {artist}',
        }
        response = get(f'{self._base_url}', params=params)
        try:
            json = response.json()
            if json['lyrics'] != 'Not Found.':
                return json['lyrics']
        except JSONDecodeError:
            return None
