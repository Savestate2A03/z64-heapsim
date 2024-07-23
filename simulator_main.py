from sim import GameState, actors
import copy
import cProfile
from address_checks import LostWoods
from sim.actors import ActorList

# Examples
# ret = state.search(checkPotDrawpointer, indefinite=True, forceMagic=True, blockedRooms=[0x2], keepFishOverlay=True)
# ret = state.search(checkFishAddress, indefinite=True, forceMagic=True, blockedRooms=[0x1], blockedActors=[], peekRooms=[0x1])
# ret = state.search(checkBushDrawpointer, blockedRooms=[0x1], blockedActors=[actors.En_Insect])
# ret = state.search(checkGrotto, blockedRooms=[0x1], peekRooms=[0x1], blockedActors=[], forceMagic=False, indefinite=True)

scenes = {
    "Lost Woods": 0x5b,
    "Goron City": 0x62
}

# :: Valid Versions ::
# - OoT-N-1.0
# - OoT-N-1.1
# - OoT-P-1.0
# - OoT-N-1.2
# - OoT-P-1.1
# - OoT-J-GC-MQDisc
# - OoT-J-MQ
# - OoT-U-GC
# - OoT-U-MQ
# - OoT-P-GC
# - OoT-P-MQ
# - OoT-J-GC-CEDisc
# - OoT-iQue

# This creates the initial state that the simulator uses for certain cases (ex: should owl be loaded).
# Cleared rooms and switch/collectible flags can be found by using gz's logging function

state = GameState('OoT', 'OoT-J-GC-MQDisc',
    {'lullaby':True, 'saria':True, 'bombchu':True,
     'bomb':True, 'bottle':True, 'hookshot':False,
     'clearedRooms':[], 'beanPlanted':False, 'switchFlags':[], 'collectibleFlags':[]})

# Then we load a scene and room and setup (note: setups are now called overlays)
state.loadScene(sceneId=scenes["Lost Woods"], setupId=0x0, roomId=0x0)

# Print the initial heap, useful for debugging in Spectrum
[print(node) for node in state.heap()]

# You can pre-load the state with actions before starting the simulation search!
# All available actions are available in getAvailableActions in sim/sim.py
# -----------------------------------------
# state.loadRoom(3) # go into mido room ...
# state.unloadRoomsExcept(3)
# state.loadRoom(4) # both rooms 3 and 4 loaded
# state.allocMultipleActorsWithRoom(actors.En_Insect, 3, 4) # load 3 bugs in room 4
# state.unloadRoomsExcept(4)
# hookshot = state.allocActor(actors.Arms_Hook)
# state.loadRoom(7)
# state.unloadRoomsExcept(7)
# state.dealloc(hookshot.addr)
# -----------------------------------------

# Start the search using the current state and pray you find what you're looking for
# Fish addresses can be found here: 
# docs.google.com/spreadsheets/d/17BLPrpJRf7Vf01lYhXPKu1VumFAkxbGxyrww8ux5aZc/edit
# addresses = [0x801f94b0, 0x801f9fa0, 0x801fa7f0]
addresses = [0x801f9440] # Max Hearts, angle 0x9618
check     = LostWoods(state, addresses)
# ret       = state.search(check.fish8011xxxxRotWrite, blockedRooms=[0x9], peekRooms=[0x9], blockedActors=[], forceMagic=False, indefinite=False)
ret       = state.search(check.bushDraw, blockedRooms=[0x9], peekRooms=[0x9], blockedActors=[], forceMagic=False, indefinite=False)

# for node in state.heap():
#     print(node)

actorList = ActorList()
actorList.printSteps(ret[0][1])

# You can print out all found fish addresses if you'd like to
# print([hex(x) for x in sorted(check.info()["fish"])])