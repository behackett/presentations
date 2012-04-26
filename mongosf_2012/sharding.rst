Sharding Notes
==============

Setting up a sharded cluster
----------------------------

Create directories for mongod instances::

  mkdir shard1 shard2 config

Start up 3 mongod instances::

  mongod(.exe) --dbpath /data/shard1 --port 10000 --shardsvr
  mongod(.exe) --dbpath /data/shard1 --port 10001 --shardsvr
  mongod(.exe) --dbpath /data/config --port 20000 --confgsvr

Start an instance of mongos::

  # --chunkSize 1 means use a 1MB chunk size. This is for
  # demonstration purposes.
  mongos --configdb localhost:20000 --chunkSize 1

Add shards to the cluster::

  mongo(.exe)
  mongos> use admin

  # Pre MongoDB 2.0
  mongos> db.runCommand({'addshard': 'localhost:10000'})
  mongos> db.runCommand({'addshard': 'localhost:10001'})

  # Post MongoDB 2.0
  mongos> sh.addShard('localhost:10000')
  mongos> sh.addShard('localhost:10001')

Enable sharding on a database::

  # Pre MongoDB 2.0
  mongos> db.runCommand({'enablesharding': <database name>})

  # Post MongoDB 2.0
  mongos> sh.enableSharding(<database name>)

Shard a collection::

  # Pre MongoDB 2.0
  mongos> db.runCommand({'shardcollection': <namespace>, 'key': <shard key>})

  # Post MongoDB 2.0
  mongos> sh.shardCollection(<namespace>, <shard key>)

Important Sharding Commands
---------------------------
::

  sh.help()
  db.printShardingStatus()

