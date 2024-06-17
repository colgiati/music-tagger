from librosa import load, beat

from song import Song
from tag_component.TagComponent import TagComponent


class BPMTagger(TagComponent):

    def _tag(self, song: Song):
        if not song.has_bpm():
            y, sr = load(song.path)
            [tempo], _ = beat.beat_track(y=y, sr=sr)
            song.set_bpm(round(tempo))
