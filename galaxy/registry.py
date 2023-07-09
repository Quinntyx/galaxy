from . import utils
from . import api


class Identifier :
    def __init__ (self, namespace, title) :
        self.id = f"{namespace}::{title}"
        self.namespace = namespace
        self.title = title

    @staticmethod
    def of (string : str) -> 'Identifier' :
        if '::' in string :
            return Identifier(string.split('::')[0], string.split('::')[1])
        return Identifier("core", string)

    def __str__ (self) -> str :
        return repr(self)

    def __repr__ (self) -> str :
        return f"Identifier.of({self.id})"

    def __hash__ (self) :
        return hash(self.id)

    def __eq__ (self, other) :
        return self.id == other.id


class Registry :
    def __init__ (self, registry_type : type) :
        self._registry = {}
        self.type = registry_type

    def register (self, identifier : Identifier, target) :
        self.registry_hook(identifier, target)
        self._registry[identifier] = target

    def registry_hook (self, identifier : Identifier, target) :
        if not isinstance(target, self.type) :
            raise utils.TypeCollisionError(f"Attempted to insert {str(target)} of type {type(target)} into registry of {self.type}")

    def get (self, key : (Identifier, str)) :
        if not isinstance(key, Identifier) : key = Identifier.of(key)
        
        print(key)
        print(self._registry)

        return self._registry[key]

class TypeRegistry (Registry) :
    def __init__ (self, registry_superclass : type) :
        super(TypeRegistry, self).__init__(registry_superclass)

    def registry_hook (self, identifier : Identifier, target) :
        if not issubclass(target, self.type) :
            raise utils.TypeCollisionError(f"Attempted to insert type {str(target)} into registry of type {self.type}")


NODE_REGISTRY = TypeRegistry(api.NodeInterface)
INGEST_MANAGER_REGISTRY = Registry(api.IngestManagerInterface)

