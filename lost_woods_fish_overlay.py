from sim import GameState, actors
import copy

fishAddresses = set()
def checkFishAddress(state):
    if 'loadedOverlay' not in state.actors[actors.En_Fish]:
        state = copy.deepcopy(state)
        state.allocActor(actors.En_Fish)
    addr = state.actors[actors.En_Fish]['loadedOverlay']+state.headerSize
    if addr not in fishAddresses:
        print(hex(addr))
        fishAddresses.add(addr)
    return addr == 0x801F8F30 #1.2
    #return addr == 0x801F8880 #1.0


state = GameState('OoT', 'OoT-N-1.2', {'lullaby':True, 'saria':True, 'bombchu':True, 'bomb':False, 'bottle':False, 'clearedRooms':[], 'beanPlanted':False, 'switchFlags':[], 'collectibleFlags':[]})
state.loadScene(sceneId=0x5B, setupId=0, roomId=0)

ret = state.search(checkFishAddress)
print(ret)
print([hex(x) for x in sorted(fishAddresses)])


