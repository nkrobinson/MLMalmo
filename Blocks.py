class Blocks(object):

    def __init__(self):
        self.wall = '"stone"'
        self.floor = '"stone"'
        self.path = '"stone"'
        self.subgoal = '"beacon"'
        self.goal = '"redstone_block"'
        self.start = '"emerald_block"'

    def getWall(self):
        return self.wall

    def setWall(self, block):
        self.wall = block

    def getFloor(self):
        return self.floor

    def setFloor(self, block):
        self.floor = block

    def getPath(self):
        return self.path

    def setPath(self, block):
        self.path = block

    def getSubGoal(self):
        return self.subgoal

    def setSubGoal(self, block):
        self.subgoal = block

    def getGoal(self):
        return self.goal

    def setGoal(self, block):
        self.goal = block

    def getStart(self):
        return self.start

    def setStart(self, block):
        self.start = block

    def blockId(self, block):
        if block == "air":
            return 0.0
        elif block == "stone":
            return 1.0
        elif block == "grass":
            return 2.0
        elif block == "dirt":
            return 3.0
        elif block == "glowstone":
            return 89.0
        elif block == "emerald_block":
            return 133.0
        elif block == "beacon":
            return 138.0
        elif block == "redstone_block":
            return 152.0
        elif block == "stained_hardened_clay":
            return 159.0
        elif block == "sea_lantern":
            return 169.0
        else:
            return -1.0
