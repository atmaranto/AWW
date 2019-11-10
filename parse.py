import sys, math, csv, os

if len(sys.argv) < 3:
	print("Usage: "+sys.argv[0]+" <lat> <lng>")
	print("--> yields nearest TEMPERATURE,DEW,HUMIDITY")
	sys.exit(1)

if not os.path.isfile("Stations.csv"):
	print("Stations.csv not found in this directory")
	sys.exit(1)

LAT_COLUMN = 19
LNG_COLUMN = 20

TEMP_COLUMN = 6
DEW_COLUMN = 7
HUMID_COLUMN = 8
WEATHER_COLUMN = 16

f = open("Stations.csv", "r")
closest = None
distance = 100000000

latitude = float(sys.argv[1])
longitude = float(sys.argv[2])

f.readline()

for line in csv.reader(f.readlines()):
	lat, lng = (float(line[LAT_COLUMN])-latitude), (float(line[LNG_COLUMN])-longitude)
	dist = math.sqrt(lat*lat + lng*lng)
	
	if dist < distance:
		distance = dist
		closest = line

f.close()

toReturn = [TEMP_COLUMN, DEW_COLUMN, HUMID_COLUMN]

print(','.join([closest[item] for item in toReturn]), end="")