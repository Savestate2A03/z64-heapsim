from sim import GameState, actors

fishAddresses = set()
def checkFishAddress(gameState):
    if 'loadedOverlay' not in gameState.actors[En_Fish]:
        gameState = copy.deepcopy(gameState)
        gameState.allocActor(En_Fish)
    fishAddresses.add(gameState.actors[En_Fish]['loadedOverlay'])
    return gameState.actors[En_Fish]['loadedOverlay'] == 0x801F8F30


gameState = GameState('OoT', 'OoT-N-1.2', {'lullaby':True, 'saria':True, 'bombchu':True, 'bomb':True, 'bottle':True})
gameState.loadScene(sceneId=0x5B, setupId=0, roomId=0)

#print(gameState.search(5, checkFishAddress))
#print([hex(x) for x in sorted(fishAddresses)])

bombchu = gameState.allocActor(actors.En_Bom_Chu)
gameState.loadRoom(1)
print(gameState)
print()
gameState.unloadRoomsExcept(1)
gameState.dealloc(bombchu.addr)
gameState.loadRoom(2)
gameState.allocActor(actors.En_Fish)
print(gameState)
