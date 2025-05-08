from .enums import ConnectionType, InputType

from .controlsbase import ControlsBase
from .dualsense_controller import DualSenseController
from .dualsense_edge_controller import DualSenseEdgeController
from .logitech_f310_controller import LogitechF310Controller
from .logitech_f510_controller import LogitechF510Controller
from .logitech_f710_controller import LogitechF710Controller
from .xbox_series_x_controller import XboxSeriesXController
from .sony_playstation3_controller import SonyPlayStation3Controller
from .playstation3_controller import PlayStation3Controller
from .sony_playstation4_controller import SonyPlayStation4Controller
from .playstation4_controller import PlayStation4Controller
from .generic_controller import GenericController
from .logitech_dual_action_controller import LogitechDualActionController

def init():
    global VID_PID
    VID_PID = {
        "046d:c216": "Logitech Gamepad F310",
        "046d:c21d": "Microsoft X-Box 360 pad",
        "046d:c21d": "Logitech Dual Action",
        "045e:0b12": "Xbox Series X Controller",
        "045e:0b13": "Xbox Series X Controller",
        "045e:0b20": "Xbox Series X Controller",
        "045e:0b21": "Xbox Series X Controller",
        "054c:0ce6": "DualSense Wireless Controller",
        "054c:0df2": "DualSense Wireless Controller",
    }
    global CONTROLLERS
    CONTROLLERS = {
        "DualSense Wireless Controller": DualSenseController,
        "DualSense Edge Wireless Controller": DualSenseEdgeController,
        "Logitech Gamepad F310": LogitechF310Controller,
        "Logitech Gamepad F510": LogitechF510Controller,
        "Logitech Gamepad F710": LogitechF710Controller,
        "Logitech Dual Action": LogitechDualActionController,
        "Microsoft X-Box 360 pad": LogitechDualActionController,
        "Xbox Series X Controller": XboxSeriesXController,
        "Sony PLAYSTATION(R)3 Controller": SonyPlayStation3Controller,
        "PLAYSTATION(R)3 Controller": PlayStation3Controller,
        "Sony PLAYSTATION(R)4 Controller": SonyPlayStation4Controller,
        "PLAYSTATION(R)4 Controller": PlayStation4Controller,
        "Generic Controller": GenericController
        }
    global GAMEPADS
    GAMEPADS = {
        "Sony Controller": [
            {
                "vidpid": "054c:0ce6",
                "guid": "0300fd574c050000e60c000011810000",
                "connection": ConnectionType.USB,
                "input": InputType.DirectInput,
                "name": [
                    "Sony Interactive Entertainment DualSense Wireless Controller",
                    "Sony Corp. DualSense wireless controller (PS5)",
                    "DualSense Wireless Controller"
                    ],
                "class": CONTROLLERS["DualSense Wireless Controller"]
            },
            {
                "vidpid": "054c:0df2",
                "guid": "050057564c050000e60c000000810000",
                "connection": ConnectionType.BLUETOOTH,
                "input": InputType.DirectInput,
                "name": [
                    "DualSense Wireless Controller"
                    ],
                "class": CONTROLLERS["DualSense Wireless Controller"]
            },
            {
                "vidpid": "054c:0dfc",
                "guid": "",
                "connection": ConnectionType.USB,
                "input": InputType.DirectInput,
                "name": ["DualSense Edge Wireless Controller"],
                "class": CONTROLLERS["DualSense Edge Wireless Controller"]
            },
            {
                "vidpid": "054c:0dfc",
                "guid": "",
                "connection": ConnectionType.BLUETOOTH,
                "input": InputType.DirectInput,
                "name": ["DualSense Edge Wireless Controller"],
                "class": CONTROLLERS["DualSense Edge Wireless Controller"]
            },
            {
                "vidpid": "054c:0268",
                "guid": "0300afd34c0500006802000011810000",
                "connection": ConnectionType.USB,
                "input": InputType.DirectInput,
                "name": ["Sony PLAYSTATION(R)3 Controller"],
                "class": CONTROLLERS["Sony PLAYSTATION(R)3 Controller"]
            },
            {
                "vidpid": "",
                "guid": "0500f9d24c0500006802000000800000",
                "connection": ConnectionType.BLUETOOTH,
                "input": InputType.DirectInput,
                "name": ["PLAYSTATION(R)3 Controller"],
                "class": CONTROLLERS["PLAYSTATION(R)3 Controller"]
            },
            {
                "vidpid": "054c:05c4",
                "guid": "",
                "connection": ConnectionType.USB,
                "input": InputType.DirectInput,
                "name": ["DualShock 4 v1 Controller"],
                "class": CONTROLLERS["PLAYSTATION(R)4 Controller"]
            },
            {
                "vidpid": "054c:05c4",
                "guid": "",
                "connection": ConnectionType.BLUETOOTH,
                "input": InputType.DirectInput,
                "name": ["DualShock 4 v1 Controller"],
                "class": CONTROLLERS["Sony PLAYSTATION(R)4 Controller"]
            },
            {
                "vidpid": "054c:09cc",
                "guid": "",
                "connection": ConnectionType.USB,
                "input": InputType.DirectInput,
                "name": ["DualShock 4 v2 Controller"],
                "class": CONTROLLERS["PLAYSTATION(R)4 Controller"]
            },
            {
                "vidpid": "054c:09cc",
                "guid": "",
                "connection": ConnectionType.BLUETOOTH,
                "input": InputType.DirectInput,
                "name": ["DualShock 4 v2 Controller"],
                "class": CONTROLLERS["Sony PLAYSTATION(R)4 Controller"]
            }
        ],
        "Microsoft Controller": [
            {
                "vidpid": "045e:0b12",
                "guid": "0300509d5e040000120b000017050000",
                "connection": ConnectionType.USB,
                "input": InputType.XInput,
                "name": [
                    "Xbox Series X Controller",
                    "Microsoft Corp. Xbox Controller"
                ],
                "class": CONTROLLERS["Xbox Series X Controller"]
            },
            {
                "vidpid": "045e:0b13",
                "guid": "0500509d5e040000130b000023050000",
                "connection": ConnectionType.BLUETOOTH,
                "input": InputType.XInput,
                "name": [
                    "Xbox Series X Controller",
                    "Xbox Wireless Controller"
                ],
                "class": CONTROLLERS["Xbox Series X Controller"]
            }
        ],
        "Logitech Controller": [
            {
                "vidpid": "046d:c21d",
                "guid": "030005ff6d0400001dc2000014400000",
                "connection": ConnectionType.USB,
                "input": InputType.XInput,
                "name": [
                    "Logitech, Inc. F310 Gamepad [XInput Mode]",
                    "Logitech Gamepad F310"
                ],
                "class": CONTROLLERS["Logitech Gamepad F310"]
            },
            {
                "vidpid": "046d:c216",
                "guid": "0300040e6d04000016c2000011010000",
                "connection": ConnectionType.USB,
                "input": InputType.DirectInput,
                "name": [
                    "Logitech, Inc. F310 Gamepad [DirectInput Mode]",
                    "Logitech Dual Action",
                    "Logitech Logitech Dual Action"
                ],
                "class": CONTROLLERS["Logitech Dual Action"]
            },
            {
                "vidpid": "046d:c21d",
                "guid": "",
                "connection": ConnectionType.USB,
                "input": InputType.XInput,
                "name": [
                    "Logitech, Inc. F710 Gamepad [XInput Mode]",
                    "Logitech Gamepad F710"
                ],
                "class": CONTROLLERS["Logitech Gamepad F710"]
            },
            {
                "vidpid": "046d:c216",
                "guid": "",
                "connection": ConnectionType.USB,
                "input": InputType.DirectInput,
                "name": [
                    "Logitech, Inc. F710 Gamepad [DirectInput Mode]",
                    "Logitech Dual Action"
                ],
                "class": CONTROLLERS["Logitech Dual Action"]
            }
        ]
    }