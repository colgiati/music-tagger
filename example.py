from lyric_source import LrcLibSource, QQMusicSource, MusixmatchSource
from tag_component import LyricsTagger
from tag_component.BPMTagger import BPMTagger
from tagger import Tagger

paths = ['path/to/music/folder']
taggers = [
    BPMTagger(),
    LyricsTagger(
        sources=[
            LrcLibSource(),
            MusixmatchSource(),
            QQMusicSource(),
        ]
    )
]

if __name__ == '__main__':
    tagger = Tagger(path=paths, taggers=taggers, log=True)
    tagger.run()
