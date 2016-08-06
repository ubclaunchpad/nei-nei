var fs = require('fs');

// measured in radians
var ANGLE_THRESHOLD = 0.7;

// Removes points p(i), such that p(0) and p(n-1) always remain, and so that
// 1. Any 3 adjacent points p(i-1), p(i), p(i+1) have an angle between them greater
// than the ANGLE_THRESHOLD
// 2.
const trim = (hood) => {
	var name = hood.name;
	var points = hood.polygon.map(p => ({
		lat: Number(p.lat),
		lng: Number(p.lng)
	}));
	var newPoints = [];
	newPoints.push(points[0]);

	var currLine = getLine(points[0], points[1]);
	var nextLine = getLine(points[1], points[2]);
	for (var i = 1; i < points.length - 3; i++) {
		console.log('dist', findDistance(currLine.p1, nextLine.p2));
		if (isAngleOverThreshold(currLine, nextLine)) {
			newPoints.push(points[i]);
			currLine = nextLine;
		} else {
			currLine = getLine(currLine.p1, nextLine.p2);
		}
		nextLine = getLine(points[i + 1], points[i + 2]);
	}
	newPoints.push(points[points.length - 1]);
	return {
		name: name,
		polygon: newPoints
	};
}

// Puts points into a nice object
const getLine = (p1, p2) => ({
	p1: p1,
	p2: p2
});

const isAngleOverThreshold = (l1, l2) => {
	var angle = findAngle(l1.p1, l2.p1, l2.p2);
	console.log('angle', angle);
	return angle > ANGLE_THRESHOLD;
}

// p0 = point 0
// p1 = point 1
// c = centre
// returns angle in radians
const findAngle = (p0, p1, c) => {
	var p0c = Math.sqrt(Math.pow(c.lat-p0.lat,2) + Math.pow(c.lng-p0.lng,2));
	var p1c = Math.sqrt(Math.pow(c.lat-p1.lat,2) + Math.pow(c.lng-p1.lng,2));
	var p0p1 = Math.sqrt(Math.pow(p1.lat-p0.lat,2) + Math.pow(p1.lng-p0.lng,2));
	return Math.acos((p1c*p1c+p0c*p0c-p0p1*p0p1)/(2*p1c*p0c));
}

const M_PER_DEG = 111000;
const LNG_COEFFICIENT = Math.cos(49.246292);
const findDistance = (p0, p1) => {
	if (!p0 || !p1) return;
	return Math.sqrt(Math.pow(p0.lat-p1.lat, 2) + Math.pow((p0.lng-p1.lng)*LNG_COEFFICIENT, 2)) * M_PER_DEG;
}

// Begin processing
let hoods = JSON.parse(fs.readFileSync('./polygons.json'));

console.log('Initial');
hoods.forEach(h => console.log(h.name) || console.log(h.polygon.length));

hoods = hoods.map(h => trim(h));
console.log('After');
hoods.forEach(h => console.log(h.name) || console.log(h.polygon.length));
