import drone_control as dc
import drone_control.commands as commands


controller = dc.get_drone_controller(debug=True)
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
}
while True:
    c = input("Command: ")
    c = c.lower()
    controller.send_command(translate_commands[c]())
    if c == "stop":
        break
print("Flight over")