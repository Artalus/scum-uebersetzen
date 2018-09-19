from typing import Union, TextIO
import json

class JsConfig:
    def __init__(self, **json_args):
        for a, b in json_args.items():
            if not hasattr(self, a):
                print("warning: json sets '{0}: {1}' that has no default value".format(a,b))
            setattr(self, a, b)
    
    @staticmethod
    def read_js(filename: str):
        with open(filename) as f:
            return json.load(f)