import drone_control as dc
import drone_control.commands as commands


controller = dc.get_drone_controller(debug=True, mock=True)
input("Are you ready kids?? ") # aye aye
controller.start_flight()
translate_commands = {
    "": commands.Land,
    "stop": commands.Stop,
    "takeoff": commands.Takeoff,
    "land": commands.Land,
    "forward": commands.Forward,
    "backward": commands.Backward,
    "left": commands.Left,
    "right": commands.Right,
    "up": commands.Up,
    "down": commands.Down,
    "turnl": commands.TurnLeft,
    "turnr": commands.TurnRight,
    "flip": commands.FlipForward,
    "flipf": commands.FlipForward,
    "flipb": commands.FlipBackward,
    "flips": commands.FlipRight,
    
}
while True:
    c = input("Command: ")
    c = c.lower()
    try:
        controller.send_command(translate_commands[c]())
    except:
        print("Invalid command")
    if c == "stop":
        break
print("Flight over")
