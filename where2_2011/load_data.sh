#!/bin/sh
#
# Quick & dirty script to load the BART Transit 
# Data to mongodb. Assumes mongod is running.
# 
# Data file is from: http://www.bart.gov/schedules/developers/gtfs.aspx 
# and freely available/redistributable.
# 
# Spec on the data format is available at: 
# http://code.google.com/transit/spec/transit_feed_specification.html
#
# Original script developed by Brendan W. McAdams

MONGO_IMPORT=/opt/mongo/bin/mongoimport
DOS2UNIX=
IMPORT_CMD="$MONGO_IMPORT -d bart --type csv --headerline --drop --ignoreBlanks"
BART_ZIP="google_transit.zip"
echo "Unzipping BART File ($BART_ZIP)"

unzip -o $BART_ZIP

# Agency is malformed in current file release... Fix it

# add the missing endline character.
echo '\n' >> agency.txt

echo "Loading Agency file..."
perl -pi -e 's/\r\n|\n|\r/\n/g' agency.txt
$IMPORT_CMD -c agency agency.txt
echo "Loading Stops file..."
perl -pi -e 's/\r\n|\n|\r/\n/g' stops.txt
$IMPORT_CMD -c stops stops.txt
echo "Loading Routes file..."
perl -pi -e 's/\r\n|\n|\r/\n/g' routes.txt
$IMPORT_CMD -c routes routes.txt
echo "Loading Trips file..."
perl -pi -e 's/\r\n|\n|\r/\n/g' trips.txt
$IMPORT_CMD -c trips trips.txt
echo "Loading Stop Times file..."
perl -pi -e 's/\r\n|\n|\r/\n/g' stop_times.txt
$IMPORT_CMD -c stop_times stop_times.txt
echo "Loading Calendar file..."
perl -pi -e 's/\r\n|\n|\r/\n/g' calendar.txt
$IMPORT_CMD -c calendar calendar.txt
echo "Loading Calendar Dates File..."
perl -pi -e 's/\r\n|\n|\r/\n/g' calendar_dates.txt
$IMPORT_CMD -c calendar_dates calendar_dates.txt
echo "Loading Shapes file..." # For line drawing - might be usable by GeoMongo
perl -pi -e 's/\r\n|\n|\r/\n/g' shapes.txt
$IMPORT_CMD -c shapes shapes.txt

echo "Loading zips.json to geo..."
$MONGO_IMPORT zips.json -d geo -c zips --drop
