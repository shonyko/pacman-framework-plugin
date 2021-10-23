from random import randrange
import random
from Game import Agent
from graphicsUtils import *
from pacman import GhostRules

class GhostPacmanAgent(Agent):
    "A pacman ghost filled with the rage of defeat."
    def getAction( self, state ):
        actions = state.getLegalPacmanActions(self.index)
        
        rnd = randrange(len(actions))

        return actions[rnd]

    def copy( self, index = 0 ):
        return GhostPacmanAgent(index)

GHOST_PACMAN_COLORS = [
    #outline
    formatColor(1.0, 0.75, 0.79),
    #fill
    formatColor(1.0, 0.75, 0.79)
]

DEAD_PACMAN_COLORS = [
    #outline
    formatColor(0.0, 0.0, 0.0),
    #fill
    formatColor(0.0, 0.0, 0.0)
]

def isTrue(value):
    if type(value) == bool:
        return value == True
    if type(value) == str:
        return str(value) == "True"
    if type(value) == int:
        return str(value) > 0

# Singleton
def GhostPacmanConfig( args = None ):
    if _GhostPacmanConfig._instance is None:
        _GhostPacmanConfig._instance = _GhostPacmanConfig(**args)

    return _GhostPacmanConfig._instance
    


class _GhostPacmanConfig():
    _instance = None

    def __init__( self, enabled = True,  numFoods = 3, startingFoods = 0, probability = 1.0 / 3.0, maxSteps = 15, killGhosts = False, ghostPacmanAgent = GhostPacmanAgent, ghostPacmanColors = GHOST_PACMAN_COLORS, deadPacmanColors = DEAD_PACMAN_COLORS ):
        self.enabled = isTrue(enabled)
        self.numFoods = int(numFoods)
        self.startingFoods = int(startingFoods)
        self.probability = float(probability)
        self.maxSteps = int(maxSteps)
        self.killGhosts = isTrue(killGhosts)
        self.ghostPacmanAgent = ghostPacmanAgent
        self.ghostPacmanColors = ghostPacmanColors
        self.deadPacmanColors = deadPacmanColors

        self._isInitialized = False

    def initialize( self, game ):
        self._eatenFoods = self.startingFoods
        self._ghostPacmanAgents = {}
        self._ghostPacmanId = 0

        self._game = game

        self._isInitialized = True

    def move( self, agentIndex ):
        if not self.enabled: return 0
        if not self._isInitialized:
            print("Not initialized!")
            return 0

        # Daca e pacman verificam daca putem invoca si alte fantome sa ne ajute !
        if agentIndex == 0:
            return self.eat(agentIndex)

        numGhostAgents = self._game.state.getNumGhostAgents()
        # Nu ne intereseaza fantomele
        if agentIndex <= numGhostAgents:
            return 0
        
        # Daca e o fantoma pacman ii actualizam timpul de stat in viata
        #   si verificam daca poate manca alte fantome
        despawned = False

        agentState = self._game.state.data.agentStates[agentIndex]

        if self.killGhosts:
            for index in range(1, numGhostAgents + 1):
                ghostState = self._game.state.getGhostState(index)
                if GhostRules.canKill(agentState.getPosition(), ghostState.getPosition()):
                    self._game.state.data.scoreChange += 50
                    GhostRules.placeGhost(self._game.state, ghostState)

        self._ghostPacmanAgents[agentState._ghostPacmanId] = self._ghostPacmanAgents[agentState._ghostPacmanId] - 1 

        if self._ghostPacmanAgents[agentState._ghostPacmanId] <= 0:
            self.despawnGhostPacman(agentIndex)
            despawned = True

        return -1 if despawned else 0
    
    def eat( self, agentIndex ):
        spawned = False

        self._eatenFoods += self._game.state.data._foodEaten is not None
        if self._eatenFoods >= self.numFoods:
            rnd = random.random()
            if rnd < self.probability:
                self.spawnGhostPacman()
                spawned = True

            self._eatenFoods -= self.numFoods

        return spawned

    def spawnGhostPacman( self ):
        agentState = self._game.state.data.agentStates[0].copy()
        agent = self.ghostPacmanAgent( len(self._game.agents) )

        agentState._ghostPacmanId = self._ghostPacmanId
        self._ghostPacmanAgents[self._ghostPacmanId] = self.maxSteps

        self._game.display.addGhostPacmanObject(agentState, self.ghostPacmanColors)
        self._game.agents.append(agent)
        self._game.state.data.agentStates.append(agentState)

        self._ghostPacmanId += 1

    def despawnGhostPacman( self, agentIndex ):
        agentState = self._game.state.data.agentStates[agentIndex]

        for index in range(agentIndex + 1, self._game.state.getNumAgents()):
            self._game.agents[index].index = index - 1

        self._game.display.undrawGhostPacman(agentIndex, self.deadPacmanColors)
        self._game.display.removeGhostPacmanObject(agentIndex)
        self._game.agents.pop(agentIndex)
        self._game.state.data.agentStates.pop(agentIndex)

        del self._ghostPacmanAgents[agentState._ghostPacmanId]




