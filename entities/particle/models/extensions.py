from dataclasses import dataclass

@dataclass
class LinkedList:
    prev : 'LinkedList' = None
    next : 'LinkedList' = None