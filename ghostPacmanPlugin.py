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


class GhostPacmanConfig():
    def __init__( self, enabled = True,  numFoods = 3, probability = 1 / 3, ghostPacmanAgent = GhostPacmanAgent, ghostPacmanColors = GHOST_PACMAN_COLORS ):
        self.enabled = enabled
        self.numFoods = numFoods
        self.probability = probability
        self.ghostPacmanAgent = ghostPacmanAgent
        self.ghostPacmanColors = ghostPacmanColors

        self._isInitialized = False

    def initialize( self, game, startingFoods = 0 ):
        self._eatenFoods = startingFoods

        this._game = game

        self._isInitialized = True

    def eat( self, agentIndex ):
        if not self.enabled:    return 0
        if agentIndex != 0:     return 0
        if not self._isInitialized:
            print("Not initialized!")
            return 0
        
        spawned = False

        self._eatenFoods += self._game.state.data._foodEaten is not None
        if self._eatenFoods >= numFoods:
            
            rnd = uniform(0, 1)
            if rnd <= self.probability:
                self.spawnNewGhostPacman()
                spawned = True

            self._eatenFoods -= numFoods

        return spawned

    def spawnNewGhostPacman( self ):
        print("Nasteee")
        agentState = self._game.state.data.agentStates[0].copy()
        agent = self.ghostPacmanAgent( len(self._game) )

        self._game.display.addNewGhostPacmanObject(agent.index, agentState)
        self._game.agents.append(agent)
        self._game.state.data.agentStates.append(agentState)




