import pygame
from . import globals

__version__ = "0.2.5"

class Controllers:
    def __init__(self, joy):
        globals.init()
        self.controllers = []
        cont = self.detect_controller(joy.get_guid())
        self.controllers.append(cont(joy))

    def detect_controller(self, guid):
        for gp in globals.GAMEPADS:
            for p in globals.GAMEPADS[gp]:
                if p["guid"] != guid:
                    continue
                return p["class"]
        return globals.CONTROLLERS["Generic Controller"]