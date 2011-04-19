# Simple examples of doing various Geo queries using pymongo.
#
# Created for Where2.0 2011 Working with Geo data in MongoDB.
# Bernie Hackett <bernie@10gen.com>
#
import math

import bson
import pymongo

# Approximate radius of Earth according to Google calculator
RADIUS_MILES = 3963
# Very rough scale multiplier for distance on Earth.
# For standard $near queries. Spherical queries just use radius.
DISTANCE_MULTIPLIER = RADIUS_MILES * (math.pi / 180)

# Connect to mongod
connection = pymongo.Connection()

# Some examples require a newer mongod versions...
version_string = (connection.server_info()['version'])[:3]
version = tuple([int(num) for num in version_string.split('.')])

def bart_foreign_cinema(num_stops=1):
    """Find the BART station(s) closest to the Foreign Cinema
    in San Francisco.

    :Parameters:
        - `num_stops`: How many stations to list.
    """
    db = connection.bart
    cursor = db.stops.find(
            {'stop_geo': {'$near': [-122.419088, 37.75689]}}).limit(num_stops)
    for doc in cursor:
        print doc['stop_name']

# Using geoNear we can get an approximte or spherical
# distance and scale it to our needs
def bart_foreign_cinema_geonear(spherical=False):
    """How far away is the closest BART station to the
    Foreign Cinema in San Francisco.

    :Parameters:
        - `spherical`: Should we do a spherical query?
    """
    db = connection.bart
    if spherical:
        mult = RADIUS_MILES
    else:
        mult = DISTANCE_MULTIPLIER
    q = bson.son.SON({'geoNear': 'stops'})
    q.update({'near': [-122.419088, 37.75689]})
    q.update({'distanceMultiplier': mult})
    if spherical:
        q.update({'spherical': True})
    results = db.command(q)
    name = results['results'][0]['obj']['stop_name']
    dist = results['results'][0]['dis']
    print "Distance to %s: %r miles" % (name, dist)

map_func = "function(){ emit(this.state, this.pop); }"
reduce_func = "function(key, values){ return Array.sum(values); }"

# Calculate the entire population of the zipcode dataset.
# Inline map reduce just returns the result set instead
# of storing it in the database.
def calculate_population():
    """Use inline map reduce to calculate the entire
    population from the zips dataset.
    """
    if version < (1, 8):
        print "inline map reduce requires mongod >= 1.8"
    db = connection.geo
    print sum([res['value']
              for res
              in db.zips.inline_map_reduce(map_func, reduce_func)])

# How many people live within 100 miles of the
# Empire State Building (based on our dataset)?

range_in_miles = 100.0
max_distance = range_in_miles / DISTANCE_MULTIPLIER
nearq = bson.son.SON({'$near': [-73.985656, 40.748433]})
nearq.update({'$maxDistance': max_distance})
# Standard $near queries are limited to a result set of 100 documents.
# We use $within to get around that limitation.
withinq = {'$within': {'$center': [[-73.985656, 40.748433], max_distance]}}

def empire_state_find():
    """How many people live within 100 miles of the Empire State Building
    (according to our dataset). This calculates the answer twice. Once
    with $within, once with $near.
    """
    db = connection.geo
    # We only really care about the 'pop' field in the result documents.
    # The second parameter of find() tells mongod what fields to return
    # to us. MongoDB always returns '_id' unless you tell it not to.
    cursor = db.zips.find({'loc': withinq}, {'pop': True, '_id': False})
    print '$within: %d' % (sum([doc['pop'] for doc in cursor]),)
    cursor = db.zips.find({'loc': nearq},
                          {'pop': True, '_id': False}).limit(60000)
    print '$near: %d' % (sum([doc['pop'] for doc in cursor]),)

def empire_state_spherical():
    """How many people live within 100 miles of the Empire State Building
    (according to our dataset). This calculates the answer using $nearSphere
    so the distance calulation should be accurate.
    """
    db = connection.geo
    q = bson.son.SON({'$nearSphere': [-73.985656, 40.748433]})
    q.update({'$maxDistance': 100.0 / 3963})
    cursor = db.zips.find({'loc': q}).limit(60000)
    print '$nearSphere: %d' % (sum([doc['pop'] for doc in cursor]),)

# Using map/reduce or group with GEO queries requires MongoDB 1.9.
# ----------------------------------------------------------------------------
# Same result using map/reduce.
def empire_state_map_reduce():
    """Same $within query from above using map/reduce.
    """
    if version < (1, 9):
        print "map/reduce with geo requires mongod >= 1.9"
    else:
        db = connection.geo
        result = db.zips.inline_map_reduce(map_func,
                                           reduce_func,
                                           query={'loc': withinq})
        print sum([doc['value'] for doc in result])

# Same result using group.
def empire_state_group():
    """Same $within query again using group.
    """
    if version < (1, 9):
        print "group with geo requires mongod >= 1.9"
    else:
        db = connection.geo
        pop_reduce = "function(obj, prev){ prev.sum += obj.pop; }"
        result = db.zips.group(['state'], {'loc': withinq}, {'sum': 0}, pop_reduce)
        print sum([doc['sum'] for doc in result])
# ----------------------------------------------------------------------------

