from random import randrange
from random import uniform
from Game import Agent
from graphicsUtils import *

class GhostPacmanAgent(Agent):
    "A pacman ghost filled with the rage of defeat."
    def getAction( self, state ):
        actions = state.getLegalPacmanActions(self.index)
        
        rnd = randrange(len(actions))

        return actions[rnd]

    def copy( self, index = 0 ):
        return RandomAgent(index)

GHOST_PACMAN_COLORS = [
    #outline
    formatColor(1.0, 0.75, 0.79),
    #fill
    formatColor(1.0, 0.75, 0.79)
]

# Singleton
def GhostPacmanConfig( args = None ):
    return _GhostPacmanConfig._instance = _GhostPacmanConfig(**args) if _GhostPacmanConfig._instance is None else _GhostPacmanConfig._instance
    


class _GhostPacmanConfig():
    _instance = None

    def __init__( self, enabled = True,  numFoods = 3, probability = 1 / 3, maxSteps = 15, killGhosts = False, ghostPacmanAgent = GhostPacmanAgent, ghostPacmanColors = GHOST_PACMAN_COLORS ):
        self.enabled = enabled
        self.numFoods = numFoods
        self.probability = probability
        self.maxSteps = maxSteps
        self.killGhosts = killGhosts
        self.ghostPacmanAgent = ghostPacmanAgent
        self.ghostPacmanColors = ghostPacmanColors

        self._isInitialized = False

    def initialize( self, game, startingFoods = 0 ):
        self._eatenFoods = startingFoods
        self._ghostPacmanAgents = {}
        self._ghostPacmanId = 0

        self._game = game

        self._isInitialized = True

    def move( self, agentIndex ):
        if not self.enabled: return 0
        if not self._isInitialized:
            print("Not initialized!")
            return 0

        # Nu ne intereseaza fantomele
        if agentIndex <= self._game.state.getNumGhostAgents()
            return 0

        # Daca e pacman verificam daca putem invoca si alte fantome sa ne ajute !
        if agentIndex == 0:
            return self.eat(agentIndex)
        
        # Daca e o fantoma pacman ii actualizam timpul de stat in viata
        despawned = False

        agentState = self._game.state.data.agentStates[agentIndex]
        self._ghostPacmanAgents[agentState._ghostPacmanId] = self._ghostPacmanAgents[agentState._ghostPacmanId] - 1

        if self._ghostPacmanAgents[agentState._ghostPacmanId] <= 0:
            self.despawnGhostPacman(agentIndex)
            despawned = True

        return -1 if despawned else 0
    
    def eat( self, agentIndex ):
        spawned = False

        self._eatenFoods += self._game.state.data._foodEaten is not None
        if self._eatenFoods >= numFoods:
            rnd = uniform(0, 1)
            if rnd <= self.probability:
                self.spawnGhostPacman()
                spawned = True

            self._eatenFoods -= numFoods

        return spawned

    def spawnGhostPacman( self ):
        print("Nasteee")
        agentState = self._game.state.data.agentStates[0].copy()
        agent = self.ghostPacmanAgent( len(self._game) )

        agentState._ghostPacmanId = self._ghostPacmanId
        self._ghostPacmanAgents[self._ghostPacmanId] = self.maxSteps

        self._game.display.addGhostPacmanObject(agentState, self.ghostPacmanColors)
        self._game.agents.append(agent)
        self._game.state.data.agentStates.append(agentState)

        self._ghostPacmanId += 1

    def despawnGhostPacman( self, agentIndex ):
        print("Moareee")
        agentState = self._game.state.data.agentStates[agentIndex]

        for index in range(agentIndex + 1, numAgents = self._game.state.getNumAgents()):
            self._game.agents[index].index = index - 1

        self._game.display.removeGhostPacmanObject(agentIndex)
        self._game.agents.pop(agentIndex)
        self._game.state.data.agentStates.pop(agentIndex)

        del self._ghostPacmanAgents[agentState._ghostPacmanId]




