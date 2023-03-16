from random import randint

class Server:
    def __init__(self, id):
        self.id = id
        self.data = {}



class ConsistentHashing:
    # can set range of possible values with mod
    # can set number of virtual servers per server
    def __init__(self, mod = 3600, virtuals = 3):
        self.servers = []
        self.mod = mod
        self.virtuals = virtuals
        self.assignedValues = []
        self.assignedToServer = {}

    
    def displayServers(self):
        print("\n--- Displaying current servers ---")

        for server in self.servers:
            print("\n" + server.id)
            print(server.data)

    
    def displayServersUsage(self):
        print("\n--- Current servers usage ---")
        total = 0

        for server in self.servers:
            total += len(server.data)
            print("Data usage of " + server.id + ": " + str(len(server.data)))
        
        print("\nTotal data usage: " + str(total))


    def addServers(self, serverIds):
        for serverId in serverIds:
            self.addServer(serverId)
    

    def addServer(self, serverId):
        newServer = Server(serverId)
        self.servers.append(newServer)

        for v in range(1, self.virtuals + 1):
            extra = "." + str(v)
            assignedValue = self.getAssignedValue(serverId, extra)

            # this prevents duplicate assignedValues
            while assignedValue in self.assignedToServer:
                extra += "." + str(v)
                assignedValue = self.getAssignedValue(serverId, extra)

            self.assignedValues.append(assignedValue)
            self.assignedToServer[assignedValue] = len(self.servers) - 1

            # if there are servers, try to retrieve data from predecessor
            if len(self.servers) > 0:
                predecessor = self.findServer(assignedValue)
                migrationData = self.getMigrationData(self.servers[predecessor], assignedValue)
                self.addDataToServer(self.servers[len(self.servers) - 1], migrationData)        
        
        self.assignedValues.sort()


    def getAssignedValue(self, serverId, extra):
        virtualId = serverId + extra
        hashed = hash(virtualId)
        assignedValue = hashed % self.mod

        return assignedValue


    def scaleDown(self, count):
        for _ in range(count):
            if len(self.servers) == 3:
                print("Minimum number of servers is 3, no further scaledown allowed!!")
                break
            self.removeServer()


    def removeServer(self):
        server = self.servers.pop()
        serverIndex = len(self.servers)
        data = server.data

        removedAssignedValues = []

        for key in self.assignedToServer:
            if self.assignedToServer[key] == serverIndex:
                removedAssignedValues.append(key)
        
        for key in removedAssignedValues:
            del self.assignedToServer[key]
            index = self.findAssignedValue(key)
            self.assignedValues.pop(index)
        
        # repopulate data to the other servers
        self.addDataToServers(data)


    # finds index of assigned value
    def findAssignedValue(self, value):
        lo, hi = 0, len(self.assignedValues) - 1

        while lo < hi:
            mid = lo + ((hi - lo) >> 1)

            if self.assignedValues[mid] == value:
                return mid
            elif self.assignedValues[mid] < value:
                lo = mid + 1
            else:
                hi = mid - 1
        
        return lo
        

    # finds index of server object that value should be assigned to
    def findServer(self, value):
        lo, hi = 0, len(self.assignedValues)

        while lo < hi:
            mid = lo + ((hi - lo) >> 1)

            if self.assignedValues[mid] < value:
                lo = mid + 1
            else:
                hi = mid
        
        # ensures circular assignment
        assignedValue = self.assignedValues[lo % len(self.assignedValues)]
        
        return self.assignedToServer[assignedValue]
    

    # retrieves data to be migrated to successor
    def getMigrationData(self, server, target):
        mig, removedKeys = {}, []

        for key in server.data:
            hashed = hash(key)
            assignedValue = hashed % self.mod

            if assignedValue < target:
                mig[key] = server.data[key]
                removedKeys.append(key)
        
        for key in removedKeys:
            del server.data[key]
        
        return mig
    

    def addDataToServers(self, data):
        for key in data:
            hashed = hash(key)
            assignedValue = hashed % self.mod
            targetServer = self.findServer(assignedValue)
            self.addDataToServer(self.servers[targetServer], { key: data[key]})
    

    def addDataToServer(self, server, data):
        for key in data:
            server.data[key] = data[key]



class TestData:
    # randomly generate server ids
    def genServers(self, count):
        direction = ["North", "South", "East", "West"]
        countries = ["Singapore", "Australia", "France", "Canada", "China", "Chile", "Nepal", "Uruguay", "Cameroon"]

        servers = [""] * count

        for i in range(count):
            servers[i] = direction[randint(0,3)] + "-" + countries[randint(0,8)] + "-" + str(randint(1,9))

        return servers
    

    # randomly generate data key value pairs
    def genData(self, count):
        colors = [
            "red", "blue", "green", "yellow", "orange",
            "purple", "pink", "brown", "gray", "cyan"
        ]
        fruits = [
            "apple", "banana", "orange", "grape", "pineapple",
            "mango", "kiwi", "strawberry", "blueberry", "raspberry",
            "papaya", "watermelon", "cantaloupe", "peach", "nectarine",
            "plum", "apricot", "cherimoya", "pomegranate", "coconut"
        ]
        # abbreviations of famous fruit markets
        markets = [
            "LBQ", "PPM", "TOM", "CRM", "MDA",
            "BRM", "MSM", "MCF", "KAW", "SLM",
            "FPM", "RLM", "MCS", "MDL", "CTM",
            "QVM", "MLM", "CMA", "MDA", "OSH",
        ]

        data = {}

        for _ in range(count):
            data[markets[randint(0,19)] + "-" + str(randint(100_000,999_999))] = colors[randint(0,9)] + "-" + fruits[randint(0,19)]
        
        return data



def main():
    td = TestData()
    servers = td.genServers(3)
    consistent_hashing = ConsistentHashing()
    consistent_hashing.addServers(servers)
    data = td.genData(10)
    consistent_hashing.addDataToServers(data)


    # displays servers contents at first creation
    consistent_hashing.displayServers()


    # demonstrates data redistribution when adding new servers
    newServers = td.genServers(3)
    consistent_hashing.addServers(newServers)
    consistent_hashing.displayServers()


    # demonstrates new data is succesfully distributed to servers
    newData = td.genData(50)
    consistent_hashing.addDataToServers(newData)
    consistent_hashing.displayServers()


    # in general, when larger data sets are used, data distribution is rather even
    newData2 = td.genData(100_000)
    consistent_hashing.addDataToServers(newData2)
    consistent_hashing.displayServersUsage()


    # shows data is redistributed rather evenly during scale up
    newServers2 = td.genServers(6)
    consistent_hashing.addServers(newServers2)
    consistent_hashing.displayServersUsage()


    # shows scaledown and redistribution of data
    consistent_hashing.scaleDown(3)
    consistent_hashing.displayServersUsage()


    # shows scaledown stopping mechanism
    consistent_hashing.scaleDown(10)
    consistent_hashing.displayServersUsage()
    
    return



main()


