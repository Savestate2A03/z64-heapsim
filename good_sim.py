import json
import copy

f=open('actors.json')
actorInfo = json.load(f)
f.close()

f=open('scenes.json')
sceneInfo = json.load(f)
f.close()

f=open('versions.json')
versionInfo = json.load(f)
f.close()

player_actor = 0x0000
En_Elf= 0x0018
En_Bom_Chu = 0x00DA
En_Fish = 0x0021
En_River_Sound = 0x003B
Object_Kankyo = 0x0097
En_Bom = 0x0010
En_Holl = 0x0023
En_Wonder_Item = 0x0112
En_Kusa = 0x125
En_Insect = 0x0020
En_Fish = 0x0021

class GameState:
    def __init__(self, game, version, startFlags):
        self.game = game
        self.version = version
        self.heapStart = versionInfo[version]['heapStart']
        self.console = versionInfo[version]['console']
        self.game = versionInfo[version]['game']
        self.headerSize = 0x30 if self.console=='N64' else 0x10
        self.flags = startFlags

    def loadScene(self, sceneId, setupId, roomId):
        if 'ALL' in sceneInfo[self.game][sceneId]:
            self.setupData = sceneInfo[self.game][sceneId]['ALL'][setupId]
        elif self.game in sceneInfo[self.game][sceneId]:
            self.setupData = sceneInfo[self.game][sceneId][self.game][setupId]
        else:
            self.setupData = sceneInfo[self.game][sceneId][self.version][setupId]

        self.actors = {}
        for actorId in range(len(actorInfo[self.game])):
            if 'ALL' in actorInfo[self.game][actorId]:
                actor = actorInfo[self.game][actorId]['ALL']
            elif self.console in actorInfo[self.game][actorId]:
                actor = actorInfo[self.game][actorId][self.console]
            else:
                actor = actorInfo[self.game][actorId][self.version]
            actor['numLoaded'] = 0
            self.actors[actorId] = actor

        self.ram = {}
        self.ram[self.heapStart] = HeapNode(self.heapStart, self.headerSize, 0x100000000-self.headerSize)
        
        self.allocActor(player_actor, 'ALL') # Link
        self.alloc(0x2010, 'Get Item Object')
        self.allocActor(En_Elf, 'ALL') # Navi

        self.loadedRooms = set()
        
        self.loadRoom(roomId)

    def heap(self):
        nodeAddr = self.heapStart
        while nodeAddr != 0:
            yield self.ram[nodeAddr]
            nodeAddr = self.ram[nodeAddr].nextNodeAddr

    def loadRoom(self, roomId):

        for transitionActor in self.setupData['transitionActors']:
            if (transitionActor['frontRoom'] == roomId or transitionActor['backRoom'] == roomId) and transitionActor['frontRoom'] not in self.loadedRooms and transitionActor['backRoom'] not in self.loadedRooms:
                self.allocActor(transitionActor['actorId'], [transitionActor['frontRoom'],transitionActor['backRoom']])

        loadedActors = []
            
        for actor in self.setupData['rooms'][roomId]['actors']:
            loadedActors.append(self.allocActor(actor['actorId'], [roomId], actor['actorParams']))

        for loadedActor in loadedActors:
            self.initFunction(loadedActor)

        self.loadedRooms.add(roomId)

    def unloadRoomsExcept(self, roomId):

        assert roomId in self.loadedRooms
        self.loadedRooms = set([roomId])
            
        for node in self.heap():
            if not node.free and node.rooms != 'ALL':
                for actorRoomId in node.rooms:
                    if actorRoomId in self.loadedRooms:
                        break
                else:
                    self.dealloc(node.addr)

    def allocActor(self, actorId, rooms='ALL', actorParams=0x0000):

        actor = self.actors[actorId]

        if actor['numLoaded'] == 0 and actor['overlaySize'] and actor['allocType']==0:
            overlayNode = self.alloc(actor['overlaySize'], 'Code %04X %s'%(actorId,actor['name']))
            actor['loadedOverlay'] = overlayNode.addr

        instanceNode = self.alloc(actor['instanceSize'], 'Actor %04X %s (%04X)'%(actorId,actor['name'],actorParams))
        instanceNode.rooms = rooms
        instanceNode.nodeType = 'INSTANCE'
        instanceNode.actorId = actorId
        instanceNode.actorParams = actorParams

        actor['numLoaded'] += 1

        return instanceNode

    def alloc(self, allocSize, description):
        allocSize = allocSize + ((-allocSize)%0x10)
        for node in self.heap():
            if node.free and node.blockSize >= allocSize:
                if node.blockSize > allocSize + self.headerSize:
                    newNode = HeapNode(node.addr+self.headerSize+allocSize, self.headerSize, node.blockSize-allocSize-self.headerSize)
                    self.ram[newNode.addr] = newNode
                    node.blockSize = allocSize
                    newNode.prevNodeAddr = node.addr
                    newNode.nextNodeAddr = node.nextNodeAddr
                    if node.nextNodeAddr:
                        self.ram[node.nextNodeAddr].prevNodeAddr = newNode.addr
                    node.nextNodeAddr = newNode.addr
                node.free = False
                node.description = description
                return node
        raise Exception('alloc should always succeed')

    def dealloc(self, nodeAddr):
        node = self.ram[nodeAddr]
        assert not node.free

        if node.nodeType == 'INSTANCE':
            actor = self.actors[node.actorId]
            actor['numLoaded'] -= 1
            if actor['numLoaded'] == 0 and actor['overlaySize'] and actor['allocType']==0:
                self.dealloc(actor['loadedOverlay'])
        
        if self.ram[node.nextNodeAddr].free:
            node.blockSize += self.headerSize + self.ram[node.nextNodeAddr].blockSize
            node.nextNodeAddr = self.ram[node.nextNodeAddr].nextNodeAddr
            if node.nextNodeAddr > 0:
                self.ram[node.nextNodeAddr].prevNodeAddr = node.addr
        if self.ram[node.prevNodeAddr].free:
            self.ram[node.prevNodeAddr].blockSize += self.headerSize + node.blockSize
            self.ram[node.prevNodeAddr].nextNodeAddr = node.nextNodeAddr
            if node.nextNodeAddr > 0:
                self.ram[node.nextNodeAddr].prevNodeAddr = node.prevNodeAddr
                
        node.reset()

    def initFunction(self, node): ### Incomplete -- need to add all behaviour here that matters for heap manip.

        if node.actorId == En_River_Sound and node.actorParams==0x000C and (not self.flags['lullaby'] or self.flags['saria']): # Proximity Saria's Song
            self.dealloc(node.addr)
            return None

        if node.actorId == Object_Kankyo:
            node.rooms = 'ALL'
            if self.actors[node.actorId]['numLoaded'] > 1:
                self.dealloc(node.addr)
                return None

        return node

    def getAvailableActions(self): ### Also incomplete.

        availableActions = []

        if len(self.loadedRooms) > 1:
            for room in self.loadedRooms:
                availableActions.append(['unloadRoomsExcept', room])
        
        if self.flags['bombchu'] and self.actors[En_Bom]['numLoaded'] + self.actors[En_Bom_Chu]['numLoaded'] < 3:
            availableActions.append(['allocActor', En_Bom_Chu])
        
        if self.flags['bomb'] and self.actors[En_Bom]['numLoaded'] + self.actors[En_Bom_Chu]['numLoaded'] < 3:
            availableActions.append(['allocActor', En_Bom])

        if self.flags['bottle']:
            availableActions.append(['allocActor', En_Insect])
            availableActions.append(['allocActor', En_Fish])

        for node in self.heap():
            if not node.free and node.nodeType=='INSTANCE':
                
                if node.rooms != 'ALL' and len(node.rooms) > 1 and len(self.loadedRooms) == 1: # This is a transition actor
                    for room in node.rooms:
                        if room not in self.loadedRooms:
                            availableActions.append(['loadRoom', room])

                if node.actorId in [En_Bom, En_Bom_Chu, En_Insect, En_Fish]:
                    availableActions.append(['dealloc', node.addr])

                if len(self.loadedRooms) == 1 and node.actorId in [En_Wonder_Item, En_Kusa]:
                    availableActions.append(['dealloc', node.addr])
            

        return availableActions

    def search(self, maxActionCount, successFunction, actionsAlreadyTaken=(), alreadySeenHeaps = {}):

        # Currently depth-first. TODO make breadth-first.

        selfHash = hash(str(self))

        if selfHash in alreadySeenHeaps and alreadySeenHeaps[selfHash] >= maxActionCount:
            return None

        alreadySeenHeaps[selfHash] = maxActionCount

        if successFunction(self):
            return self, actionsAlreadyTaken

        print(actionsAlreadyTaken)

        if maxActionCount < 1:
            return None
        
        for action in self.getAvailableActions():
            selfCopy = copy.deepcopy(self)
            func = getattr(selfCopy, action[0])
            func(*action[1:])
            searchResult = selfCopy.search(maxActionCount-1, successFunction, actionsAlreadyTaken+(action,), alreadySeenHeaps)
            if searchResult:
                return searchResult

        return None

    def __str__(self):
        return "\n".join((str(node) for node in self.heap()))

