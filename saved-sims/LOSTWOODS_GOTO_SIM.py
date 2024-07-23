from sim import GameState, actors
import copy
import cProfile

fishAddresses = set()
kusaAddresses = set()
skullKidAddresses = set()
potDrawAddrs = set()
totalAttempts = 0
totalRealAttempts = 0

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
    return addr == 0x801E8f30 or addr == 0x801f8f30 #1.2
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
    # room 2 to 3
    if 0x2 in state.loadedRooms and 0x1 not in state.loadedRooms and 0x3 not in state.loadedRooms:
        En_Kusa_ID = 0x0125
        for k in [k for k in state.heap() if k.actorId == En_Kusa_ID]:
            p_temp_state = copy.deepcopy(state)
            for remove_k in [remove_k for remove_k in state.heap() if remove_k.actorId == En_Kusa_ID]:
                if remove_k.addr != k.addr:
                    p_temp_state.dealloc(remove_k.addr)
            for node in p_temp_state.heap():
                if node.actorId in [actors.En_Bom, actors.Eff_Dust, actors.En_M_Thunder, actors.En_Insect, actors.Arms_Hook, actors.En_Bom_Chu]:
                    p_temp_state.dealloc(node.addr)
            # -------
            temp_state = copy.deepcopy(p_temp_state)
            og_temp_state = copy.deepcopy(p_temp_state)            
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
                        print("kusa.addr rm 2 to 3 " + hex(kusa.addr) + ", " + hex(kusa_draw_addr))
                        print("BEFORE ------------------")
                        for n in og_temp_state.heap():
                            print(n)
                        print("AFTER ------------------")
                        for n in temp_state.heap():
                            print(n)
                        return True

    # room 7 to 4
    if 0x7 in state.loadedRooms and 0x4 not in state.loadedRooms and 0x8 not in state.loadedRooms:
        En_Kusa_ID = 0x0125
        for k in [k for k in state.heap() if k.actorId == En_Kusa_ID]:
            p_temp_state = copy.deepcopy(state)
            for remove_k in [remove_k for remove_k in state.heap() if remove_k.actorId == En_Kusa_ID]:
                if remove_k.addr != k.addr:
                    p_temp_state.dealloc(remove_k.addr)
            for node in p_temp_state.heap():
                if node.actorId in [actors.En_Bom, actors.Eff_Dust, actors.En_M_Thunder, actors.En_Insect, actors.Arms_Hook, actors.En_Bom_Chu]:
                    p_temp_state.dealloc(node.addr)
            # -------
            temp_state = copy.deepcopy(p_temp_state)
            kusas = [node for node in temp_state.heap() if node.actorId == En_Kusa_ID]
            temp_state.loadRoom(4)
            temp_state.unloadRoomsExcept(4)
            temp_state.loadRoom(7)
            temp_state.unloadRoomsExcept(7)
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
                        print("kusa.addr rm 7 to 4 " + hex(kusa.addr) + ", " + hex(kusa_draw_addr))
                        for n in temp_state.heap():
                            print(n)
                        return True


    # room 7 to 8
    if 0x7 in state.loadedRooms and 0x4 not in state.loadedRooms and 0x8 not in state.loadedRooms:
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
            temp_state.loadRoom(8)
            temp_state.unloadRoomsExcept(8)
            temp_state.loadRoom(7)
            temp_state.unloadRoomsExcept(7)
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
                        print("kusa.addr rm 7 to 8 " + hex(kusa.addr) + ", " + hex(kusa_draw_addr))
                        for n in temp_state.heap():
                            print(n)
                        return True

    # room 8 to 7
    if 0x8 in state.loadedRooms and 0x7 not in state.loadedRooms:
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
            temp_state.loadRoom(7)
            temp_state.unloadRoomsExcept(7)
            temp_state.loadRoom(8)
            temp_state.unloadRoomsExcept(8)
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
                        print("kusa.addr rm 8 to 7 " + hex(kusa.addr) + ", " + hex(kusa_draw_addr))
                        for n in temp_state.heap():
                            print(n)
                        return True



    return False


