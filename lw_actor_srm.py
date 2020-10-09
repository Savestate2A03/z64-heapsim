from sim import GameState, actors
import copy

gameState = GameState('OoT', 'OoT-N-1.2', {'lullaby':True, 'saria':True, 'bombchu':True, 'bomb':True, 'bottle':True, 'clearedRooms':[], 'beanPlanted':False})
gameState.loadScene(sceneId=0x5B, setupId=0, roomId=6)

for i in range(0x01D7):
    gameState.allocActor(i)

print(gameState)
