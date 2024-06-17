from song import Song
from tag_component.TagComponent import TagComponent


class TrackNumberFixer(TagComponent):
    def _tag(self, song: Song):
        song.fix_track_number_tags()
        song.pad_track_numbers()
        song.pad_disc_numbers()
