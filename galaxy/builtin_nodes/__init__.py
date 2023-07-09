from .txt import *
from galaxy import registry

registry.NODE_REGISTRY.register(registry.Identifier.of("txt"), Node)
registry.INGEST_MANAGER_REGISTRY.register(registry.Identifier.of("txt"), TextIngestManager())

