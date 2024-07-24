
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

When using the simulator normally, there's a few steps of setup needed before you can run the simulator. You will need to do initialize the `GameState`, do things like let it know if we have _Saria's Song_, what items are available to us (*ex: Bombchus, Hookshot*), what scene and room to start on, among other things.

### GameState initialization

Before anything, we need to initialize an instance of `GameState` with 3 arguments.

| Argument | Description |
|--|---|
| **`game`** | This will almost always be `"OoT"` |
| **`version`** | The following options are available for OoT version <table class="table table-striped table-bordered"><thead><tr><th>Version</th><th>Description</th></tr></thead><tbody><tr><td><code>OoT-N-1.0</code></td><td>NTSC 1.0</td></tr><tr><td><code>OoT-N-1.1</code></td><td>NTSC 1.1</td></tr><tr><td><code>OoT-P-1.0</code></td><td>PAL 1.0</td></tr><tr><td><code>OoT-N-1.2</code></td><td>NTSC 1.2</td></tr><tr><td><code>OoT-P-1.1</code></td><td>PAL 1.1</td></tr><tr><td><code>OoT-J-GC-MQDisc</code></td><td>JP OoT on the MQ Disc</td></tr><tr><td><code>OoT-J-MQ</code></td><td>JP Master Quest</td></tr><tr><td><code>OoT-U-GC</code></td><td>JP OoT on the MQ Disc</td></tr><tr><td><code>OoT-U-MQ</code></td><td>JP Master Quest</td></tr><tr><td><code>OoT-P-GC</code></td><td>PAL OoT on the MQ Disc</td></tr><tr><td><code>OoT-P-MQ</code></td><td>PAL Master Quest</td></tr><tr><td><code>OoT-J-GC-CEDisc</code></td><td>JP Collectors Edition</td></tr><tr><td><code>OoT-iQue</code></td><td>iQue</td></tr></tbody></table>
| **`startFlags`** | A list of flags passed into the simulator as a `dict`. If you write your own code in `sim/sim.py`, you can control how these flags affect actors' init functions in `initFunction()` and available actions in `getAvailableActions()` as an example. <table><thead><tr><th>Flag</th><th>Description</th></tr></thead><tbody><tr><td><strong><code>lullaby</code></strong></td><td>Boolean for having Zelda’s Lullaby</td></tr><tr><td><strong><code>saria</code></strong></td><td>Boolean for having Saria’s Song</td></tr><tr><td><strong><code>bombchu</code></strong></td><td>Boolean for having Bombchus</td></tr><tr><td><strong><code>bomb</code></strong></td><td>Boolean for having Bombs</td></tr><tr><td><strong><code>bottle</code></strong></td><td>Boolean for having Bottle. Enables both Fish and Bugs as droppable contents.</td></tr><tr><td><strong><code>hookshot</code></strong></td><td>Boolean for having Hookshot</td></tr><tr><td><strong><code>clearedRooms[]</code></strong></td><td>Lets the simulator know to not load any enemies in the provided room numbers</td></tr><tr><td><strong><code>beanPlanted</code></strong></td><td>Boolean for if beans are planted in patches in the scene</td></tr><tr><td><strong><code>switchFlags[]</code></strong></td><td>Deallocate actors on room load that match the provided switch flags</td></tr><tr><td><strong><code>collectibleFlags[]</code></strong></td><td>Deallocate actors on room load that match the provided collectible flags</td></tr></tbody></table> 

Some **`startFlags`** are required for the simulator to work for certain checks and available actions; the below python code is recommended as a starting point.

```py
state = GameState('OoT', 'OoT-N-1.2',
        {'lullaby':True, 'saria':True, 'bombchu':True,
         'bomb':True, 'bottle':True, 'hookshot':True,
         'clearedRooms':[], 'beanPlanted':False, 'switchFlags':[], 'collectibleFlags':[]})
```

### Scene Load

Once we have a `GameState` instance, we need to load a scene. We do this with `GameState.loadScene(scene, setup, roomId)`. 

| GameState Argument | Description |
| ------------------ | ----------- |
| `scene` | The scene id to load. Currently only *Lost Woods* and *Goron City* have been tested, although others likely work, but might need some fenangling to be accurate. Easy access to these scene ids are provided in `scenes` in `simulator_main.py`. |
| `setup` | Determines which version of a scene to load. Now known as 'overlay' in OoT development circles. <table><thead><tr><th>Setup</th><th>Description</th></tr></thead><tbody><tr><td>0x0</td><td>Child Day</td></tr><tr><td>0x1</td><td>Child Night <em>(same as Child Day if no night overlay exists)</em></td></tr><tr><td>0x2</td><td>Adult Day</td></tr><tr><td>0x3</td><td>Adult Night <em>(same as Adult Day if no night overlay exists)</em></td></tr></tbody></table> Further setups are used for cutscenes and generally will not be accessible. |
| `roomId` | Which room to start out in in the simulator. Generally you'll need this to be a room that's connected to a loading zone so that it can actually be the first room loaded.

### Searching / Simulating

Once the above two things are setup, it's time to start searching. Our `GameState` instance has a search function we'll use to do so.
```py
GameState.search(successFunction, actorList, keepFishOverlay=False, carryingActor=False, blockedRooms=[], peekRooms=[], blockedActors=[], forceMagic=False, indefinite=False)
```
| Search Argument | Description |
| --------------- | ----------- |
| **`successFunction`** | The function that is used to determine if the current state of the heap matches the requirements as defined in the success function. Several of these are already defined in `address_checks.py` ready to use, for example `LostWoods.fish8011xxxxRotWrite`. Feel free to create your own however if you have a specific use case.
| **`actorList`** | An instance of `ActorList` from `sim/actors.py`. The simulator uses it to pretty print successes after each one is found.
| **`keepFishOverlay`** | Ensures a fish overlay is never unloaded. You probably will not use this, I made it when doing weird testing stuff a while back.
| **`carryingActor`** | Tells the simulator to not add actions that require the use of Link's hands because you are telling it that he is currently holding something. Also probably something you will not use.
| **`blockedRooms`** | A list of rooms that Link is not allowed to go into. Useful for helping direct the search in a particular direction.
| **`peekRooms`** | A list of rooms that Link is allowed to step into, but not fully. This ignores `blockedRooms` so you can block Link from fully entering a room while allowing him to still load it if the room is a black-fade transition and not an instant room transition. Useful as well.
| **`blockedActors`** | A list of actor ids that will be forced to not be used in the simulator. 
| **`forceMagic`** | Forces (at the moment) spin attacks to load both `En_M_Thunder` and `Eff_Dust`.
| **`indefinite`** | Lets the search continue even after the success function returns `True`.

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