def checkSkullKidDrawpointer(state):
    global totalAttempts
    totalAttempts += 1
    if actors.En_Kusa not in state.actorStates:
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
            temp_state.loadRoom(1)
            temp_state.unloadRoomsExcept(1)
            temp_state.loadRoom(2)
            temp_state.unloadRoomsExcept(2)
            temp_state.loadRoom(1)
            skull_kid_draw_addr = temp_state.actorStates[actors.En_Kusa]['loadedOverlay']+temp_state.headerSize+0x30f0
            skullkids = [node for node in temp_state.heap() if node.actorId == actors.En_Skj]
            if skull_kid_draw_addr < 0x801f0000 or skull_kid_draw_addr > 0x801ffffc:
                return False
            if skull_kid_draw_addr not in skullKidAddresses:
                print('%08X (%d)\n'%(skull_kid_draw_addr, totalAttempts), end='')
                skullKidAddresses.add(skull_kid_draw_addr)
                kusa_text = ""
                skull_text = ""
                for kusa in kusas: 
                    kusa_text = kusa_text + hex(kusa.addr+kusa.headerSize+0xb4) + ", "
                for skullkid in skullkids:
                    skull_text = skull_text + hex(skullkid.addr+skullkid.headerSize+0x134) + ", "
                print("Kusa x rot: " + kusa_text + " and SkullKid DrawPtrs: " + skull_text)
            for kusa in kusas:
                for skullkid in skullkids:
                    if kusa.addr + kusa.headerSize + 0xb4 == skullkid.addr + skullkid.headerSize + 0x134:
                        for n in temp_state.heap():
                            print(n)
                        print("kusa.addr " + hex(kusa.addr) + ", " + hex(skull_kid_draw_addr))
                        return True
    return False


def checkPotDrawpointer(state):
    global totalAttempts
    global totalRealAttempts
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
            totalRealAttempts += 1
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


def checkGrotto(state):
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

    if 0x7 in state.loadedRooms and 0x4 not in state.loadedRooms and 0x8 not in state.loadedRooms:
        En_Kusa_ID = 0x0125
#        for k in [k for k in state.heap() if k.actorId == En_Kusa_ID]:
#            p_temp_state = copy.deepcopy(state)
#            for remove_k in [remove_k for remove_k in state.heap() if remove_k.actorId == En_Kusa_ID]:
#                # if remove_k.addr != k.addr:
#                #     print(f"WE ARE KILLING KUSA {hex(remove_k.addr)}")
#                #     p_temp_state.dealloc(remove_k.addr)
#                pass
        p_temp_state = copy.deepcopy(state)
        for node in p_temp_state.heap():
            if node.actorId in [actors.En_Bom, actors.Eff_Dust, actors.En_M_Thunder, actors.En_Insect, actors.Arms_Hook, actors.En_Bom_Chu]:
                print(f"WE ARE ALSO KILLING ACTOR {node.actorId} AT ADDRESS {hex(node.addr)}")
                p_temp_state.dealloc(node.addr)
            if node.actorId == actors.En_Kusa and node.addr + node.headerSize != 0x801e8910:
                print(f"WE ARE ALSO KILLING ACTOR {node.actorId} AT ADDRESS {hex(node.addr)}")
                p_temp_state.dealloc(node.addr)
        # -------
        p_temp_state = copy.deepcopy(p_temp_state)
        kusas = [node for node in p_temp_state.heap() if node.actorId == En_Kusa_ID]
        p_temp_state.loadRoom(4)
        p_temp_state.unloadRoomsExcept(4)
        p_temp_state.loadRoom(6)
        p_temp_state.unloadRoomsExcept(6)

        grotto = None

        for node in p_temp_state.heap():
            if node.actorId == actors.Door_Ana:
                grotto = node

        if grotto is None:
            print("no grotto!")
            [print(node) for node in p_temp_state.heap()]
            # how did this happen
        else:
            grottoOvl           = p_temp_state.actorStates[actors.Door_Ana]['loadedOverlay']
            grottoOvlPlusHeader = grottoOvl + p_temp_state.headerSize
            grottoOvlOffset     = grottoOvlPlusHeader + 0x5e6
            print(":: Grotto after SRM ...")
            print(f'Door_Ana {hex(grottoOvlPlusHeader)}, destination {hex(grottoOvlOffset)}')
             
            for kusa in kusas:
                if kusa.addr + kusa.headerSize + 0x26 == grottoOvlOffset:
                    print(f'!!!!!!!!!!!!!!!!')
                    print(f'kusa addr is {hex(kusa.addr + kusa.headerSize)}')
                    print(f'kusa 2nd half of the float x addr is {hex(kusa.addr + kusa.headerSize + 0x26)}')
                    print(f'grotto addr is {hex(grottoOvlPlusHeader)}')
                    print(f'grotto entrance addr is {hex(grottoOvlOffset)}')
                    print(f'!!!!!!!!!!!!!!!!')
                    [print(node) for node in p_temp_state.heap()]
                    return True
                else:
                    print(f'off by: {hex((kusa.addr + kusa.headerSize + 0x26) - (grottoOvlOffset))} - kusa addr {hex(kusa.addr + kusa.headerSize + 0x26)}, grotto addr {hex(grottoOvlOffset)}')
    return False

