from drone_control.drone_controller import DroneController

def get_drone_controller(addr="d0:3a:86:4c:e6:5a", debug=False):
    return DroneController(addr, debug)
    # d0:3a:86:9d:e6:5a for blu

