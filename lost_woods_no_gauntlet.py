from sim import GameState, actors
import copy

results = set()
def checkDrawPointers(state):

    for node in state.heap():
        if node.addr >= 0x801EC000:
            break
        if node.actorId and node.actorId not in [actors.En_Dnt_Nomal, actors.En_Kusa, actors.En_Wonder_Item] and not (node.actorId==actors.En_Skj and node.actorParams==0x1BFF) and 'loadedOverlay' in state.actors[node.actorId] and state.actors[node.actorId]['loadedOverlay'] >= 0x801ED1A0:
            results.add((str(node), str(state.ram[state.actors[node.actorId]['loadedOverlay']])))
            #print('!!!')
            return True
    return False


    
    #if 'loadedOverlay' not in state.actors[actors.En_Fish]:
    #    state = copy.deepcopy(state)
    #    state.allocActor(actors.En_Fish)
    #addr = state.actors[actors.En_Fish]['loadedOverlay']+state.headerSize
    #if addr not in fishAddresses:
    #    print(hex(addr))
    #    fishAddresses.add(addr)
    #return False#return addr == 0x801F8F30


#print(state)

for i in range(0,100):

    print(i)

    state = GameState('OoT', 'OoT-N-1.2', {'lullaby':False, 'saria':False, 'bombchu':False, 'bomb':False, 'bottle':False, 'clearedRooms':[], 'beanPlanted':False})
    state.loadScene(sceneId=0x5B, setupId=0, roomId=0)

    state.changeRoom(1)
    state.changeRoom(2)
    state.changeRoom(3)
    state.changeRoom(4)
    state.changeRoom(7)
    state.changeRoom(4)
    state.changeRoom(3)

    
    ret = state.search(i, checkDrawPointers, carryingActor=True)
    print(ret)
    print(results)
    if (ret or results):
        print(i)
        break
