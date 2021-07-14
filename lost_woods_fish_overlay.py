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
    return addr == 0x801F8F30 #1.2
    #return addr == 0x801F8880 #1.0

def checkBushDrawpointer(state):
    if actors.En_Kusa not in state.actorStates:
        return False
    if actors.En_Bom in state.actorStates:
        if state.actorStates[actors.En_Bom]['numLoaded'] > 0:
            return False
    if actors.En_M_Thunder in state.actorStates:
        if state.actorStates[actors.En_M_Thunder]['numLoaded'] > 0:
            return False
    if 0x2 in state.loadedRooms and 0x3 not in state.loadedRooms and 0x1 not in state.loadedRooms:
        En_Kusa_ID = 0x0125
        for k in [k for k in state.heap() if k.actorId == En_Kusa_ID]:
            p_temp_state = copy.deepcopy(state)
            for remove_k in [remove_k for remove_k in state.heap() if remove_k.actorId == En_Kusa_ID]:
                if remove_k.addr != k.addr:
                    p_temp_state.dealloc(remove_k.addr)
            for node in p_temp_state.heap():
                if node.actorId in [actors.En_Bom, actors.Eff_Dust, actors.En_M_Thunder, actors.En_Insect]:
                    p_temp_state.dealloc(node.addr)
            # -------
            temp_state = copy.deepcopy(p_temp_state)
            kusas = [node for node in temp_state.heap() if node.actorId == En_Kusa_ID]
            temp_state.loadRoom(3)
            temp_state.unloadRoomsExcept(3)
            for node in temp_state.heap():
                if node.actorId in [actors.En_Fish]:
                    temp_state.dealloc(node.addr)
            temp_state.loadRoom(2)
            kusa_draw_addr = state.actorStates[actors.En_Kusa]['loadedOverlay']+state.headerSize+0x11a0
            if kusa_draw_addr < 0x801f0000:
                return False
            kusas2 = [node for node in temp_state.heap() if node.actorId == En_Kusa_ID]
            for kusa in kusas:
                for kusa2 in kusas2:
                    if kusa.addr + kusa.headerSize + 0xb4 == kusa2.addr + kusa2.headerSize + 0x134:
                        print("kusa.addr rm 3 " + hex(kusa.addr) + ", " + hex(kusa_draw_addr))
                        return True
            # -------
            temp_state = copy.deepcopy(p_temp_state)
            kusas = [node for node in temp_state.heap() if node.actorId == En_Kusa_ID]
            temp_state.loadRoom(1)
            temp_state.unloadRoomsExcept(1)
            for node in temp_state.heap():
                if node.actorId in [actors.En_Fish]:
                    temp_state.dealloc(node.addr)
            temp_state.loadRoom(2)
            kusa_draw_addr = state.actorStates[actors.En_Kusa]['loadedOverlay']+state.headerSize+0x11a0
            if kusa_draw_addr < 0x801f0000:
                return False
            kusas2 = [node for node in temp_state.heap() if node.actorId == En_Kusa_ID]
            for kusa in kusas:
                for kusa2 in kusas2:
                    if kusa.addr + kusa.headerSize + 0xb4 == kusa2.addr + kusa2.headerSize + 0x134:
                        print("kusa.addr rm 1 " + hex(kusa.addr) + ", " + hex(kusa_draw_addr))
                        return True
    return False




# state = GameState('OoT', 'OoT-N-1.2', {'lullaby':True, 'saria':True, 'bombchu':False, 'bomb':True, 'bottle':True, 'clearedRooms':[], 'beanPlanted':False, 'switchFlags':[0x8, 0xc, 0xb], 'collectibleFlags':[]})
# state.loadScene(sceneId=0x62, setupId=2, roomId=3)

state = GameState('OoT', 'OoT-N-1.2', {'lullaby':True, 'saria':True, 'bombchu':False, 'bomb':True, 'bottle':True, 'clearedRooms':[], 'beanPlanted':False, 'switchFlags':[0x11, 0x7], 'collectibleFlags':[]})
state.loadScene(sceneId=0x5b, setupId=2, roomId=2)

# 2 > 3 > 4 > 7
# superslide into 4

# ret = state.search(checkFishAddress)

# thunder = state.allocActor(actors.En_M_Thunder)
# dust = state.allocActor(actors.Eff_Dust)
# state.dealloc(thunder.addr)
# state.dealloc(dust.addr)

#ret = state.search(checkBushDrawpointer, blockedRooms=[0x1], blockedActors=[actors.En_Insect])
ret = state.search(checkBushDrawpointer, blockedRooms=[], blockedActors=[], forceMagic=True)

print(ret)
# print([hex(x) for x in sorted(fishAddresses)])


