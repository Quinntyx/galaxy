from .utils import Interface, default
import fs

class FsCopyIngestAction (IngestActionInterface) :
    def __init__ (self, 
    
class NodeInterface (metaclass=Interface) :
    @property
    def content (self) :
        pass

    @property
    def match_data (self) : 
        pass

    @property
    def parsed_data (self) : 
        pass

    @property
    def links (self) : 
        pass

    def match (self, target : str) -> 'Match' : 
        pass

    @default
    def link (self, target : str, strength = 1) :
        self.parsed_data['links'].append(
            {
                "target" : target,
                "strength" : strength
            }
        )

    def flush (self) :
        pass


class IngestManagerInterface (metaclass=Interface) :
    def ingest (self, galaxy_dir) -> str : pass


class Match :
    def __init__ (self, strength) :
        self.strength = strength

    @property
    def valid (self) -> bool : 
        return bool(self.strength)
    
