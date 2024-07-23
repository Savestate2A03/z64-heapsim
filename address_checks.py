from sim import GameState, actors
import copy
import cProfile

# ------------------------------------------------------------------------ #
# This file contains the various checks that the simulator uses each       #
# time it propagates forward, once per available action.                   #
# ------------------------------------------------------------------------ #
# Crafted by MrCheeze and heavily modified / new stuff added by Savestate. #
# ------------------------------------------------------------------------ #

class LostWoods:
    def __init__(self, state, addresses):
        # Keeps track of addresses already found.
        # Implementation of use is up to the developer of the check.
        self.fishAddresses     = set()
        self.kusaAddresses     = set()
        self.skullKidAddresses = set()
        # Tracking attempts. totalRealAttempts counts the total
        # number of times an attempt at (developer implementation)
        # was able to be taken. totalAttempts is much less strict.
        self.totalAttempts     = 0
        self.totalRealAttempts = 0
        self.state             = state
        self.addresses         = addresses

    def info(self):
        return {
            "fish":          self.fishAddresses,
            "kusa":          self.kusaAddresses,
            "skullkid":      self.skullKidAddresses,
            "attempts":      self.totalAttempts,
            "real-attempts": self.totalRealAttempts,
        }

    def fish8011xxxxRotWrite(self, state):
        self.totalAttempts += 1

        # Create a deep copy of the state so we don't modify the working copy
        state = copy.deepcopy(state)

        # Deallocate all problem actors before simulating...
        # In this case, we can't drop a fish while charging spin attack.
        for node in state.heap():
            if node.actorId in [actors.Eff_Dust, actors.En_M_Thunder]:
                state.dealloc(node)

        # If fish or its overlay is not currently in the heap, make a deep copy of the state and allocate it there.
        # (Deep copies of objects allow you to make a separate copy of it to modify without touching the original)
        if actors.En_Fish not in state.actorStates or 'loadedOverlay' not in state.actorStates[actors.En_Fish]:
            state.allocActor(actors.En_Fish)

        # Get the address of the fish overlay in the actor heap, accounting for the header size of the
        # current OoT version (0x30 for 1.0-1.2, 0x10 for GC).
        addr = state.actorStates[actors.En_Fish]['loadedOverlay']+state.headerSize

        # Add to our fish address list if we have not had the fish overlay load here yet.
        if addr not in self.fishAddresses:
            for address in self.addresses:
                distance = f'{hex(addr - address)}' if (addr - address < 0) else f' {hex(addr - address)}'
                print('%08X (%d)'%(addr, self.totalAttempts) + f', {distance} away from {hex(address)}')
                self.fishAddresses.add(addr)

        # If the fish overlay loaded in one of our desired spots, then let the simulator know that we have
        # fulfilled the requirements for this check by returning true.
        for address in self.addresses:
            if addr == address:
                return True

        return False # Otherwise, keep on searching

    def bushDraw(self, state):
        self.totalAttempts += 1

        # This check has quite a lot going on, so I will try to break it down with comments.
        # We simulate a proper SRM superslide below, so if there's no kusas available at this
        # iteration of our breadth first search, instantly fail the test.
        if actors.En_Kusa not in state.actorStates:
            return False

        # If there's any bombs loaded, instantly fail because the rest of the check assumes
        # all non-room associated actors will stay loaded from this point on.
        if actors.En_Bom in state.actorStates:
            if state.actorStates[actors.En_Bom]['numLoaded'] > 0:
                return False

        # Same thing for spin attack. Plus it's impossible to perform SRM while spin-attacking
        if actors.En_M_Thunder in state.actorStates:
            if state.actorStates[actors.En_M_Thunder]['numLoaded'] > 0:
                return False

        #######################################################
        # This next check goes through the whole SRM process  #
        # starting from the current state. They are all the   #
        # same for the most part, just changing which rooms   #
        # we start from, and go to with the superslide.       #
        #######################################################

        # There are 4 implemented room transitions supported
        # --- Room 2 to 3
        # --- Room 2 to 1
        # --- Room 7 to 4
        # --- Room 7 to 8
        # --- Room 8 to 7

        # s:  Starting room
        # b1: Blocked room 1 (when starting, can't be loaded)
        # b2: Blocked room 2 (when starting, can't be loaded)
        # ss: Room to superslide to
        # d:  Destination

        actionConfiguration = [
            {'s': 0x2, 'b1': 0x1, 'b2': 0x3, 'ss': 0x3, 'd': 0x2},
            {'s': 0x2, 'b1': 0x1, 'b2': 0x3, 'ss': 0x1, 'd': 0x2},
            {'s': 0x7, 'b1': 0x4, 'b2': 0x8, 'ss': 0x4, 'd': 0x7},
            {'s': 0x7, 'b1': 0x4, 'b2': 0x8, 'ss': 0x8, 'd': 0x7},
            {'s': 0x8, 'b1': 0x7, 'b2': 0x7, 'ss': 0x7, 'd': 0x8},
        ]
        
        for a in actionConfiguration:
            # First make sure that our desired starting room is the only
            # one loaded according to our current action configuration.
            if not (a['s'] in state.loadedRooms and 
                    a['b1'] not in state.loadedRooms and
                    a['b2'] not in state.loadedRooms):
                continue

            # Assigning the actor ID to a variable helps a lot with readability.
            En_Kusa_ID = 0x0125

            # For loop through all the kusas on the heap using list comprehension
            # 'k' will be our current kusa, there should only be three.
            for k in [k for k in state.heap() if k.actorId == En_Kusa_ID]:

                # Make a deep copy of the current state so we can modify it 
                # as we simulate SRM without messing up the original state
                # that was passed into this method.
                p_temp_state = copy.deepcopy(state)

                # Deallocate all kusas except for the one we are about to simulate SRM off of.
                # Not necessary, can be commented out, and realistically it would be best if
                # this was modified to check 0, 1, and 2 kusas deallocated. Maybe in da future.
                for remove_k in [remove_k for remove_k in state.heap() if remove_k.actorId == En_Kusa_ID]:
                    if remove_k.addr != k.addr:
                        p_temp_state.dealloc(remove_k)
                
                # Deallocate all problem actors before simulating SRM.
                for node in p_temp_state.heap():
                    if node.actorId in [actors.En_Bom, actors.Eff_Dust, actors.En_M_Thunder,
                                        actors.En_Insect, actors.Arms_Hook, actors.En_Bom_Chu]:
                        p_temp_state.dealloc(node)

                # Create more deep copies, this time of our modified deep copy.
                # We need to be able to check if the kusas' rotations in this loop
                # overlaps with any of the kusas after the SRM simulation.
                temp_state = copy.deepcopy(p_temp_state)
                og_temp_state = copy.deepcopy(p_temp_state)            
                
                # Gather the kusas before starting SRM simulation.
                kusas = [node for node in temp_state.heap() if node.actorId == En_Kusa_ID]

                # Simulate superslide SRM. We don't need to simulate bringing the bush with us
                # because it gets unloaded and thus doesn't affect the heap.
                temp_state.loadRoom(a['ss'])
                temp_state.unloadRoomsExcept(a['ss'])
                temp_state.loadRoom(a['d'])
                temp_state.unloadRoomsExcept(a['d'])

                # Get the address of the kusas' draw function (it's shared by every kusa) and
                # add it to the kusaAddresses set. Not particularly useful to print out to the
                # screen but it's useful to see what kind of results you're getting sometimes.
                kusa_draw_addr = temp_state.actorStates[actors.En_Kusa]['loadedOverlay']+temp_state.headerSize+0x11a0
                if kusa_draw_addr not in self.kusaAddresses:
                    print(f'drawptr: {hex(kusa_draw_addr)} ({self.totalAttempts}), superslide from {a["s"]} to {a["ss"]} then {a["d"]}')
                    # print('%08X (%d)\n'%(kusa_draw_addr, self.totalAttempts), end='')
                    self.kusaAddresses.add(kusa_draw_addr)

                # 0x801eXXXX allocated kusas will almost guaranteed get overwritten, not worth checking.
                if kusa_draw_addr < 0x801f0000:
                    continue

                # kusas2 is the state from after the superslide, and kusas is from before.
                kusas2 = [node for node in temp_state.heap() if node.actorId == En_Kusa_ID]
                for kusa in kusas:
                    for kusa2 in kusas2:
                        # Calculate the rotation address and the draw pointer address
                        # for both the kusas we can SRM off of and the kusas that are
                        # in the room we went to with the SRM'd kusa in-hand. 
                        kusaRot      = kusa.addr  + kusa.headerSize  + 0xb4
                        kusa2DrawPtr = kusa2.addr + kusa2.headerSize + 0x134
                        if kusaRot == kusa2DrawPtr:
                            print(f'####################################')
                            print(f'------------ HEAP DUMPS ------------')
                            print(f'####################################')
                            print(" -- ::::::: BEFORE ::::::: --")
                            for n in og_temp_state.heap():
                                print(n)
                            print("-- ::::::: AFTER ::::::: --")
                            for n in temp_state.heap():
                                print(n)
                            print(f'###################################################')
                            print(f'Superslide from room {a["s"]} to {a["ss"]}')
                            print(f'-- [kusa ovly] -- {hex(kusa_draw_addr)}')
                            print(f'-- [srmd kusa] -- address: {hex(kusa.addr)}, rot: {hex(kusaRot)}')
                            print(f'-- [draw kusa] -- address: {hex(kusa2.addr)}, drawptr: {hex(kusa2DrawPtr)}')
                            print(f'###################################################')
                            return True
        return False

    def skullKidDraw(self, state):
        self.totalAttempts += 1
        if actors.En_Kusa not in state.actorStates:
            return False
        if 0x2 in state.loadedRooms and 0x1 not in state.loadedRooms and 0x3 not in state.loadedRooms:
            En_Kusa_ID = 0x0125
            for k in [k for k in state.heap() if k.actorId == En_Kusa_ID]:
                p_temp_state = copy.deepcopy(state)
                for remove_k in [remove_k for remove_k in state.heap() if remove_k.actorId == En_Kusa_ID]:
                    if remove_k.addr != k.addr:
                        p_temp_state.dealloc(remove_k)
                for node in p_temp_state.heap():
                    if node.actorId in [actors.En_Bom, actors.Eff_Dust, actors.En_M_Thunder, actors.En_Insect]:
                        p_temp_state.dealloc(node)
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
                if skull_kid_draw_addr not in self.skullKidAddresses:
                    print('%08X (%d)\n'%(skull_kid_draw_addr, self.totalAttempts), end='')
                    self.skullKidAddresses.add(skull_kid_draw_addr)
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

    def grottoDestination(self, state):
        self.totalAttempts += 1
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
            for k in [k for k in state.heap() if k.actorId == En_Kusa_ID]:
                p_temp_state = copy.deepcopy(state)
                for remove_k in [remove_k for remove_k in state.heap() if remove_k.actorId == En_Kusa_ID]:
                    pass # Originally removed kusas, deleted because we need them to SRM with them rofl
                for node in p_temp_state.heap():
                    # Before we superslide, make sure no trouble actors are loaded.
                    # The sim doesn't know that we can't realistically setup superslide with these loaded
                    if node.actorId in [actors.En_Bom, actors.Eff_Dust, actors.En_M_Thunder, actors.En_Insect, actors.Arms_Hook, actors.En_Bom_Chu]:
                        print(f"WE ARE KILLING ACTOR {node.actorId} AT ADDRESS {hex(node.addr)}")
                        p_temp_state.dealloc(node)
                # -------
                temp_state = copy.deepcopy(p_temp_state)
                # These are the three kusas in Room 7 before we superslide that
                # will be checked for overlapping with the Grotto scene list. 
                kusas = [node for node in temp_state.heap() if node.actorId == En_Kusa_ID]
                temp_state.loadRoom(4)
                temp_state.unloadRoomsExcept(4)
                temp_state.loadRoom(6)
                temp_state.unloadRoomsExcept(6)

                grotto = None
                for node in temp_state.heap():
                    if node.actorId == actors.Door_Ana:
                        grotto = node

                if grotto is None:
                    # This should never happen
                    print("no grotto!")
                    [print(node) for node in temp_state.heap()]
                else:
                    print(":: Grotto after SRM ...")
                    print(f'Door_Ana {hex(grotto.addr+grotto.headerSize)}, destination {hex(grotto.addr+grotto.headerSize + 0x5e6)}')
                     
                    for kusa in kusas:
                        if kusa.addr + kusa.headerSize + 0x26 == grotto.addr + grotto.headerSize + 0x5e6:
                            print(f'!!!!!!!!!!!!!!!!')
                            print(f'kusa addr is {hex(kusa.addr + kusa.headerSize)}')
                            print(f'kusa 2nd half of the float x addr is {hex(kusa.addr + kusa.headerSize + 0x26)}')
                            print(f'grotto addr is {hex(grotto.addr + grotto.headerSize)}')
                            print(f'grotto entrance addr is {hex(grotto.addr + grotto.headerSize + 0x5e6)}')
                            print(f'!!!!!!!!!!!!!!!!')
                            return True
                        else:
                            print(f'off by: {hex((kusa.addr + kusa.headerSize + 0x26) - (grotto.addr + grotto.headerSize + 0x5e6))} - kusa addr {hex(kusa.addr + kusa.headerSize + 0x26)}, grotto addr {hex(grotto.addr + grotto.headerSize + 0x5e6)}')
        return False

    def lightNodeLostWoodsAdult(self, state):
        self.totalAttempts += 1
        if (self.totalAttempts % 2000 == 0):
            print('Attempt %d (%d)'%(self.totalRealAttempts, self.totalAttempts))
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
                        p_temp_state.dealloc(remove_k)
                for node in p_temp_state.heap():
                    if node.actorId in [actors.En_Bom, actors.Eff_Dust, actors.En_M_Thunder, actors.En_Insect, actors.Arms_Hook, actors.En_Bom_Chu]:
                        p_temp_state.dealloc(node)
                # -------
                temp_state = copy.deepcopy(p_temp_state)
                og_temp_state = copy.deepcopy(p_temp_state)            
                kusas = [node for node in temp_state.heap() if node.actorId == En_Kusa_ID]
                temp_state.loadRoom(4)
                temp_state.unloadRoomsExcept(4)
                temp_state.loadRoom(3)
                self.totalRealAttempts += 1
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

