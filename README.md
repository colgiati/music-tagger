# music-tagger

Little python library to help with tagging music files. Recursively tags files in a given folder.

## Setup

> Tool is being developed using python 3.11. It might work with lower versions, but has not been tested with anything
> else.

- Clone or download the repository
- Create a python virtual environment in the source directory
    - https://python.land/virtual-environments/virtualenv#How_to_create_a_Python_venv
- Install requirements
    - `pip install -r requirements.txt`

## Usage

> The following changes are to be made in the `main.py` file. A basic configuration is given by default.
---
Set the path of the root folder containing the music files you want to be tagged.
```py
path = 'C:/user/music'
```
---
Set the taggers you would like to use.
```py
taggers = [
    LyricsTagger(
        sources=[LrcLib(), Spotify()]
    )
]
```
---
Build the Tagger. Set log=True if you would like the current directory to be printed.
```py
if __name__ == '__main__':
    tagger = Tagger(path=path, taggers=taggers, log=True)
    tagger.run()
```
---
You can now run the program by running `main.py`.
```bash
py main.py
```

## Taggers

Currently only a single tagger exists (for adding synchronised lyrics). 
More taggers exist in my private repository for this project.
I will publish them later on, once I add .mp3 support (currently they only work with .flac files).

### LyricsTagger

Embeds synchronised lyrics into music files. Different sources for lyrics can be used with this tagger. 
Currently, there are two sources: LrcLib and Spotify. 
You can choose which sources you would like to use, by passing them to the LyricsTagger:
```py
lyrics_tagger = LyricsTagger(
    sources=[LrcLib(), Spotify()]
)
```

Or if you only want to use one specific source:
```py
lyrics_tagger = LyricsTagger(
    sources=[LrcLib()]
)
```

The sources are searched in the given order. If no lyrics are found in the first source, the next source is searched.


