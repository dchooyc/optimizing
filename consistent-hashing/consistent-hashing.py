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
            hashed = hash(virtualId)
            assignedValue = hashed % 360
            self.assignedValues.append(assignedValue)
            self.assignedToServer[assignedValue] = len(self.servers) - 1

            if len(self.servers) > 0:
                predecessor = self.findServer(assignedValue)
                print(predecessor)
                migrationData = self.getMigrationData(self.servers[predecessor], assignedValue)
                self.addDataToServer(self.servers[len(self.servers) - 1], migrationData)        
        
        self.assignedValues.sort()
        print("These are the assignedValues")
        print(self.assignedValues)
        print("These are the assigned values to server")
        print(self.assignedToServer)
        

    def findServer(self, value):
        lo, hi = 0, len(self.assignedValues)

        while lo < hi:
            mid = lo + ((hi - lo) >> 1)

            if self.assignedValues[mid] < value:
                lo = mid + 1
            else:
                hi = mid
        
        assignedValue = self.assignedValues[lo % len(self.assignedValues)]
        
        return self.assignedToServer[assignedValue]
    

    def getMigrationData(self, server, target):
        mig = {}

        for key in server.data:
            hashed = hash(key)
            assignedValue = hashed % 360

            if assignedValue < target:
                mig[key] = server.data[key]
                del server.data[key]
        
        return mig
    

    def addDataToServer(self, server, data):
        for key in data:
            server.data[key] = data[key]



def main():
    servers = ["Singapore", "Australia", "France"]
    consistent_hashing = ConsistentHashing()

    for server in servers:
        consistent_hashing.addServer(server)
    
    return



main()


