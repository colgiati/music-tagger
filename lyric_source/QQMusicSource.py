import json
from json import JSONDecodeError
from typing import Optional, Dict, Any, List

from requests import get, post

from lyric_source import LyricSource


class QQMusicSource(LyricSource):
    _base_url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp"
    _lyrics_url = "https://paxmusic.serv00.net/getQQLyrics.php"

    def get_lyrics(self, title: str, artist: str, album: str, duration: int) -> Optional[str]:
        payload = self._get_payload(title, artist)
        return self._get_lyrics(payload)

    def _get_lyrics(self, payload: Dict[str, Any]) -> Optional[str]:
        response = post(self._lyrics_url, data=json.dumps(payload))
        try:
            return self._to_lrc(response.json())
        except JSONDecodeError:
            return None

    def _get_payload(self, title: str, artist: str) -> Dict[str, Any]:
        query = f'{title} {artist}'
        response = get(self._base_url, params=self._get_params(query), headers=self._get_headers())
        song_details = response.json()
        song = song_details['data']['song']['list'][0]
        return {
            'artist': [singer['name'] for singer in song['singer']],
            'album': song['album']['name'],
            'id': song['id'],
            'title': song['title']
        }

    @classmethod
    def _to_lrc(cls, lyrics: List[Dict]) -> str:
        lines = []
        for lyric in lyrics:
            time = cls._transform_time(lyric['timestamp'])
            text = ''.join([word['text'] for word in lyric['text']])
            lines.append(f'{time} {text}')
        return '\n'.join(lines)

    @classmethod
    def _get_headers(cls) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        }

    @classmethod
    def _get_params(cls, query: str) -> Dict[str, str]:
        return {
            "format": "json",
            "inCharset": "utf8",
            "outCharset": "utf8",
            "platform": "yqq.json",
            "new_json": 1,
            "w": query,
        }
