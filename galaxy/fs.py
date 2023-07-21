import json
import shutil
import os

""" 
Lists files relative to the galaxy root directory passed.
"""
def files (galaxy_root, target='data') -> list[str] :
    return os.listdir(f"{galaxy_root}/{target}")

""" 
Copies files from an absolute path `f` (relative to the 
python interpreter) to the file location `t`, inside the
data directory of the galaxy root passed. 

If `t` is None, the original filename is preserved and it
is copied to {galaxy_root}/data/filename.ext. 
"""
def copy (galaxy_root, f, t=None) -> None :
    if t is not None :
        shutil.copy2(str(f), f"{galaxy_root}/data/{t}")
    else :
        shutil.copy2(str(f), f'{galaxy_root}/data')

"""
Reads a file relative to the galaxy root directory.
returns a string containing the contents of the file. 
ex. 

>>> fs.read("galaxy", "file.txt")

This reads from galaxy/data/file.txt and returns 
the contents of the file. 
"""
def read (galaxy_root, path) -> str :
    with open(f"{galaxy_root}/data/{path}", 'r') as f :
        return f.read()

"""
Loads a json file relative to the galaxy root directory. 
returns a dict containing the contents of the file. 
ex. 

>>> fs.load("galaxy", "file.json")

This loads from galaxy/data/file.json and returns the
contents of the file.
"""
def load (galaxy_root, path) -> dict :
    with open(f"{galaxy_root}/data/{path}", 'r') as f :
        return json.load(f)


"""
Dumps a dict to a json file located relative to the 
galaxy root directory. 
ex. 

>>> fs.dump("galaxy", {'a': 'b'}, "file.json")

This serializes the dictionary `{'a': 'b'}` to JSON and
writes it to the file galaxy/data/file.json. 
"""
def dump (galaxy_root, data, path) -> None :
    with open(f"{galaxy_root}/data/{path}", 'w') as f :
        json.dump(data, f, indent=4)
