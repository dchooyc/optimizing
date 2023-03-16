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
                migrationData = self.getMigrationData(self.servers[predecessor], assignedValue)
                self.addDataToServer(self.servers[len(self.servers) - 1], migrationData)        
        
        self.assignedValues.sort()
        

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
        mig, removedKeys = {}, []

        for key in server.data:
            hashed = hash(key)
            assignedValue = hashed % 360

            if assignedValue < target:
                mig[key] = server.data[key]
                removedKeys.append(key)
        
        for key in removedKeys:
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
    
    data = ({"Fruit1": "Apple", "Fruit2": "Pear",
             "Fruit3": "Orange", "Fruit4": "Pineapple",
             "Fruit5": "Wintermelon", "Fruit6": "Starfruit",
             "Fruit7": "Banana", "Fruit8": "Grape",
             "Fruit9": "Strawberry", "Fruit10": "Peach",
             "Fruit11": "Orange", "Fruit12": "Pineapple",
             "Fruit13": "Wintermelon", "Fruit14": "Starfruit",
             "Fruit15": "Banana", "Fruit16": "Grape",
             "Fruit17": "Strawberry", "Fruit18": "Peach",
             "Fruit19": "Orange", "Fruit20": "Pineapple"
             })
    
    for key in data:
        hashed = hash(key)
        assignedValue = hashed % 360
        targetServer = consistent_hashing.findServer(assignedValue)
        consistent_hashing.addDataToServer(consistent_hashing.servers[targetServer], { key: data[key]})

    print("\n--- Displaying original set of servers ---")

    for server in consistent_hashing.servers:
        print("\n" + server.id)
        print(server.data)

    newServers = ["Canada", "China", "Chile"]

    for server in newServers:
        consistent_hashing.addServer(server)

    print("\n--- Displaying servers after adding more servers ---")

    for server in consistent_hashing.servers:
        print("\n" + server.id)
        print(server.data)

    newData = ({"Fruit21": "Wintermelon", "Fruit22": "Starfruit",
                "Fruit23": "Banana", "Fruit24": "Grape",
                "Fruit25": "Strawberry", "Fruit26": "Peach",
                "Fruit27": "Orange", "Fruit28": "Pineapple",
                "Fruit29": "Wintermelon", "Fruit30": "Starfruit",
                "Fruit31": "Banana", "Fruit32": "Grape",
                "Fruit33": "Strawberry", "Fruit34": "Peach",
                "Fruit35": "Orange", "Fruit36": "Pineapple",
                "Fruit37": "Wintermelon", "Fruit38": "Starfruit",
                "Fruit39": "Banana", "Fruit40": "Grape",
                "Fruit41": "Strawberry", "Fruit42": "Peach"})
    
    for key in newData:
        hashed = hash(key)
        assignedValue = hashed % 360
        targetServer = consistent_hashing.findServer(assignedValue)
        consistent_hashing.addDataToServer(consistent_hashing.servers[targetServer], { key: newData[key]})

    print("\n--- Displaying servers after adding more data ---")

    for server in consistent_hashing.servers:
        print("\n" + server.id)
        print(server.data)
    
    return



main()


