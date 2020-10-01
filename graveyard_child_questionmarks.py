from sim import GameState, actors

state = GameState('OoT', 'OoT-N-1.2', {'lullaby':True, 'saria':True, 'bombchu':True, 'bomb':True, 'bottle':True, 'clearedRooms':[], 'beanPlanted':False})
state.loadScene(sceneId=0x53, setupId=0, roomId=1)

print(state)

for i in range(20):

    print(list(state.heap())[-1])

    forceToStayLoaded = []
    for node in state.heap():
        if node.actorId in [actors.Obj_Kibako2, actors.Bg_Mjin, actors.En_Gs]:
            forceToStayLoaded.append(node.addr)
        if node.actorId == actors.En_Poh and node.position[0] == 552:
            forceToStayLoaded.append(node.addr)


    state.changeRoom(0,forceToStayLoaded)
    #print(list(state.heap())[-1])
    state.changeRoom(1)

#print(state)

