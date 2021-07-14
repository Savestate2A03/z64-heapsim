from sim import GameState, actors
 
fishAddresses = set()
def checkFishAddress(gameState):
    if 'loadedOverlay' not in gameState.actors[En_Fish]:
        gameState = copy.deepcopy(gameState)
        gameState.allocActor(En_Fish)
    fishAddresses.add(gameState.actors[En_Fish]['loadedOverlay'])
    return gameState.actors[En_Fish]['loadedOverlay'] == 0x801F8F30
 
 
gameState = GameState('OoT', 'OoT-N-1.2', {'lullaby':True, 'saria':True, 'bombchu':True, 'bomb':True, 'bottle':True, 'clearedRooms':[], 'switchFlags': [0x11], 'beanPlanted':False})
gameState.loadScene(sceneId=0x5B, setupId=0, roomId=1)
 
#print(gameState.search(5, checkFishAddress))
#print([hex(x) for x in sorted(fishAddresses)])
 
# bombchu = gameState.allocActor(actors.En_Bom_Chu)
# gameState.loadRoom(1)
# print(gameState)
# print()
# gameState.unloadRoomsExcept(1)
# gameState.dealloc(bombchu.addr)
# gameState.loadRoom(2)
# gameState.allocActor(actors.En_Fish)
# print(gameState)
 
 
# bombchu = gameState.allocActor(actors.En_Bom_Chu)
# gameState.dealloc(bombchu.addr)
# 
# boomerang = gameState.allocActor(actors.En_Boom)
# gameState.dealloc(boomerang.addr)
# 
# dekuseed = gameState.allocActor(actors.En_Arrow)
# gameState.dealloc(dekuseed.addr)
# 
# thunder = gameState.allocActor(actors.En_M_Thunder)
# gameState.dealloc(thunder.addr)
# dust = gameState.allocActor(actors.Eff_Dust)
# gameState.dealloc(dust.addr)
 
# main heap manip
 
dekuseed = gameState.allocActor(actors.En_Arrow)
gameState.loadRoom(1)
gameState.dealloc(dekuseed.addr)
gameState.loadRoom(1)
gameState.loadRoom(1)
gameState.loadRoom(2)
gameState.unloadRoomsExcept(2)
gameState.loadRoom(1)
gameState.unloadRoomsExcept(1)
gameState.loadRoom(2)
 
# put fish overlay in memory
 
fish = gameState.allocActor(actors.En_Fish)
overlay_addr = gameState.actors[actors.En_Fish]['loadedOverlay']
print(fish)
print(f'0x801f8f30 == {hex(overlay_addr)} -> {overlay_addr == 0x801F8F30}, {hex(overlay_addr - 0x801f8f30)}')
gameState.dealloc(fish.addr)
 
# secondary heap manip for bush draw pointer srm
 
gameState.unloadRoomsExcept(1)
gameState.loadRoom(0)
gameState.unloadRoomsExcept(0)
gameState.loadRoom(1)
gameState.unloadRoomsExcept(1)
gameState.loadRoom(2)
gameState.unloadRoomsExcept(2)
 
En_Kusa_ID = 0x0125
kusas = [node for node in gameState.heap() if node.actorId == En_Kusa_ID]
print(":: Kusas before superslide ...")
print(f'En_Kusa 1 (Back Right) {hex(kusas[1].addr+kusas[1].headerSize)}, srm x rot2 {hex(kusas[1].addr+kusas[1].headerSize + 0xb4)}')
print(f'En_Kusa 2 (Front)      {hex(kusas[2].addr+kusas[2].headerSize)}, srm x rot2 {hex(kusas[2].addr+kusas[2].headerSize + 0xb4)}')
print(f'En_Kusa 0 (Back Left)  {hex(kusas[0].addr+kusas[0].headerSize)}, srm x rot2 {hex(kusas[0].addr+kusas[0].headerSize + 0xb4)}')
 
# srm bush
 
gameState.loadRoom(1)
gameState.unloadRoomsExcept(1)
gameState.loadRoom(2)
 
kusas2 = [node for node in gameState.heap() if node.actorId == En_Kusa_ID]
print(":: Kusas after SRM ...")
print(f'En_Kusa 1 (Back Right) {hex(kusas2[1].addr+kusas2[1].headerSize)}, draw pointer {hex(kusas2[1].addr+kusas2[1].headerSize + 0x134)}')
print(f'En_Kusa 2 (Front)      {hex(kusas2[2].addr+kusas2[2].headerSize)}, draw pointer {hex(kusas2[2].addr+kusas2[2].headerSize + 0x134)}')
print(f'En_Kusa 0 (Back Left)  {hex(kusas2[0].addr+kusas2[0].headerSize)}, draw pointer {hex(kusas2[0].addr+kusas2[0].headerSize + 0x134)}')
 
for kusa in kusas:
    for kusa2 in kusas2:
        if kusa.addr + kusa.headerSize + 0xb4 == kusa2.addr + kusa2.headerSize + 0x134:
            print('!!!!!!!!!!!!!!!!')
 
# check for draw pointer
