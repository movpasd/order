from inputs.keyboard import controller, ControllerButton


@controller
class Paddle:

    north = ControllerButton("north")

    def __init__(self):

        self.north = False
        self.south  = False
        self.west = False
        self.east = False

    @north.on_keypress("north")
    def keypress_north(self):
        self.north = True

    @north.on_keyrelease("north")
    def keyrelease_north(self):
        self.north = False