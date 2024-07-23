from sim import GameState, actors

state = GameState('OoT', 'OoT-N-1.2', {'lullaby':True, 'saria':True, 'bombchu':True, 'bomb':True, 'bottle':True, 'clearedRooms':[], 'beanPlanted':False})
state.loadScene(sceneId=0x58, setupId=0, roomId=1)
state.dealloc(0x801F54B0)
state.dealloc(0x801F5670)
state.dealloc(0x801F52F0)
thunder = state.allocActor(actors.En_M_Thunder)
fishes = []
for _ in range(5):
    fishes.append(state.allocActor(actors.En_Fish))
state.dealloc(thunder.addr)
kanbans = []
for _ in range(6):
    kanbans.append(state.allocActor(actors.En_Kanban))
               
for fish in fishes:
    state.dealloc(fish.addr)

bombchu = state.allocActor(actors.En_Bom_Chu)

for _ in range(5):
    fishes.append(state.allocActor(actors.En_Fish))

state.dealloc(bombchu.addr)
for kanban in kanbans:
    state.dealloc(kanban.addr)

print(state)
