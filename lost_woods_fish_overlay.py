from sim import GameState, actors
import copy

fishAddresses = set()
def checkFishAddress(gameState):
    if 'loadedOverlay' not in gameState.actors[actors.En_Fish]:
        gameState = copy.deepcopy(gameState)
        gameState.allocActor(actors.En_Fish)
    addr = gameState.actors[actors.En_Fish]['loadedOverlay']+gameState.headerSize
    if addr not in fishAddresses:
        print(hex(addr))
        fishAddresses.add(addr)
    return False#return addr == 0x801F8F30


gameState = GameState('OoT', 'OoT-N-1.2', {'lullaby':True, 'saria':True, 'bombchu':True, 'bomb':True, 'bottle':True, 'clearedRooms':[], 'beanPlanted':False})
gameState.loadScene(sceneId=0x5B, setupId=0, roomId=0)

print(gameState.search(6, checkFishAddress))
print([hex(x) for x in sorted(fishAddresses)])

#bombchu = gameState.allocActor(actors.En_Bom_Chu)
#gameState.loadRoom(1)
#print(gameState)
#print()
#gameState.unloadRoomsExcept(1)
#gameState.dealloc(bombchu.addr)
#gameState.loadRoom(2)
#gameState.allocActor(actors.En_Fish)
#print(gameState)
