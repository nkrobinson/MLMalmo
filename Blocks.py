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
