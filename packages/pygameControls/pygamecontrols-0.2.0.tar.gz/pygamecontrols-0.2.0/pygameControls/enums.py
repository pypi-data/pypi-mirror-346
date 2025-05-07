from enum import Enum

class ConnectionType(Enum):
    USB = 1
    BLUETOOTH = 2
    WIRELESS = 3
    Unknown = -1

class InputType(Enum):
    DirectInput = 1
    XInput = 2
    Unknown = -1