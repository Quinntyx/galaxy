from . import registry
from . import fs
from . import utils
import sys


class Galaxy :
    def __init__ (self, silent=False, modules=None, api="core") :
        nodes = [fs.load(i) for i in fs.files() if utils.FileHelper(i).ext == 'json']
        self.nodes = {i['title'] : registry.NODE_REGISTRY.get(i['type'])(i['title'], i['source']) for i in nodes}
        self.modules = {}
        self.silent = silent
        sys.path.append(api)

        if modules :
            sys.path.append(modules)
            for i in fs.files(modules) :
                i = utils.FileHelper(i)
                if i.ext != 'py' : continue
                self.modules[i.filename] = __import__(i.filename)
                self.post(f"Loaded module {i.filename} from {modules}/{i.file}")

    def post (self, *args, **kwargs) :
        if self.silent : return
        print(*args, **kwargs)

    def load_node (self, loc : str) -> 'Brain' :
        new_node = fs.load(f"{loc}.json")
        self.nodes[new_node['title']] = registry.NODE_REGISTRY.get(new_node['type'])(
            new_node['title'],
            new_node['source']
        )
        return self.get(new_node['title'])

    def get (self, node : str) :
        return self.nodes[node]

    def process_new_match (self, srcnode) :
        """
        Iterates through nodes and creates a link to srcnode in each node that matches.
        """
        for i in self.nodes.values() :
            match = i.match(srcnode.name)
            if match.valid :
                i.link(srcnode.name, match.strength)
                self.post(f"Making new link from {i.name} to {srcnode.name}")

            match2 = srcnode.match(i.name)
            if match2.valid :
                srcnode.link(i.name, match2.strength)

    def flush (self) :
        for i in self.nodes.values() :
            i.flush()


