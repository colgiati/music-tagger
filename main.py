from lyric_source import LrcLibSource, SpotifySource
from tag_component import LyricsTagger
from tagger import Tagger

path = ''
taggers = [
    LyricsTagger(
        sources=[LrcLibSource(), SpotifySource()]
    )
]

if __name__ == '__main__':
    tagger = Tagger(path=path, taggers=taggers, log=True)
    tagger.run()
