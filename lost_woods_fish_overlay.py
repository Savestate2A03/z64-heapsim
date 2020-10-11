from sim import GameState, actors
import copy

import cProfile

fishAddresses = set()
totalAttempts = 0
def checkFishAddress(state):
    if actors.En_Fish not in state.actorStates or 'loadedOverlay' not in state.actorStates[actors.En_Fish]:
        state = copy.deepcopy(state)
        state.allocActor(actors.En_Fish)
    addr = state.actorStates[actors.En_Fish]['loadedOverlay']+state.headerSize
    global totalAttempts
    totalAttempts += 1
    if addr not in fishAddresses:
        print('%08X (%d)\n'%(addr, totalAttempts), end='')
        fishAddresses.add(addr)
    #return addr == 0x801F8F30 #1.2
    return addr == 0x801F8880 #1.0


state = GameState('OoT', 'OoT-N-1.0', {'lullaby':True, 'saria':False, 'bombchu':True, 'bomb':False, 'bottle':False, 'clearedRooms':[], 'beanPlanted':False, 'switchFlags':[], 'collectibleFlags':[]})
state.loadScene(sceneId=0x5B, setupId=0, roomId=0)

ret = state.search(checkFishAddress)
print(ret)
print([hex(x) for x in sorted(fishAddresses)])


