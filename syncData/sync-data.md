# Two ways to sync data across a distributed system

## Multi-master replication
One have, all have.

Put simply whenever there is write operation to one server, the same write operation will be replicated to all the other servers.

![mmr-overview](images/mmr-overview.png)

When there is a read operation performed, it will be done on the server that is nearest to where the read operation is called.

One possible risk is that there may be conflicting data write operations. For example if one server is writing to the same entry as another server.

One way to prevent conflicting data write operations is to lock the object that is being written to. This means that when one server is writing to one entry, all other servers cannot write to that entry. So before the write operation is done, a lock operation is performed first. When the write operation is completed, the object is unlocked and other servers can write to that entry.

![mmr-locking](images/mmr-locking.png)

The benefit of using this method to sync data read and write is that if one server fails, the data is still available in all other servers.

One problem with using this method is that scale up is slow. This is because when adding a new server, it has to completely copy all previous data from the other servers.

Another problem with this method is that because the write operation is done to all servers, it may slow the system down as each server has to do every write operation in the system.


## Consistent hashing
Each have own.