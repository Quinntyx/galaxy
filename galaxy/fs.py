import json
import shutil
import os


def files (target='data') -> list[str] :
    return os.listdir(target)

def copy (f, t=None) -> None :
    if t is not None :
        shutil.copy2(str(f), f"data/{t}")
    else :
        shutil.copy2(str(f), 'data')

def read (path) -> str :
    with open(f"data/{path}", 'r') as f :
        return f.read()

def load (path) -> dict :
    with open(f"data/{path}", 'r') as f :
        return json.load(f)

def dump (data, path) -> None :
    with open(f"data/{path}", 'w') as f :
        json.dump(data, f, indent=4)
