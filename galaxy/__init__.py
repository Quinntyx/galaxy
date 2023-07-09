from . import fs, utils, api, registry, builtin_nodes, galaxy
from typing import Self

db = galaxy.Galaxy(modules='modules', api='galaxy')

def ingest (path, *args, **kwargs) -> api.NodeInterface :
    path = utils.FileHelper(path)

    try :
        loc = registry.INGEST_MANAGER_REGISTRY.get(path.ext).ingest(str(path), *args, **kwargs)
    except KeyError :
        print("WARN: Ingest manager not found, ingesting as text")
        loc = registry.INGEST_MANAGER_REGISTRY.get("txt").ingest(str(path), *args, **kwargs)

    node = db.load_node(loc)
    db.process_new_match(node)
