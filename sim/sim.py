import json
import copy
import os
from . import actors

dirname = os.path.dirname(__file__) + '/'
f=open(dirname+'/actors.json')
actorInfo = json.load(f)
f.close()

f=open(dirname+'/scenes.json')
sceneInfo = json.load(f)
f.close()

f=open(dirname+'/versions.json')
versionInfo = json.load(f)
f.close()

ACTORTYPE_ENEMY = 5

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
        self.sceneId = sceneId
        self.setupId = setupId
        
        self.loadedObjects = set([0x0001])
        if setupId not in [2,3]:
            self.loadedObjects.add(0x0015) # object_link_child
        if setupId not in [0,1]:
            self.loadedObjects.add(0x0014) # object_link_boy
        specialObject = self.setupData['specialObject']
        if specialObject != 0:
            self.loadedObjects.add(specialObject)

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
        
        self.allocActor(actors.Player, 'ALL') # Link
        self.alloc(0x2010, 'Get Item Object')
        self.allocActor(actors.En_Elf, 'ALL') # Navi

        self.loadedRooms = set()
        
        self.loadRoom(roomId)

    def heap(self):
        nodeAddr = self.heapStart
        while nodeAddr != 0:
            yield self.ram[nodeAddr]
            nodeAddr = self.ram[nodeAddr].nextNodeAddr

    def loadRoom(self, roomId, unloadOthersImmediately=False, forceToStayLoaded=[]):

        for transitionActor in self.setupData['transitionActors']:
            if (transitionActor['frontRoom'] == roomId or transitionActor['backRoom'] == roomId) and transitionActor['frontRoom'] not in self.loadedRooms and transitionActor['backRoom'] not in self.loadedRooms:
                self.allocActor(transitionActor['actorId'], [transitionActor['frontRoom'],transitionActor['backRoom']])

        currentRoomClear = False
        if roomId in self.flags['clearedRooms']:
            currentRoomClear = True

        for obj in self.setupData['rooms'][roomId]['objects']:
            self.loadedObjects.add(obj)

        actorsToInit = []
        actorsToUpdate = [[],[],[],[],[],[],[],[],[],[],[],[]] # separate by actor type
            
        for actor in self.setupData['rooms'][roomId]['actors']:
            actorId = actor['actorId']
            actorType = self.actors[actorId]['actorType']
            if actorType == ACTORTYPE_ENEMY and currentRoomClear:
                continue
            elif self.actors[actorId]['objectId'] not in self.loadedObjects:
                continue
            else:
                loadedActor = self.allocActor(actor['actorId'], [roomId], actor['actorParams'], actor['position'])
                actorsToInit.append(loadedActor)
                actorsToUpdate[actorType].append(loadedActor)

        for actorType in range(12):
            for loadedActor in actorsToInit:
                self.initFunction(loadedActor)

        self.loadedRooms.add(roomId)

        if unloadOthersImmediately:
            self.unloadRoomsExcept(roomId, forceToStayLoaded=forceToStayLoaded)

        for actorType in range(12):
            for loadedActor in actorsToUpdate[actorType]:
                if not loadedActor.free:
                    self.updateFunction(loadedActor)

    def unloadRoomsExcept(self, roomId, forceToStayLoaded=[]):

        assert roomId in self.loadedRooms
        self.loadedRooms = set([roomId])
            
        for node in self.heap():
            if not node.free and node.rooms != 'ALL':
                if node.addr in forceToStayLoaded:
                    node.rooms = 'FORCE_STAY_LOADED'
                    continue
                for actorRoomId in node.rooms:
                    if actorRoomId in self.loadedRooms:
                        break
                else:
                    self.dealloc(node.addr)

    def changeRoom(self, roomId, forceToStayLoaded=[]):
        self.loadRoom(roomId, unloadOthersImmediately=True, forceToStayLoaded=forceToStayLoaded)

    def allocActor(self, actorId, rooms='ALL', actorParams=0x0000, position=(0,0,0)):

        actor = self.actors[actorId]

        if actor['numLoaded'] == 0 and actor['overlaySize'] and actor['allocType']==0:
            overlayNode = self.alloc(actor['overlaySize'], 'Overlay %04X %s'%(actorId,actor['name']))
            actor['loadedOverlay'] = overlayNode.addr

        instanceNode = self.alloc(actor['instanceSize'], 'Actor %04X %s (%04X)'%(actorId,actor['name'],actorParams))
        instanceNode.rooms = rooms
        instanceNode.nodeType = 'INSTANCE'
        instanceNode.actorId = actorId
        instanceNode.actorParams = actorParams
        instanceNode.position = position

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

        if node.actorId == actors.En_River_Sound and node.actorParams==0x000C and (not self.flags['lullaby'] or self.flags['saria']): # Proximity Saria's Song
            self.dealloc(node.addr)

        elif node.actorId == actors.Object_Kankyo:
            node.rooms = 'ALL'
            if self.actors[node.actorId]['numLoaded'] > 1 and node.actorParams != 0x0004:
                self.dealloc(node.addr)

        elif node.actorId == actors.Door_Warp1 and node.actorParams == 0x0006:
            self.dealloc(node.addr)

        elif node.actorId == actors.Obj_Bean and self.setupId in [2,3] and not self.flags['beanPlanted']:
            self.dealloc(node.addr)

        elif node.actorId == actors.Bg_Spot02_Objects and self.setupId in [2,3] and node.actorParams == 0x0001:
            self.dealloc(node.addr)

        elif node.actorId == actors.En_Weather_Tag and node.actorParams == 0x1405:
            self.dealloc(node.addr)

        elif node.actorId == actors.En_Wonder_Item:
            wonderItemType = node.actorParams >> 0xB
            switchFlag = node.actorParams & 0x003F
            if wonderItemType == 1 or wonderItemType == 6 or wonderItemType > 9:
                self.dealloc(node.addr)
            elif switchFlag in self.flags['switchFlags']:
                self.dealloc(node.addr)

        elif node.actorId == actors.En_Owl and self.sceneId == 0x5B and (not self.flags['lullaby']):
            self.dealloc(node.addr)

        elif node.actorId in [actors.Obj_Bombiwa, actors.En_Wonder_Talk2]:
            switchFlag = node.actorParams & 0x003F
            if switchFlag in self.flags['switchFlags']:
                self.dealloc(node.addr)

        elif node.actorId == actors.En_Item00:
            collectibleFlag = (node.actorParams & 0x3F00) // 0x100
            if collectibleFlag in self.flags['collectibleFlags']:
                self.dealloc(node.addr)

    def updateFunction(self, node): ### Also incomplete -- This sim runs update on all actors just once after loading.

        if node.actorId in [actors.En_Ko, actors.En_Md, actors.En_Sa]:
            self.allocActor(actors.En_Elf, rooms=node.rooms)

    def getAvailableActions(self, carryingActor): ### Also incomplete.

        availableActions = []

        if len(self.loadedRooms) > 1:
            for room in self.loadedRooms:
                availableActions.append(['unloadRoomsExcept', room])

        if not carryingActor:
        
            if self.flags['bombchu'] and self.actors[actors.En_Bom]['numLoaded'] + self.actors[actors.En_Bom_Chu]['numLoaded'] < 3:
                availableActions.append(['allocActor', actors.En_Bom_Chu])
            
            if self.flags['bomb'] and self.actors[actors.En_Bom]['numLoaded'] + self.actors[actors.En_Bom_Chu]['numLoaded'] < 3:
                availableActions.append(['allocActor', actors.En_Bom])

            if self.flags['bottle']:
                availableActions.append(['allocActor', actors.En_Insect])
                availableActions.append(['allocActor', actors.En_Fish])

        for node in self.heap():
            if not node.free and node.nodeType=='INSTANCE':
                
                if node.rooms != 'ALL' and len(node.rooms) > 1 and len(self.loadedRooms) == 1: # This is a transition actor
                    for room in node.rooms:
                        if room not in self.loadedRooms:
                            availableActions.append(['loadRoom', room])

                if node.actorId in [actors.En_Bom, actors.En_Bom_Chu, actors.En_Insect, actors.En_Fish]:
                    availableActions.append(['dealloc', node.addr])

                if len(self.loadedRooms) == 1 and node.actorId in [actors.En_Wonder_Item]:
                    availableActions.append(['dealloc', node.addr])

                if len(self.loadedRooms) == 1 and node.actorId in [actors.En_Kusa] and not carryingActor:
                    availableActions.append(['dealloc', node.addr])
            

        return availableActions

    def search(self, maxActionCount, successFunction, actionsAlreadyTaken=(), alreadySeenHeaps = {}, carryingActor=False):

        # Currently depth-first. TODO make breadth-first.

        selfHash = hash(str(self))

        if selfHash in alreadySeenHeaps and alreadySeenHeaps[selfHash] >= maxActionCount:
            return None

        alreadySeenHeaps[selfHash] = maxActionCount

        if successFunction(self):
            return self, actionsAlreadyTaken

        #print(actionsAlreadyTaken)

        if maxActionCount < 1:
            return None
        
        for action in self.getAvailableActions(carryingActor):
            selfCopy = copy.deepcopy(self)
            func = getattr(selfCopy, action[0])
            func(*action[1:])
            searchResult = selfCopy.search(maxActionCount-1, successFunction, actionsAlreadyTaken+(action,), alreadySeenHeaps, carryingActor=carryingActor)
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