def checkLightNodeLostWoodsAdult(state):
    global totalAttempts
    global totalRealAttempts
    totalAttempts += 1
    if (totalAttempts % 2000 == 0):
        print('Attempt %d (%d)'%(totalRealAttempts, totalAttempts))
    if actors.En_Kusa not in state.actorStates:
        return False
    if actors.En_Bom in state.actorStates:
        if state.actorStates[actors.En_Bom]['numLoaded'] > 0:
            return False
    if actors.En_M_Thunder in state.actorStates:
        if state.actorStates[actors.En_M_Thunder]['numLoaded'] > 0:
            return False
    # room 2 to 3
    if 0x7 in state.loadedRooms and 0x4 not in state.loadedRooms and 0x8 not in state.loadedRooms:
        En_Kusa_ID = 0x0125
        for k in [k for k in state.heap() if k.actorId == En_Kusa_ID]:
            p_temp_state = copy.deepcopy(state)
            for remove_k in [remove_k for remove_k in state.heap() if remove_k.actorId == En_Kusa_ID]:
                if remove_k.addr != k.addr:
                    p_temp_state.dealloc(remove_k.addr)
            for node in p_temp_state.heap():
                if node.actorId in [actors.En_Bom, actors.Eff_Dust, actors.En_M_Thunder, actors.En_Insect, actors.Arms_Hook, actors.En_Bom_Chu]:
                    p_temp_state.dealloc(node.addr)
                if node.actorId == actors.En_Kusa and node.addr + node.headerSize != 0x801e8910:
                    p_temp_state.dealloc(node.addr)
            # -------
            temp_state = copy.deepcopy(p_temp_state)
            og_temp_state = copy.deepcopy(p_temp_state)            
            kusas = [node for node in temp_state.heap() if node.actorId == En_Kusa_ID]
            temp_state.loadRoom(4)
            temp_state.unloadRoomsExcept(4)
            temp_state.loadRoom(3)
            totalRealAttempts += 1
            fairies = [node for node in temp_state.heap() if node.actorId == actors.En_Elf]
            for kusa in kusas:
                for fairy in fairies:
                    if kusa.addr + kusa.headerSize + 0xb4 == fairy.addr + fairy.headerSize + 0x264:
                        print("kusa.addr rm 2 to 3 " + hex(kusa.addr))
                        print("BEFORE ------------------")
                        for n in og_temp_state.heap():
                            print(n)
                        print("AFTER ------------------")
                        for n in temp_state.heap():
                            print(n)
                        return True


state = GameState('OoT', 'OoT-N-1.2', {'lullaby':True, 'saria':False, 'bombchu':True, 'bomb':True, 'bottle':True, 'hookshot':True, 'clearedRooms':[], 'beanPlanted':False, 'switchFlags':[], 'collectibleFlags':[]}) # 0x7, 0x11
state.loadScene(sceneId=0x5b, setupId=0x2, roomId=0x2)


# ret = state.search(checkPotDrawpointer, indefinite=True, forceMagic=True, blockedRooms=[0x2], keepFishOverlay=True)
# ret = state.search(checkFishAddress, indefinite=True, forceMagic=True, blockedRooms=[0x1], blockedActors=[], peekRooms=[0x1])

#ret = state.search(checkBushDrawpointer, blockedRooms=[0x1], blockedActors=[actors.En_Insect])

[print(node) for node in state.heap()]

# ret = state.search(checkGrotto, blockedRooms=[0x1], peekRooms=[0x1], blockedActors=[], forceMagic=False, indefinite=True)

state.loadRoom(3)
state.unloadRoomsExcept(3)
state.loadRoom(4)
state.allocActorWithRoom(33, 4)
state.unloadRoomsExcept(4)
state.loadRoom(7)
state.unloadRoomsExcept(7)
state.allocActorWithRoom(33, 7)

ret = state.search(checkGrotto, blockedRooms=[0x1], peekRooms=[0x1], blockedActors=[], forceMagic=False, indefinite=False)

# print(ret)
# print([hex(x) for x in sorted(fishAddresses)])


