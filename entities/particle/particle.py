from .models.position import Position

class Particle:
    def __init__(self):
        self.position = Position(0.0, 0.0, 0.0)
        self.extensions = {}

    def register_extension(self, name: str, extension_class) -> None:
        self.extensions[name] = extension_class()