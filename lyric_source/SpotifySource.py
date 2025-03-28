import base64
from datetime import datetime
from typing import Optional, Dict
from pyotp import TOTP
from requests import get, JSONDecodeError, Response

from lyric_source.LyricSource import LyricSource

_user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
               'AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/119.0.0.0 Safari/537.36')


class SpotifySource(LyricSource):
    _player_url = 'https://open.spotify.com/'
    _lyrics_api_url = 'https://spotify-lyrics-api-cyan.vercel.app/'
    _base_url: str = 'https://api.spotify.com/v1/'
    _sp_dc: str
    _token: Optional[str] = None
    _token_time: Optional[int] = None

    def __init__(self, sp_dc):
        self._sp_dc = sp_dc
        self._refresh_token()

    def get_lyrics(self, title: str, artist: str, album: str, duration: int) -> Optional[str]:
        song_id = self._get_song_id(title, artist, duration * 1000)
        if not song_id:
            return None

        url = f'https://spclient.wg.spotify.com/color-lyrics/v2/track/{song_id}?format=json&vocalRemoval=false&market=from_token'
        response = get(url, headers=self._get_headers())
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

    def _get_song_id(self, song_name: str, artist_name: str, duration: int) -> Optional[str]:
        self._refresh_token()

        params = {'q': f'{song_name} {artist_name}', 'type': 'track', 'limit': 1, 'offset': 0}
        headers = {'Authorization': f'Bearer {self._token}'}
        response = get(f'{self._base_url}search', params=params, headers=headers)
        body = response.json()

        if 'tracks' in body and body['tracks']['items']:
            track_duration = body['tracks']['items'][0]['duration_ms']
            if duration - 5000 <= track_duration <= duration + 5000:
                return body['tracks']['items'][0]['id']

    def _refresh_token(self):
        if self._token_time and datetime.now().toordinal() - self._token_time <= 30 * 60 * 1000:  # 30 minutes
            return

        server_time = self._get_server_time()
        totp_generator = TOTP(self._get_key())
        totp = totp_generator.at(server_time)

        params = self._get_params(server_time * 1000, totp, reason='init')
        headers = self._get_headers()
        response = get(f'{self._player_url}/get_access_token', params=params, headers=headers)
        body = response.json()

        self._token = body['accessToken']
        self._token_time = datetime.now().toordinal()

    def _get_server_time(self) -> int:
        headers = self._get_headers()
        response = get(f'{self._player_url}/server-time', headers=headers)
        return response.json()['serverTime']

    def _get_headers(self, sp_dc: Optional[str] = None) -> Dict:
        headers = {
            'referer': 'https://open.spotify.com/',
            'origin': 'https://open.spotify.com/',
            'accept': 'application/json',
            'app-platform': 'WebPlayer',
            'spotify-app-version': '1.2.61.20.g3b4cd5b2',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        }
        if self._token:
            headers['authorization'] = f'Bearer {self._token}'
        if sp_dc:
            headers['Cookie'] = f'sp_dc={self._sp_dc}'
        return headers

    @classmethod
    def _get_params(cls, server_time: int, totp: str, reason: str = 'transport') -> Dict:
        return {
            'reason': reason,
            'productType': 'mobile-web-player',
            'totp': totp,
            'ts': server_time,
            'totpVer': 5,
        }

    @classmethod
    def _get_key(cls) -> str:
        secret = '35353037313435383533343837343939353932323438363330333239333437'
        return base64.b32encode(bytearray.fromhex(secret)).decode('utf-8')
