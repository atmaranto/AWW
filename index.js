var express = require("express"),
	fs = require("fs"),
	bodyParser = require("body-parser"),
	parse = require("csv-parse"),
	http = require("http");

const LAT_COLUMN = 20,
	  LNG_COLUMN = 21,

	  TEMP_COLUMN = 7,
	  DEW_COLUMN = 8,
	  HUMID_COLUMN = 9,
	  WEATHER_COLUMN = 17;

var fileData = fs.readFileSync("index.html");
var dbCacheFile = fs.readFileSync("Stations.csv");

var exts = ["i.js", "style.css"];

var parser = parse(dbCacheFile, {
	delimiter: ","
});

var dbCache = [];

parser.on("readable", () => {
	parser.read();
	var record;
	
	while(record = parser.read()) {
		dbCache.push(record);
	}
});

parser.end();

var findClosest = (latitude, longitude) => {
	var closest = null;
	var distance = 1000000;
	
	var dist, line, lat, lng;
	
	for(line in dbCache) {
		lat = parseFloat(line[LAT_COLUMN]);
		lng = parseFloat(line[LNG_COLUMN]);
		
		dist = Math.sqrt(lat*lat + lng*lng);
		if(dist < distance) {
			distance = dist;
			closest = line;
		}
	}
	
	if(!closest) {
		return null;
	}
	
	return {
		temperature: parseFloat(line[TEMP_COLUMN]), dew: parseFloat(line[DEW_COLUMN]),
		humidity: parseFloat(line[HUMID_COLUMN]), weather: line[WEATHER_COLUMN]
	};
};

var app = express();

var server = http.createServer(app);

app.use(bodyParser.json());

app.get("/", (req, res) => {
	res.set("Content-Type", "text/html");
	res.set("Content-Disposition", "inline");
	
	return res.status(200).send(fileData); //Lol
});

exts.forEach((ext) => {
	app.get("/"+ext, (req, res) => {
		res.set("Content-Type", "text/html");
		res.set("Content-Disposition", "inline");
		
		fs.readFile(ext, (data) => {
			return res.status(200).send(data);
		});
	});
});

app.post("/temp", (req, res) => {
	if(typeof req.body.latitude != "number" || typeof req.body.longitude != "number") {
		return req.status(400).send("latitude and longitude must both be specified.");
	}
	
	return res.status(200).json(findClosest(req.body.latitude, req.body.longitude));
});

server.listen(400);