class RelativePosition:
    def __init__(self, radius: float, angle: float, bot_to_follow):
        self.bot_to_follow = bot_to_follow
        self.angle = angle
        self.radius = radius
