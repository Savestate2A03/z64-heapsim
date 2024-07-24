# Zelda 64 Heap Simulator

This is a heap simulator for Ocarina of Time that supports multiple versions of the game. It uses a breadth-first search to iterate through all the possible actions Link can perform in a scene while using a user-defined success function to determine success or failure in the current iteration. It continues to search for a success indefinitely until one is found.

This simulator was created by [MrCheeze](https://github.com/MrCheeze/zelda64-heapsim) with heavy modification by myself.

## Important Files

There's a few key files in the simulator that you will want to be aware of---
| Filename       |Description                    |
|----------------|-------------------------------|
|`simulator_main.py`| Contains setup info for the simulator         |
|`address_checks.py`| Contains success functions that the simulator checks against the current state of the heap
|`sim/actors.py`|A list of actors and their ids, as well as `class ActorList` which can be used to return a string representing an actor given an actor id  |
|`sim/sim.py`|Main simulator logic, also contains the list of possible actions and the logic behind them|

All of these can be modified and tweaked according to your will if you so choose to do so.

## Usage

When using the simulator normally, there's a few steps of setup needed before you can run the simulator. You will need to do things like let it know if we have Saria's Song, what items are available to us (*ex: Bombchus, Hookshot*), among other things.

### `GameState` initialization

Before anything, we need to initialize an instance of `GameState`. It takes 3 arguments...

**`game`**
This will almost always be `"OoT"`

**`version`**
The following options are available for OoT version
| Version        |Description                    |
|----------------|-------------------------------|
`OoT-N-1.0`      | NTSC 1.0
`OoT-N-1.1`      | NTSC 1.1
`OoT-P-1.0`      | PAL 1.0
`OoT-N-1.2`      | NTSC 1.2
`OoT-P-1.1`      | PAL 1.1
`OoT-J-GC-MQDisc`| JP OoT on the MQ Disc
`OoT-J-MQ`       | JP Master Quest
`OoT-U-GC`       | JP OoT on the MQ Disc
`OoT-U-MQ`       | JP Master Quest
`OoT-P-GC`       | PAL OoT on the MQ Disc
`OoT-P-MQ`       | PAL Master Quest
`OoT-J-GC-CEDisc`| JP Collectors Edition
`OoT-iQue`       | iQue

**`startFlags`**
A list of flags passed into the simulator as a `dict`. If you write your own code in `sim/sim.py`, you can control how these flags affect actors' init functions in `initFunction()` and available actions in `getAvailableActions()` as an example. `currentRoomClear` lets the simulator know to not load any enemies in the provided rooms. `switchFlags` and `collectibleFlags` are used to deallocate actors on room load that match the provided flag numbers. Some flags are required for the simulator to work however; the below python code is recommended as a starting point.

```py
state = GameState('OoT', 'OoT-J-GC-MQDisc',
        {'lullaby':True, 'saria':True, 'bombchu':True,
         'bomb':True, 'bottle':True, 'hookshot':True,
         'clearedRooms':[], 'beanPlanted':False, 'switchFlags':[], 'collectibleFlags':[]})
```

### Scene Load

Once we have a `GameState` instance, we need to load a scene. `GameState` does this with `GameState.loadScene(scene, setup, roomId)`. 

`scene` will be the scene id. Currently only *Lost Woods* and *Goron City* have been tested, although others likely work, but might need some fenangling to be accurate. Easy access to these scene ids are provided in `scenes` in `simulator_main.py`.

`setup` (now known as 'overlay' in OoT development circles) determines which version of a scene to load. 
- 0x0 is Child Day
- 0x1 is Child Night 
_same as Child Day if no night overlay exists_
- 0x2 is Adult Day
- 0x3 is Adult Night

Further setups are used for cutscenes and generally will not be accessible.

`roomId` is which room to start out in in the simulator. Generally you'll need this to be a room that's connected to a loading zone so that it can actually be the first room loaded,

### Searching / Simulating

Once the above two things are setup, it's time to start searching. Our `GameState` instance has a search function we'll use to do so.
```py
GameState.search(successFunction, actorList, keepFishOverlay=False, carryingActor=False, blockedRooms=[], peekRooms=[], blockedActors=[], forceMagic=False, indefinite=False)
```
**`successFunction`** is the function that is used to determine if the current state of the heap matches the requirements as defined in the success function. Several of these are already defined in `address_checks.py` ready to use, for example `LostWoods.fish8011xxxxRotWrite`. Feel free to create your own however if you have a specific use case.

**`actorList`** is an instance of `ActorList` from `sim/actors.py`. The simulator uses it to pretty print successes after each one is found.

**`keepFishOverlay`** ensures a fish overlay is never unloaded. You probably will not use this, I made it when doing weird testing stuff a while back.

**`carryingActor`** tells the simulator to not add actions that require the use of Link's hands because you are telling it that he is currently holding something. Also probably something you will not use.

**`blockedRooms`** is a list of rooms that Link is not allowed to go into. Useful for helping direct the search in a particular direction.

**`peekRooms`** is a list of rooms that Link is allowed to step into, but not fully. This ignores `blockedRooms` so you can block Link from fully entering a room while allowing him to still load it if the room is a black-fade transition and not an instant room transition. Useful as well.

**`blockedActors`** is a list of actor ids that will be forced to not be used in the simulator. 

**`forceMagic`** forces (at the moment) spin attacks to load both `En_M_Thunder` and `Eff_Dust`.

**`indefinite`** lets the search continue even after the success function returns `True`.

## Pre-simulator Actions

Before you hand your `GameState` to the search simulator, you can manually add actions to create a customized starting point. Here's an example.
```py
# Starting from Room 0 in Lost Woods
state.loadRoom(1)
state.unloadRoomsExcept(1)
state.loadRoom(2)
state.unloadRoomsExcept(2)
state.loadRoom(3) # go into mido room ...
state.unloadRoomsExcept(3)
state.loadRoom(4) # both rooms 3 and 4 loaded
state.allocMultipleActorsWithRoom(actors.En_Insect, 3, 4) # load 3 bugs in room 4
state.unloadRoomsExcept(4)
hookshot = state.allocActor(actors.Arms_Hook)
state.loadRoom(7)
state.unloadRoomsExcept(7)
state.dealloc(hookshot.addr)
```
You can find all the actions you can take in `sim/sim.py`.

## Notes

This is a fairly complicated system but I tried my best to make it accessible to those who wish to use it.
