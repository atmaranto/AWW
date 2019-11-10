import pandas as pd
import xgboost
import sklearn
import pickle
import pandas as pd
import sys, math, csv, os
import numpy as np
import time

LAT_COLUMN = 19
LNG_COLUMN = 20

TEMP_COLUMN = 6
DEW_COLUMN = 7
HUMID_COLUMN = 8
WEATHER_COLUMN = 16
WIND_COLUMN = 10
closest = None
distance = 100000000

latitude = 32.9858
longitude = 96.7501
occupancy = 5
indoorTemp = 23.33
indoorHumid = 50.1
fanClass = 2
windowState = 0
currentCool = 23
currentHeat = -1.33
r = np.asarray([occupancy, indoorTemp, indoorHumid, 0.0, 0.0, fanClass, windowState, currentCool, currentHeat])
toReturn = [TEMP_COLUMN, DEW_COLUMN, HUMID_COLUMN, WIND_COLUMN]

np.random.seed(int(time.time() / 3600))
if(len(sys.argv) != 4):
    print("Missing params")
# Room temperature, Latitude, Longitude
else:
    latitude = float(sys.argv[3])
    longitude = float(sys.argv[2])
    temp = float(sys.argv[1])
    with open("Stations.csv", 'r') as stations:
        next(stations)
        for line in csv.reader(stations.readlines()):
	        lat, lng = (float(line[LAT_COLUMN])-latitude), (float(line[LNG_COLUMN])-longitude)
	        dist = math.sqrt(lat*lat + lng*lng)
	        if dist < distance:
		        distance = dist
		        closest = line
    save = False
    with open('MODIF_DATA.csv', 'r') as f:
        if not save:
            table = pd.read_csv(f, header=0)

            del table['Time']
            del table['Occupancy1']
            del table['Occupancy2']
            del table['IndoorAir']
            del table['OutdoorAir']
            del table['IndoorMean']
            del table['IndoorCO2']
            del table['Office']
            del table['Floor']
            del table['Location']
            del table['BaseThermoCool']
            del table['BaseThermoHeat']
            hasFan = table.loc[table['FanState'].notnull()]
            Y = hasFan.loc[:, table.columns == 'FanState']
            X = hasFan.loc[:, table.columns != 'FanState']
            #Occupancy, IndoorTemp, IndoorHumid, OutdoorTemp, OutdoorHumid, FanClass, WindowState, CurrentThermoCool, CurrentThermoHeat
            clf = xgboost.XGBClassifier(tree_method='gpu_hist', predictor='gpu_predictor', num_class=2, objective='binary_crossentropy', n_estimators=500, verbosity=2)
            with open('model', 'rb') as f:
                clf = pickle.load(f)
            input = np.repeat(r[:, np.newaxis], 7, axis=1)
            input = input.T
            outdoor = (float(closest[toReturn[2]]) - 32) / 1.8
            input[0, 3] = outdoor
            input[0, 4] = outdoor
            for i in range(1, 7):
                input[i, 3] = outdoor + np.random.random() * 2 - 2
                input[i, 4] = outdoor + np.random.random() * 2 - 2
            average = (temp + outdoor) / 2#abs(temp + float(closest[toReturn[0]])) / 2
            input[:, 7] = average
            input[:, 8] = average
            output = clf.predict(input)
            epochs = 0
            if(sum(output) > 0):
                while(sum(output) > 0 and epochs < 10):
                    variance = 1
                    for i in range(0, 7):
                        input[i, 7] = average * (np.random.random() * 2 - 2) * variance
                        input[i, 8] = average * (np.random.random() * 2 - 2) * variance
                        output = clf.predict(input)
                        variance += 1
                    epochs += 1
            out = ''
            for i in range(0, 7):
                out += str("%.2f" % (input[i, 7] + np.random.rand()) + ' ')
            print(out)
        else:
            table = pd.read_csv(f, header = 0)
            del table['Time']
            del table['Occupancy1']
            del table['Occupancy2']
            del table['IndoorAir']
            del table['OutdoorAir']
            del table['IndoorMean']
            del table['IndoorCO2']
            del table['Office']
            del table['Floor']
            del table['Location']
            del table['BaseThermoCool']
            del table['BaseThermoHeat']
            hasFan = table.loc[table['FanState'].notnull()]
            Y = hasFan.loc[:, hasFan.columns == 'FanState']
            X = hasFan.loc[:, hasFan.columns != 'FanState']
            X_train, X_test, Y_train, Y_test = sklearn.model_selection.train_test_split(X, Y, stratify=Y, train_size=0.8, random_state=1)
            clf = xgboost.XGBClassifier(tree_method='gpu_hist', predictor='gpu_predictor', num_class=2, objective='binary_crossentropy', n_estimators=2500, verbosity=2)
            clf.fit(X_train.values, Y_train.values)
            print(sklearn.metrics.classification_report(Y_test.values, clf.predict(X_test.values)))
            with open('model', 'wb') as f:
                pickle.dump(clf, f)
