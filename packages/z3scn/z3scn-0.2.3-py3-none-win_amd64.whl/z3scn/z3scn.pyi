from typing import Optional, Union

# z3scn.pyi - Type stubs for z3slipro extension lite version

# initialization
def init(com: int, id: Union[int, List[int]] = 0, stroke: int = 100, accel: int = 200, gain: int = 7, normalSpd: int = 7800, homeSpd: int = 2000, moveMode: int = 0, gohome: int = 0, gocenter: int = 0, diag: int = 0) -> bool:
    """
    Initialize the SCN device.

    Parameters:
        com (int): Required. COM port number (e.g., 3 for COM4)
        id (int or list[int]): Optional. Device ID Range [0–15]
        stroke (int): Optional. Stroke length (e.g., 100)
        accel (int): Optional. Acceleration value
        gain (int): Optional. Control gain
        normalSpd (int): Optional. Normal movement speed
        homeSpd (int): Optional. Speed for homing
        moveMode (int): Optional. Movement mode
        gohome (int): Optional. If non-zero, go home on init
        gocenter (int): Optional. If non-zero, go center after home
        diag (int): Optional. Dump actuator BANK settings
    Returns:
        bool: True if initialization succeeded, False otherwise
    """
    ...
def terminate() -> None: ...    

# device information
def get_device_info(selector: str, id: int = 0) -> dict: ...    

# device motion control
def go_home(id: int = 0) -> bool: ...

def go_home(id: int = 0) -> None: ...

def go_center(id: int = 0) -> bool: ...

def go_position(pos: float, id: int = 0) -> bool: ...

def load_position(pos: float, id: int = 0) -> bool: ...

def clear_position(id: int = 0) -> None: ...

def check_scn(id: int = 0) -> bool: ...

def submit_check(id: int = 0) -> None: ...    

def submit(id: int = 0) -> None: ...

# device speed & accel control
def set_default_speed(id: int = 0) -> bool: ...

def set_speed(speed: int, id: int = 0) -> bool: ...

def set_speed_accel(speed: int, accel: int, id: int = 0) -> bool: ...

def set_accel(accel: int, id: int = 0) -> bool: ...
