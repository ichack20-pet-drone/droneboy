

class Command():
    def __init__(self, command):
        self.command_code = command


class Stop(Command):
    def __init__(self):
        super().__init__(0)


class Takeoff(Command):
    def __init__(self):
        super().__init__(1)


class Land(Command):
    def __init__(self):
        super().__init__(2)


class Forward(Command):
    def __init__(self):
        super().__init__(3)


class Backward(Command):
    def __init__(self):
        super().__init__(4)


class Left(Command):
    def __init__(self):
        super().__init__(5)


class Right(Command):
    def __init__(self):
        super().__init__(6)


class Up(Command):
    def __init__(self):
        super().__init__(7)


class Down(Command):
    def __init__(self):
        super().__init__(8)


class TurnLeft(Command):
    def __init__(self):
        super().__init__(9)


class TurnRight(Command):
    def __init__(self):
        super().__init__(10)


class FlipForward(Command):
    def __init__(self):
        super().__init__(11)


class FlipBackward(Command):
    def __init__(self):
        super().__init__(12)


class FlipRight(Command):
    def __init__(self):
        super().__init__(13)


class FlipLeft(Command):
    def __init__(self):
        super().__init__(14)
