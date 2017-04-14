import MalmoPython
import re
import json
import time

class Observations(object):

    def __init__(self, malmo_run):
        self.mr = malmo_run
        self.agent_host = self.mr.agent_host

    def update(self):
        world_state = self.mr.checkWorldState()
        while len(world_state.observations) == 0:
            if not world_state.is_mission_running:
                return False
            world_state = self.mr.checkWorldState()
        # print "Observations: World state observations: " + str(world_state.observations[0].text)
        # print "Length: " + str(len(world_state.observations))

        self.observations = json.loads(world_state.observations[0].text)
        self.direction = self.observations['Yaw']
        self.grid = self.observations['AgentGrid']
        self.gridFloat = map(self.mr.b.blockId, self.grid)
        return True

    def frontBlocked(self):
        if (self.direction <= 45 or self.direction > 315):
            return self.grid[16] != 'air'
        elif (self.direction <= 135 and self.direction > 45):
            return self.grid[12] != 'air'
        elif (self.direction <= 225 and self.direction > 135):
            return self.grid[10] != 'air'
        else:
            return self.grid[14] != 'air'

    def backBlocked(self):
        if (self.direction <= 45 or self.direction > 315):
            return self.grid[10] != 'air'
        elif (self.direction <= 135 and self.direction > 45):
            return self.grid[14] != 'air'
        elif (self.direction <= 225 and self.direction > 135):
            return self.grid[16] != 'air'
        else:
            return self.grid[12] != 'air'

    def leftBlocked(self):
        if (self.direction <= 45 or self.direction > 315):
            return self.grid[14] != 'air'
        elif (self.direction <= 135 and self.direction > 45):
            return self.grid[16] != 'air'
        elif (self.direction <= 225 and self.direction > 135):
            return self.grid[12] != 'air'
        else:
            return self.grid[10] != 'air'

    def rightBlocked(self):
        if (self.direction <= 45 or self.direction > 315):
            return self.grid[12] != 'air'
        elif (self.direction <= 135 and self.direction > 45):
            return self.grid[10] != 'air'
        elif (self.direction <= 225 and self.direction > 135):
            return self.grid[14] != 'air'
        else:
            return self.grid[16] != 'air'

    def frontBlock(self):
        if (self.direction <= 45 or self.direction > 315):
            return self.grid[16]
        elif (self.direction <= 135 and self.direction > 45):
            return self.grid[12]
        elif (self.direction <= 225 and self.direction > 135):
            return self.grid[10]
        else:
            return self.grid[14]

    def backBlock(self):
        if (self.direction <= 45 or self.direction > 315):
            return self.grid[10]
        elif (self.direction <= 135 and self.direction > 45):
            return self.grid[14]
        elif (self.direction <= 225 and self.direction > 135):
            return self.grid[16]
        else:
            return self.grid[12]

    def leftBlock(self):
        if (self.direction <= 45 or self.direction > 315):
            return self.grid[14]
        elif (self.direction <= 135 and self.direction > 45):
            return self.grid[16]
        elif (self.direction <= 225 and self.direction > 135):
            return self.grid[12]
        else:
            return self.grid[10]

    def rightBlock(self):
        if (self.direction <= 45 or self.direction > 315):
            return self.grid[12]
        elif (self.direction <= 135 and self.direction > 45):
            return self.grid[10]
        elif (self.direction <= 225 and self.direction > 135):
            return self.grid[14]
        else:
            return self.grid[16]

    def getDirection(self):
        return self.direction
