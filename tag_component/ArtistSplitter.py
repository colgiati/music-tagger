from typing import Optional, List

from song import Song
from tag_component.TagComponent import TagComponent


class ArtistSplitter(TagComponent):
    _exceptions: List[str] = []

    def __init__(self, exceptions: Optional[List[str]] = None):
        if exceptions:
            self._exceptions = exceptions

    def _tag(self, song: Song):
        artists = song.get_artists()
        new_artists = list()
        make_changes = False
        for artist in artists:
            if artist not in self._exceptions and ',' in artist:
                make_changes = True
                _artists = artist.split(',')
                for _artist in _artists:
                    new_artists.append(_artist.strip())
        for artist in artists:
            if artist in self._exceptions or ',' not in artist:
                if artist not in new_artists:
                    new_artists.append(artist)
        if make_changes:
            song.set_artists(new_artists)
