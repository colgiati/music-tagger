from lyric_source import LrcLibSource, SpotifySource
from tag_component import LyricsTagger
from tag_component.BPMTagger import BPMTagger
from tagger import Tagger

paths = ['path/to/music/folder']
taggers = [
    BPMTagger(),
    LyricsTagger(
        sources=[LrcLibSource(), SpotifySource()]
    )
]

if __name__ == '__main__':
    tagger = Tagger(path=path, taggers=taggers, log=True)
    tagger.run()