class GoronCity:
    def __init__(self, state):
        self.fishAddresses     = set()
        self.potDrawAddrs      = set()
        self.totalAttempts     = 0
        self.totalRealAttempts = 0

    def info(self):
        return {
            "fish":          self.fishAddresses,
            "pot":           self.potDrawAddrs,
            "attempts":      self.totalAttempts,
            "real attempts": self.totalRealAttempts,
        }

    # This is a duplicate of the above fish check since its location independent. Maybe make a superclass that
    # both these classes inherit? Would prevent future bloating and code duping.
    def fish8011xxxxRotWrite(self, addresses, state):
        if actors.En_Fish not in state.actorStates or 'loadedOverlay' not in state.actorStates[actors.En_Fish]:
            state = copy.deepcopy(state)
            state.allocActor(actors.En_Fish)
        addr = state.actorStates[actors.En_Fish]['loadedOverlay']+state.headerSize
        self.totalAttempts += 1
        if addr not in self.fishAddresses:
            print('%08X (%d)\n'%(addr, totalAttempts), end='')
            self.fishAddresses.add(addr)
        for address in addresses:
            if addr == address:
                return True
        return False

    def potDraw(self, state):
        self.totalAttempts += 1
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
                        p_temp_state.dealloc(node)
                # -------
                temp_state = copy.deepcopy(p_temp_state)
                pots = [node for node in temp_state.heap() if node.actorId == Obj_Tsubo_Id and (node.actorParams == 0x7108 or node.actorParams == 0x7903)]
                temp_state.loadRoom(1)
                temp_state.unloadRoomsExcept(1)
                temp_state.loadRoom(3)
                # Disable printing pot draw addresses to the screen. Can be uncommented if desired.
                # pot_draw_addr = temp_state.actorStates[actors.Obj_Tsubo]['loadedOverlay']+temp_state.headerSize+0xD9C
                #if pot_draw_addr not in self.potDrawAddrs:
                #    print('%08X (%d)\n'%(pot_draw_addr, self.totalAttempts), end='')
                #    self.potDrawAddrs.add(pot_draw_addr)
                pots2 = [node for node in temp_state.heap()]
                self.totalRealAttempts += 1
                for pot in pots:
                    for pot2 in pots2:
                        if pot.addr + pot.headerSize + 0xb4 == pot2.addr + pot2.headerSize + 0x134:
                            for n in temp_state.heap():
                                print(n)
                            if temp_state.actorStates[pot2.actorId]['loadedOverlay'] == None:
                                print(str(self.totalAttempts) + "| pot.addr " + hex(pot.addr) + ", modifying " + hex(pot2.addr) + " actorId " + hex(pot2.actorId) + " with overlay UNKNOWN")
                            else: 
                                print(str(self.totalAttempts) + "| pot.addr " + hex(pot.addr) + ", modifying " + hex(pot2.addr) + " actorId " + hex(pot2.actorId) + " with overlay " + hex(temp_state.actorStates[pot2.actorId]['loadedOverlay']+temp_state.headerSize))
                            return True
        return False
