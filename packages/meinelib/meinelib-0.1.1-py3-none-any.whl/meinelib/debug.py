""" Debugging utilities for pickling and unpickling objects. """
import pickle
import sys
from typing import Any
import json

def dump(obj: Any, filename:str ="dump", _exit: bool =False) -> None:
    """ Dump pickled object

        Params
        ------
        obj: Any -  The object to dump
        filename:str (default: dump) - The file to dump to (it will append .pickle)
        _exit: bool (default: False) - Runs sys.exit when finished.
    """
    with open(f"{filename}.pickle", "wb") as f:
        pickle.dump(obj, f)
    if _exit:
        sys.exit()


def load_dump(filename: str = "dump") -> None:
    """ Load pickled data

        Params
        ------
        filename: str (default: dump) - The file to pickle load
    """
    with open(f"{filename}.pickle", "rb") as f:
        obj = pickle.load(f)
    return obj

def json_dump (obj: Any, filename: str ="data", _exit: bool =False) -> None:
    """ Dump object as JSON

        Params
        ------
        obj: Any -  The object to dump
        filename:str (default: data) - The file to dump to (it will append .json)
        _exit: bool (default: False) - Runs sys.exit when finished.

    """
    with open(f"{filename}.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(obj))
    if _exit:
        sys.exit()

def json_load (filename:str="data") -> None:
    """ Load a JSON Object

        Params
        ------
        filename: str (default: data) - The file to JSON load
    """
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