class HeapNode:
    def __init__(self, addr, headerSize, blockSize):
        self.addr = addr
        self.headerSize = headerSize
        self.blockSize = blockSize
        self.prevNodeAddr = 0
        self.nextNodeAddr = 0
        self.reset()

    def reset(self):
        self.free = True
        self.description = 'Empty'
        self.rooms = 'ALL'
        self.nodeType = 'OTHER'
        self.actorId = None
        self.actorParams = None

    def __str__(self):
        return "header:%08X data:%08X free:%d blocksize:%X next_addr:%X prev_addr:%X - %s"%(self.addr,self.addr+self.headerSize,self.free,self.blockSize, self.nextNodeAddr, self.prevNodeAddr, self.description)





fishAddresses = set()
def checkFishAddress(gameState):
    if 'loadedOverlay' not in gameState.actors[En_Fish]:
        gameState = copy.deepcopy(gameState)
        gameState.allocActor(En_Fish)
    fishAddresses.add(gameState.actors[En_Fish]['loadedOverlay'])
    return gameState.actors[En_Fish]['loadedOverlay'] == 0x801F9F30


gameState = GameState('OoT', 'OoT-N-1.2', {'lullaby':True, 'saria':True, 'bombchu':True, 'bomb':True, 'bottle':True})
gameState.loadScene(sceneId=0x5B, setupId=0, roomId=0)

#print(gameState.search(5, checkFishAddress))
#print([hex(x) for x in sorted(fishAddresses)])

bombchu = gameState.allocActor(En_Bom_Chu)
gameState.loadRoom(1)
print(gameState)
gameState.unloadRoomsExcept(1)
gameState.dealloc(bombchu.addr)
gameState.loadRoom(2)
gameState.allocActor(En_Fish)
print(gameState)
