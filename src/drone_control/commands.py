

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
