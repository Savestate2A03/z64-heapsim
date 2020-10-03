from sim import GameState, actors

state = GameState('OoT', 'OoT-N-1.2', {'lullaby':True, 'saria':True, 'bombchu':True, 'bomb':True, 'bottle':True, 'clearedRooms':[], 'beanPlanted':False})

state.loadScene(sceneId=0x55, setupId=0, roomId=0)
print(list(state.heap())[-1])

state.changeRoom(1)
print(list(state.heap())[-1])

state.changeRoom(0)
print(list(state.heap())[-1])

state.changeRoom(1)
print(list(state.heap())[-1])

state.changeRoom(0)
print(list(state.heap())[-1])
