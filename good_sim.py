import json

f=open('actors.json')
actorInfo = json.load(f)
f.close()

f=open('scenes.json')
sceneInfo = json.load(f)
f.close()

f=open('versions.json')
versionInfo = json.load(f)
f.close()

class GameState:
    def __init__(self, version):
        self.version = version
        self.heapStart = versionInfo[version]['heapStart']
        self.console = versionInfo[version]['console']
        self.game = versionInfo[version]['game']
        self.headerSize = 0x30 if self.console=='N64' else 0x10

    def loadScene(self, sceneId, setupId, roomId):
        if 'ALL' in sceneInfo[sceneId]:
            self.setupData = sceneInfo[sceneId]['ALL'][setupId]
        elif self.game in sceneInfo[sceneId]:
            self.setupData = sceneInfo[sceneId][self.game][setupId]
        else:
            self.setupData = sceneInfo[sceneId][self.version][setupId]

        self.actors = {}
            
        self.heap = HeapNode(self.heapStart, self.headerSize, 0x100000000-self.headerSize)
        self.allocActor(0x0000, 'ALL') # Link
        self.alloc(0x2010, 'Get Item Object')
        self.allocActor(0x0018, 'ALL') # Navi

        for transitionActor in self.setupData['transitionActors']:
            if transitionActor['frontRoom'] == roomId or transitionActor['backRoom'] == roomId:
                self.allocActor(transitionActor['actorId'], [transitionActor['frontRoom'],transitionActor['backRoom']])
                
        self.loadRoom(roomId)

    def loadRoom(self, roomId):
        for node in self.heap:
            if not node.free and node.rooms != 'ALL' and roomId not in node.rooms:
                self.dealloc(node)
            
        for actor in self.setupData['rooms'][roomId]['actors']:
            self.allocActor(actor['actorId'], [roomId])

    def allocActor(self, actorId, rooms):

        if actorId in self.actors:
            actor = self.actors[actorId]
        else:
            if 'ALL' in actorInfo[actorId]:
                actor = actorInfo[actorId]['ALL']
            elif self.console in actorInfo[actorId]:
                actor = actorInfo[actorId][self.console]
            else:
                actor = actorInfo[actorId][self.version]
            actor['numLoaded'] = 0
            self.actors[actorId] = actor

        if actor['numLoaded'] == 0 and actor['overlaySize'] and actor['allocType']==0:
            overlayNode = self.alloc(actor['overlaySize'], 'Code %04X %s'%(actorId,actor['name']))
            actor['loadedOverlay'] = overlayNode

        instanceNode = self.alloc(actor['instanceSize'], 'Actor %04X %s'%(actorId,actor['name']))
        instanceNode.rooms = rooms
        instanceNode.nodeType = 'INSTANCE'
        instanceNode.actorId = actorId

        actor['numLoaded'] += 1

    def alloc(self, allocSize, description):
        allocSize = allocSize + ((-allocSize)%0x10)
        for node in self.heap:
            if node.free and node.blockSize >= allocSize:
                if node.blockSize > allocSize + self.headerSize:
                    newNode = HeapNode(node.addr+self.headerSize+allocSize, self.headerSize, node.blockSize-allocSize-self.headerSize)
                    node.blockSize = allocSize
                    newNode.prevNode = node
                    newNode.nextNode = node.nextNode
                    if node.nextNode:
                        node.nextNode.prevNode = newNode
                    node.nextNode = newNode
                node.free = False
                node.description = description
                return node
        raise Exception('alloc should always succeed')

    def dealloc(self, node):
        assert not node.free
        assert node.nextNode
        
        if node.nextNode.free:
            node.blockSize += self.headerSize + node.nextNode.blockSize
            node.nextNode = node.nextNode.nextNode
            if node.nextNode:
                node.nextNode.prevNode = node
        if node.prevNode and node.prevNode.free:
            node.prevNode.blockSize += self.headerSize + node.blockSize
            node.prevNode.nextNode = node.nextNode
            if node.nextNode:
                node.nextNode.prevNode = node.prevNode

        if node.nodeType == 'INSTANCE':
            actor = self.actors[node.actorId]
            actor['numLoaded'] -= 1
            if actor['numLoaded'] == 0 and actor['overlaySize'] and actor['allocType']==0:
                self.dealloc(actor['loadedOverlay'])
                
        node.free = True
        node.description = 'Empty'
        node.rooms = 'ALL'
        node.nodeType = 'OTHER'
        node.actorId = None

    def __str__(self):
        return "\n".join((str(node) for node in self.heap))

class HeapNode:
    def __init__(self, addr, headerSize, blockSize):
        self.addr = addr
        self.headerSize = headerSize
        self.free = True
        self.blockSize = blockSize
        self.prevNode = None
        self.nextNode = None
        self.description = 'Empty'
        self.rooms = 'ALL'
        self.nodeType = 'OTHER'
        self.actorId = None

    def __iter__(self):
        current = self
        while current is not None:
            yield current
            current = current.nextNode

    def __str__(self):
        return "header:%08X data:%08X free:%d blocksize:%X next_addr:%08X prev_addr:%08X - %s"%(self.addr,self.addr+self.headerSize,self.free,self.blockSize, self.prevNode.addr if self.prevNode else 0, self.nextNode.addr if self.nextNode else 0, self.description)

gameState = GameState('N-1.0')
gameState.loadScene(sceneId=0x55, setupId=0, roomId=0)
gameState.loadRoom(1)
print(gameState)
