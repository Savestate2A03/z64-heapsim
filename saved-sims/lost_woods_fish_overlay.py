from sim import GameState, actors
import copy

import cProfile

fishAddresses = set()
kusaAddresses = set()
potDrawAddrs = set()
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
    return addr == 0x801E8F30 or addr == 0x801f8f30 #1.2
    #return addr == 0x801F8880 #1.0

def checkBushDrawpointer(state):
    global totalAttempts
    totalAttempts += 1
    if actors.En_Kusa not in state.actorStates:
        return False
    if actors.En_Bom in state.actorStates:
        if state.actorStates[actors.En_Bom]['numLoaded'] > 0:
            return False
    if actors.En_M_Thunder in state.actorStates:
        if state.actorStates[actors.En_M_Thunder]['numLoaded'] > 0:
            return False
    if 0x2 in state.loadedRooms and 0x1 not in state.loadedRooms and 0x3 not in state.loadedRooms:
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
            temp_state.loadRoom(2)
            temp_state.unloadRoomsExcept(2)
            kusa_draw_addr = temp_state.actorStates[actors.En_Kusa]['loadedOverlay']+temp_state.headerSize+0x11a0
            if kusa_draw_addr not in kusaAddresses:
                print('%08X (%d)\n'%(kusa_draw_addr, totalAttempts), end='')
                kusaAddresses.add(kusa_draw_addr)
            if kusa_draw_addr < 0x801f0000:
                return False
            kusas2 = [node for node in temp_state.heap() if node.actorId == En_Kusa_ID]
            for kusa in kusas:
                for kusa2 in kusas2:
                    if kusa.addr + kusa.headerSize + 0xb4 == kusa2.addr + kusa2.headerSize + 0x134:
                        print("kusa.addr rm 3 " + hex(kusa.addr) + ", " + hex(kusa_draw_addr))
                        for n in temp_state.heap():
                            print(n)
                        return True
    return False


def checkPotDrawpointer(state):
    global totalAttempts
    totalAttempts += 1
    if actors.Obj_Tsubo not in state.actorStates:
        return False
    if actors.En_Bom in state.actorStates:
        if state.actorStates[actors.En_Bom]['numLoaded'] > 0:
            return False
    if actors.En_M_Thunder in state.actorStates:
        if state.actorStates[actors.En_M_Thunder]['numLoaded'] > 0:
            return False
    if 0x3 in state.loadedRooms and 0x2 not in state.loadedRooms and 0x0 not in state.loadedRooms and 0x1 not in state.loadedRooms:
        Obj_Tsubo_Id = 0x0111
        for k in state.heap():
            if k.actorId != Obj_Tsubo_Id:
                continue
            p_temp_state = copy.deepcopy(state)
            for node in p_temp_state.heap():
                if node.actorId in [actors.En_Bom, actors.Eff_Dust, actors.En_M_Thunder, actors.En_Insect]:
                    p_temp_state.dealloc(node.addr)
            # -------
            temp_state = copy.deepcopy(p_temp_state)
            pots = [node for node in temp_state.heap() if node.actorId == Obj_Tsubo_Id and (node.actorParams == 0x7108 or node.actorParams == 0x7903)]
            temp_state.loadRoom(1)
            temp_state.unloadRoomsExcept(1)
            temp_state.loadRoom(3)
            # pot_draw_addr = temp_state.actorStates[actors.Obj_Tsubo]['loadedOverlay']+temp_state.headerSize+0xD9C
            #if pot_draw_addr not in potDrawAddrs:
            #    print('%08X (%d)\n'%(pot_draw_addr, totalAttempts), end='')
            #    potDrawAddrs.add(pot_draw_addr)
            pots2 = [node for node in temp_state.heap()]
            for pot in pots:
                for pot2 in pots2:
                    if pot.addr + pot.headerSize + 0xb4 == pot2.addr + pot2.headerSize + 0x134:
                        for n in temp_state.heap():
                            print(n)
                        if temp_state.actorStates[pot2.actorId]['loadedOverlay'] == None:
                            print(str(totalAttempts) + "| pot.addr " + hex(pot.addr) + ", modifying " + hex(pot2.addr) + " actorId " + hex(pot2.actorId) + " with overlay UNKNOWN")
                        else: 
                            print(str(totalAttempts) + "| pot.addr " + hex(pot.addr) + ", modifying " + hex(pot2.addr) + " actorId " + hex(pot2.actorId) + " with overlay " + hex(temp_state.actorStates[pot2.actorId]['loadedOverlay']+temp_state.headerSize))
                        return True
    return False




state = GameState('OoT', 'OoT-N-1.2', {'lullaby':True, 'saria':True, 'bombchu':False, 'bomb':True, 'bottle':False, 'clearedRooms':[], 'beanPlanted':False, 'switchFlags':[0x8, 0xc, 0xb, 0x0, 0x1b, 0x1c], 'collectibleFlags':[]})
state.loadScene(sceneId=0x62, setupId=2, roomId=3)

#state = GameState('OoT', 'OoT-N-1.2', {'lullaby':True, 'saria':True, 'bombchu':False, 'bomb':True, 'bottle':True, 'clearedRooms':[], 'beanPlanted':False, 'switchFlags':[0x11, 0x7], 'collectibleFlags':[]})
#state.loadScene(sceneId=0x5b, setupId=2, roomId=2)

# (<sim.sim.GameState object at 0x0b7d2890>, 
# (['allocActor', 16], 
# ['loadRoom', 0], 
# ['unloadRoomsExcept', 0], 
# ['allocActor', 16], 
# ['allocActor', 16], 
# ['allocPairedActors', [87, 257]], 
# ['loadRoom', 3], 
# ['unloadRoomsExcept', 3]))
# 
# drop fish

bomb1 = state.allocActor(actors.En_Bom)

state.loadRoom(0)
state.unloadRoomsExcept(0)

bomb2 = state.allocActor(actors.En_Bom)
bomb3 = state.allocActor(actors.En_Bom)
thunder = state.allocActor(actors.En_M_Thunder)
dust = state.allocActor(actors.Eff_Dust)

state.loadRoom(3)
state.unloadRoomsExcept(3)

state.dealloc(bomb1.addr)
state.dealloc(bomb2.addr)
state.dealloc(bomb3.addr)
state.dealloc(thunder.addr)
state.dealloc(dust.addr)

fishy = state.allocActorWithRoom(actors.En_Fish, 3)

# 
# state.loadRoom(1)
# state.unloadRoomsExcept(1)
# 

# [print(node) for node in state.heap()]

ret = state.search(checkPotDrawpointer, indefinite=True, forceMagic=True, blockedRooms=[0x2], keepFishOverlay=True)
#ret = state.search(checkFishAddress, indefinite=True, forceMagic=True, blockedRooms=[0x2, 0x0])

#ret = state.search(checkBushDrawpointer, blockedRooms=[0x1], blockedActors=[actors.En_Insect])
#ret = state.search(checkBushDrawpointer, blockedRooms=[0x1], peekRooms=[0x1], blockedActors=[], forceMagic=True, indefinite=True)

# print(ret)
# print([hex(x) for x in sorted(fishAddresses)])


