from datetime import datetime
from typing import Optional

from requests import get, JSONDecodeError, Response

from lyric_source.LyricSource import LyricSource

_user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
               'AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/119.0.0.0 Safari/537.36')


class SpotifySource(LyricSource):
    _access_token_url = 'https://open.spotify.com/get_access_token'
    _lyrics_api_url = 'https://spotify-lyrics-api-cyan.vercel.app/'
    _base_url: str = 'https://api.spotify.com/v1/'
    _token: str
    _token_time: Optional[int] = None

    def __init__(self):
        self._refresh_token()

    def get_lyrics(self, title: str, artist: str, album: str, duration: int) -> Optional[str]:
        song_url = self._get_song_url(title, artist, duration * 1000)
        if not song_url:
            return None

        params = {'url': song_url, 'format': 'rlc'}
        response = get(self._lyrics_api_url, params=params)
        return self._handle_lyric_response(response)

    def _handle_lyric_response(self, response: Response) -> Optional[str]:
        if response.status_code != 200:
            return None
        try:
            body = response.json()
            if not body['error']:
                lines = body['lines']
                lines = map(lambda x: f'{self._transform_time(int(x["startTimeMs"]))}{x["words"]}', lines)
                return '\n'.join(lines)
        except JSONDecodeError:
            return None
        return None

    def _get_song_url(self, song_name: str, artist_name: str, duration: int) -> Optional[str]:
        self._refresh_token()

        params = {'q': f'{song_name} {artist_name}', 'type': 'track', 'limit': 1, 'offset': 0}
        headers = {'Authorization': f'Bearer {self._token}'}
        response = get(f'{self._base_url}search', params=params, headers=headers)
        body = response.json()

        if 'tracks' in body and body['tracks']['items']:
            track_duration = body['tracks']['items'][0]['duration_ms']
            if duration - 5000 <= track_duration <= duration + 5000:
                return body['tracks']['items'][0]['external_urls']['spotify']

    def _refresh_token(self):
        if self._token_time and datetime.now().toordinal() - self._token_time <= 30 * 60 * 1000:  # 30 minutes
            return

        params = {'reason': 'transport', 'productType': 'web_player'}
        headers = {'User-Agent': _user_agent}
        response = get(self._access_token_url, params=params, headers=headers)
        body = response.json()

        self._token = body['accessToken']
        self._token_time = datetime.now().toordinal()

    @classmethod
    def _transform_time(cls, time_ms: int) -> str:
        ms = time_ms % 1000
        time_s = time_ms // 1000
        s = time_s % 60
        m = time_s // 60
        return f'[{m:02d}:{s:02d}.{ms:02d}]'
