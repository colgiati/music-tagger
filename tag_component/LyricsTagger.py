import re
from typing import Optional, List

from lyric_source.LyricSource import LyricSource
from song import Song
from tag_component.TagComponent import TagComponent


class LyricsTagger(TagComponent):
    _sources: List[LyricSource]
    _parentheses_regex = re.compile('\\([^)]*[^)]*\\)')

    def __init__(self, sources: List[LyricSource]):
        self._sources = sources

    def _tag(self, song: Song):
        if not song.has_lyrics() or True:
            lyrics = self._get_song_lyrics(
                title=self._sanitize_song_name(song.get_title()),
                artist=song.get_artists()[0],
                album=song.get_album(),
                duration=int(song.get_length()),
            )
            if lyrics:
                song.set_lyrics(lyrics)
            else:
                print(self._depth * '\t', f'Lyrics for {song.get_title()} by {song.get_artists()[0]} not found.')

    def _get_song_lyrics(self, title: str, artist: str, album: str, duration: int) -> Optional[str]:
        for source in self._sources:
            if lyrics := source.get_lyrics(title, artist, album, duration):
                return lyrics

    def _sanitize_song_name(self, song_name: str) -> str:
        return re.sub(self._parentheses_regex, '', song_name).strip()
