from typing import List
from ..node import Node
from ..system import System

class Environment:
    def __init__(self):
        self.nodes : List[Node] = []
        self.system : System = System()
