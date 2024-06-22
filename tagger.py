import os
from typing import List, Optional

from mutagen import MutagenError
from mutagen.id3 import ID3NoHeaderError

from tag_component import TagComponent


class Tagger:
    _root_paths: List[str]
    _taggers: List[TagComponent]
    _log: bool = False

    def __init__(self, path: List[str] | str, taggers: List[TagComponent], log: Optional[bool] = None):
        if isinstance(path, str):
            self._root_paths = [path]
        else:
            self._root_paths = path
        self._taggers = taggers
        if log is not None:
            self._log = log

    def run(self):
        for root_path in self._root_paths:
            if self._log:
                print(root_path)
            self._tag_directory(root_path)

    def _tag_directory(self, path: str, depth: int = 1):
        for file in os.listdir(path):
            complete_path = f'{path}/{file}'
            self._tag_file(complete_path, depth)
            if os.path.isdir(complete_path):
                if self._log:
                    print(depth * '\t', file)
                self._tag_directory(
                    path=complete_path,
                    depth=depth + 1
                )

    def _tag_file(self, path: str, depth: int):
        for tagger in self._taggers:
            try:
                tagger.tag(path, depth)

            except ID3NoHeaderError as _:
                print(f'No headers found for: {path}')
            except MutagenError as e:
                print(e)
            except Exception as e:
                print(f'Error with file {path}')
                raise e
