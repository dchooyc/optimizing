class Server:
    def __init__(self, id):
        self.id = id
        self.data = {}


class ConsistentHashing:
    def __init__(self, virtuals = 3):
        self.servers = []
        self.virtuals = virtuals
        self.assignedValues = []
        self.assignedToServer = {}
    
    def addServer(self, serverId):
        newServer = Server(serverId)
        self.servers.append(newServer)

        for v in range(1, self.virtuals + 1):
            virtualId = serverId + "." + str(v)
            assignedValue = hash(virtualId) % 360
            self.assignedValues.append(assignedValue)
            self.assignedToServer[assignedValue] = len(self.servers) - 1
        
        self.assignedValues.sort()
        print(self.servers)
        print(self.assignedValues)
        print(self.assignedToServer)


def main():
    servers = ["Singapore", "Australia", "France"]
    consistent_hashing = ConsistentHashing()

    for server in servers:
        consistent_hashing.addServer(server)
    
    return



main()


