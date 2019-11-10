var express = require("express"),
	fs = require("fs"),
	parse = require("csv-parse"),
	http = require("http"),
	child_process = require("child_process");

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

var app = express();

var server = http.createServer(app);

app.get("/", (req, res) => {
	res.set("Content-Type", "text/html");
	res.set("Content-Disposition", "inline");
	
	return res.status(200).send(fileData); //Lol
});

app.get("/check", (req, res) => {
	var proc = child_process.execFile("/usr/local/bin/python3", ["hackutd2019.py", req.query.temperature, req.query.latitude, req.query.longitude]);
	proc.stdout.on("data", (data) => {
		res.status(200).send(data.replace(/\n/g, ""));
	});
	proc.stderr.on("data", (data) => {
		res.status(500).send(data);
		console.log(data);
	});
});

server.listen(process.env.PORT || 31418);