from typing import Set

from song import Song
from tag_component.TagComponent import TagComponent


class BracketRemover(TagComponent):
    _to_remove: Set[str] = set()

    def __init__(self, to_remove: Set[str]):
        self._to_remove = to_remove

    def _tag(self, song: Song):
        title = song.get_title()
        old_title = title
        title = self._remove_brackets(title)
        if old_title != title:
            song.set_title(title)

    def _remove_brackets(self, title: str) -> str:
        title.replace(' )', ')').replace('( ', '(')
        for x in self._to_remove:
            if x in title:
                title = title.replace(x, '')
                title = ' '.join(title.split(' ')).strip()
        return title
