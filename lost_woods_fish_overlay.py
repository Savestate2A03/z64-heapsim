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
    return addr == 0x801F8F30 #1.2
    #return addr == 0x801F8880 #1.0


gameState = GameState('OoT', 'OoT-N-1.2', {'lullaby':True, 'saria':True, 'bombchu':True, 'bomb':False, 'bottle':True, 'clearedRooms':[], 'beanPlanted':False, 'switchFlags':[], 'collectibleFlags':[]})
gameState.loadScene(sceneId=0x5B, setupId=0, roomId=0)

ret = gameState.search(20, checkFishAddress)
print(ret)
print([hex(x) for x in sorted(fishAddresses)])


