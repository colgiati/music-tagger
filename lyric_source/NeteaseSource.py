from json import JSONDecodeError
from typing import Optional, Dict, Union

from requests import get

from lyric_source import LyricSource


class NeteaseSource(LyricSource):
    _base_url = "https://music.163.com/api/"

    def get_lyrics(self, title: str, artist: str, album: str, duration: int) -> Optional[str]:
        song_id = self._get_song_id(title, artist, duration * 1000)
        if song_id is None:
            return None
        return self._get_lyrics(song_id)

    def _get_song_id(self, title: str, artist: str, duration: int) -> Optional[int]:
        query = f'{title} {artist}'
        response = get(
            url=f'{self._base_url}search/pc',
            headers=self._get_headers(),
            params=self._get_params_for_song_id(query)
        )
        json = response.json()
        song = json['result']['songs'][0]
        if duration - 2500 <= song['duration'] <= duration + 2500:
            return song['id']
        return None

    def _get_lyrics(self, song_id: int) -> Optional[str]:
        response = get(
            url=f'{self._base_url}song/lyric',
            headers=self._get_headers(),
            params=self._get_params_for_lyrics(song_id)
        )
        try:
            json = response.json()
            if json['lrc']['lyric'] == '':
                return None
            return json['lrc']['lyric']
        except JSONDecodeError:
            return None

    @classmethod
    def _get_params_for_song_id(cls, query: str, offset: int = 0) -> Dict[str, Union[str, int]]:
        return {
            'limit': 1,
            'type': 1,
            'offset': offset,
            's': query,
        }

    @classmethod
    def _get_params_for_lyrics(cls, song_id: int) -> Dict[str, Union[str, int]]:
        return {
            'id': song_id,
            'lv': 1,
            'tv': 1,
            'rv': 1,
        }

    @classmethod
    def _get_headers(cls) -> Dict[str, str]:
        return {
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9,fa;q=0.8",
            "Cache-Control": "max-age=0",
            "Sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            "Sec-ch-ua-mobile": "?0",
            "Sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "Cookie": "NMTID=00OAVK3xqDG726ITU6jopU6jF2yMk0AAAGCO8l1BA; JSESSIONID-WYYY=8KQo11YK2GZP45RMlz8Kn80vHZ9%2FGvwzRKQXXy0iQoFKycWdBlQjbfT0MJrFa6hwRfmpfBYKeHliUPH287JC3hNW99WQjrh9b9RmKT%2Fg1Exc2VwHZcsqi7ITxQgfEiee50po28x5xTTZXKoP%2FRMctN2jpDeg57kdZrXz%2FD%2FWghb%5C4DuZ%3A1659124633932; _iuqxldmzr_=32; _ntes_nnid=0db6667097883aa9596ecfe7f188c3ec,1659122833973; _ntes_nuid=0db6667097883aa9596ecfe7f188c3ec; WNMCID=xygast.1659122837568.01.0; WEVNSM=1.0.0; WM_NI=CwbjWAFbcIzPX3dsLP%2F52VB%2Bxr572gmqAYwvN9KU5X5f1nRzBYl0SNf%2BV9FTmmYZy%2FoJLADaZS0Q8TrKfNSBNOt0HLB8rRJh9DsvMOT7%2BCGCQLbvlWAcJBJeXb1P8yZ3RHA%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee90c65b85ae87b9aa5483ef8ab3d14a939e9a83c459959caeadce47e991fbaee82af0fea7c3b92a81a9ae8bd64b86beadaaf95c9cedac94cf5cedebfeb7c121bcaefbd8b16dafaf8fbaf67e8ee785b6b854f7baff8fd1728287a4d1d246a6f59adac560afb397bbfc25ad9684a2c76b9a8d00b2bb60b295aaafd24a8e91bcd1cb4882e8beb3c964fb9cbd97d04598e9e5a4c6499394ae97ef5d83bd86a3c96f9cbeffb1bb739aed9ea9c437e2a3; WM_TID=AAkRFnl03RdABEBEQFOBWHCPOeMra4IL; playerid=94262567",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        }
