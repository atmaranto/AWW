import sys, math, csv

if len(sys.argv) < 3:
	print("Usage: "+sys.argv[0]+" <lat> <lng>")
	print("--> yields nearest TEMPERATURE,DEW,HUMIDITY,WEATHER")
	sys.exit(1)

LAT_COLUMN = 20
LNG_COLUMN = 21

TEMP_COLUMN = 7
DEW_COLUMN = 8
HUMID_COLUMN = 9
WEATHER_COLUMN = 17

f = open("Stations.csv", "r")
closest = None
distance = 100000000

f.readline()

for line in csv.reader(f.readlines()):
	lat, lng = float(line[LAT_COLUMN]), float(line[LNG_COLUMN])
	dist = math.sqrt(lat*lat + lng*lng)
	if dist < distance:
		distance = dist
		closest = line

f.close()

toReturn = [TEMP_COLUMN, DEW_COLUMN, HUMID_COLUMN, WEATHER_COLUMN]

print(','.join([line[item] for item in toReturn]), end="")