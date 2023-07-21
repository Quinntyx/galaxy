from galaxy.api import NodeInterface, IngestManagerInterface, Match
from galaxy import fs
from galaxy import utils

class Node (NodeInterface) :
    def __init__ (self, name, source) :
        self.name = name
        self.source = source
        self.filename = f"{source}:{name}"
        self.type = "txt"
        self._parsed_data = None
        self._content = None
        self._match_data = None

    @property
    def content (self) :
        if self._content is None :
            self._content = fs.read(self.parsed_data['data']['file'])
        return self._content

    @property
    def match_data (self) :
        if self._match_data is None :
            self._match_data = fs.read(f"{self.filename}.match").lower()
        return self._match_data


    @property
    def parsed_data (self) :
        if self._parsed_data is None :
            self._parsed_data = fs.load(f"{self.filename}.json")
        return self._parsed_data

    @property
    def links (self) :
        return self.parsed_data['links']

    @property
    def data (self) :
        return self.parsed_data['data']

    def invalidate_cache (self, include_content=False, include_match=False) :
        self._parsed_data = None
        if include_match : 
            self._match_data = None
        if include_content:
            self._content = None

    def match (self, target : str) -> Match :
        return Match(self.match_data.count(target))

    def flush (self) :
        fs.dump(self.parsed_data, f"{self.filename}.json")


class TextIngestManager (IngestManagerInterface) :
    def ingest (self, galaxy_root: str, path: str, source: str) -> str : 
        file = utils.FileHelper(path).prepend(source)

        fs.copy(galaxy_root, path, file.chext('match').file)
        fs.dump(
            galaxy_root,
            utils.construct_node_json(
                file.filename_sect[1],
                'txt',
                source,
                [],
                {
                    "file" : str(file.file)
                }
            ),
            str(file.chext('json').file)
        )
        fs.copy(galaxy_root, path, file.file)
        
        return str(file.filename)

        
