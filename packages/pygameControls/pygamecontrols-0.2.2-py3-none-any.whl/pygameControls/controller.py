import pygame
from . import globals

__version__ = "0.2.2"

class Controllers:
    def __init__(self, joy):
        self.controllers = []
        cont = self.detect_controller(joy.get_guid())
        print(cont)
        self.controllers.append(cont(joy))

    def detect_controller(self, guid):
        for gp in globals.GAMEPADS:
            print(gp)
            for p in globals.GAMEPADS[gp]:
                print(p)
                if p["guid"] != guid:
                    continue
                return p["class"]
        return globals.CONTROLLERS["Generic Controller"]