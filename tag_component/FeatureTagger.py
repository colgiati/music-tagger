import re
from typing import List, Tuple, Optional

from mutagen.easyid3 import EasyID3

from song import Song
from tag_component.TagComponent import TagComponent


class FeatureTagger(TagComponent):
    _artists_regex: str = r'[(\[]{0} ([^()\[\]]*)[)\]]'
    _parentheses_regex: str = r'[(\[]{0} [^()]*[)\]]'
    _regex: List[str] = [r'ft\.', r'feat', r'feat\.', r'featuring', r'with']
    _exceptions: List[str] = []

    def __init__(self, exceptions: Optional[List[str]] = None):
        if exceptions:
            self._exceptions = exceptions

    def _tag(self, song: Song):
        title = song.get_title()
        artists = song.get_artists()
        if matches := self._find_featuring(title):
            for parentheses, featuring in matches:
                artists = self._get_artists(artists, featuring)
                title = self._sanitize_title(title, parentheses)
            self._update_song(song, artists, title)

    @classmethod
    def _sanitize_title(cls, title: str, parentheses: str) -> str:
        title = title.replace(parentheses, '')
        return ' '.join(title.split()).strip()

    def _get_artists(self, artists: List[str], featuring: str) -> List[str]:
        for feature in self._split_artists(featuring):
            if feature not in artists:
                artists.append(feature)
        return artists

    @classmethod
    def _update_song(cls, file: Song, artists: List[str], title: str):
        file.set_title(title)
        file.set_artists(artists)

    def _split_artists(self, featuring: str) -> List[str]:
        artists: List[str] = [a.strip() for a in re.split(r'[&,]', featuring)]
        for exception in self._exceptions:
            if exception in featuring:
                for artist in artists.copy():
                    if artist in exception:
                        artists.remove(artist)
                artists.append(exception)
        return artists

    def _find_featuring(self, title: str) -> List[Tuple[str, str]]:
        matches: List[Tuple[str, str]] = []
        for keyword in self._regex:
            parentheses: List[str] = re.findall(self._parentheses_regex.format(keyword), title, re.IGNORECASE)
            featuring: List[str] = re.findall(self._artists_regex.format(keyword), title, re.IGNORECASE)
            for match in zip(parentheses, featuring):
                matches.append(match)
        return matches
