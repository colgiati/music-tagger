import re
from pathlib import Path

from song import Song
from tag_component.TagComponent import TagComponent


class FileRenamer(TagComponent):

    def _tag(self, song: Song):
        path = Path(song.path)
        title = song.get_title()
        artists = song.get_artists()
        sanitized_title = re.sub(r'[^\w\s()\[\]-]', '-', title)
        disc_number = song.get_disc_number()
        track_number = song.get_track_number()

        new_filename = f'{disc_number}-{track_number} {sanitized_title} - {";".join(artists)}{path.suffix}'
        new_filename = re.sub(r'\"', "''", new_filename)
        path.rename(Path(path.parent, new_filename))
