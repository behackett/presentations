#!/usr/bin/python
#
# GeoIndexer for MongoDB Where2.0 Datasets
#
# Original script by:
# Brendan W. McAdams <bmcadams@evilmonkeylabs.com>
#
# Quick and dirty script which creates Geo Indices in MongoDB.
#
# Assumes you already loaded it with the provided shell script.
# 
# Needs PyMongo 1.6 or greater

import pymongo
from pymongo import Connection

connection = Connection()
db = connection['bart']
print "Indexing the Stops Data."
for row in db.stops.find():
    row['stop_geo'] = [row['stop_lon'], row['stop_lat']]
    db.stops.save(row)

db.stops.ensure_index([('stop_geo', pymongo.GEO2D)])
print "Reindexed stops with Geospatial data."

print "Indexing the Shapes data"
for row in db.shapes.find():
    row['shape_pt_geo'] = {'lon': row['shape_pt_lon'], 'lat': row['shape_pt_lat']}
    db.shapes.save(row)

db.shapes.ensure_index([('shape_pt_geo', pymongo.GEO2D)])
print "Reindexed shapes with Geospatial data."

db = connection['geo']
print "Indexing the Zips Data."
for row in db.zips.find():
    row['loc'] = [-(row['loc']['x']), row['loc']['y']]
    db.zips.save(row)

db.zips.ensure_index([('loc', pymongo.GEO2D)])
print "Reindexed zips with Geospatial data."

print "Done."
