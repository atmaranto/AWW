import pandas as pd
import xgboost
import sklearn
import pickle
import pandas as pd
import sys, math, csv, os

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
toReturn = [TEMP_COLUMN, DEW_COLUMN, HUMID_COLUMN, WIND_COLUMN]

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
            #print(X.describe())
            clf = xgboost.XGBClassifier(tree_method='gpu_hist', predictor='gpu_predictor', num_class=2, objective='binary_crossentropy', n_estimators=500, verbosity=2)
            with open('model', 'rb') as f:
                clf = pickle.load(f)
            #clf.load_model('modified.model')
            #print(X.values[0])
            output = clf.predict(X.values[0:7])
            out = ''
            for i in output:
                out += str(i) + ' '
            print(out)
        else:
            table = pd.read_csv(f, names=['Time', 'Occupancy', 'Occupancy1', 'Occupancy2', 'IndoorTemp', 'IndoorHumid', 'IndoorAir', 'IndoorMean', 'IndoorCO2', 'OutdoorTemp', 'OutdoorHumid', 'OutdoorAir', 'Office', 'Floor', 'Location', 'FanClass', 'FanState', 'WindowState', 'CurrentThermoCool', 'BaseThermoCool', 'CurrentThermoHeat', 'BaseThermoHeat'])
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
            X_train, X_test, Y_train, Y_test = sklearn.model_selection.train_test_split(X, Y, stratify=Y, train_size=0.8, random_state=1)
            clf = xgboost.XGBClassifier(tree_method='gpu_hist', predictor='gpu_predictor', num_class=2, objective='binary_crossentropy', n_estimators=500, verbosity=2)
            clf.fit(X_train.values, Y_train.values)
            print(sklearn.metrics.classification_report(Y_test.values, clf.predict(X_test.values)))
            with open('model', 'wb') as f:
                pickle.dump(clf, f)