// Safe range of angles, others are smoothed.
let minAngle = 150;
let maxAngle = 170;
// Safe range of distances, points are removed or added to ensure.
let maxD = 10;
let minD = 5;

let points = [];
let done = false;


function setup() {
    var canvas = createCanvas(500, 500);
    // background(0, 0, 30);
    stroke(255, 255, 255);
    strokeWeight(5);
    angleMode(DEGREES);
    canvas.parent('canvas');
}


function draw() {
    if (done){
        background('rgba(0,0,0, 0.2)');
    } else {
        background('rgba(0,0,0, 0.2)');
    }
    done = true
    for(let i = 1; i < points.length; i++) {
        // Swap following two lines for line or point drawing
        line(points[i].x, points[i].y, points[i-1].x, points[i-1].y);
        // point(points[i].x, points[i].y);

        // reduceDist(i, maxD)
    }
    // Create safe range of angles, outside the range is smoothed
    reduceAngle(minAngle, maxAngle)
}


function mouseDragged() {
    if(-500 < mouseX && mouseX < 500)
    {
        points.push(createVector(mouseX, mouseY));
        send()
    }
}


// Reduces distance between points by inserting points along the line
function reduceDist(i, maxD) {
    let previous = points[i-1];
    let current = points[i];

    let d = dist(previous.x, previous.y, current.x, current.y);
    if(d >= maxD) {
        let numPoints = floor(d/maxD);
        // print(numPoints);
        for(j = numPoints-1; j > 0; j--){
            let travPercent = j/numPoints;
            let p = createVector((current.x-previous.x)*travPercent + previous.x,
                                 (current.y-previous.y)*travPercent + previous.y);
            points.splice(i, 0, p);
        }
    }
}


// Reduces angles between points to region between min and max
// Also removes points too close to each other
function reduceAngle(minAngle, maxAngle){
    for(let i = 2; i<points.length; i++){
        let prevprev = points[i-2];
        let previous = points[i-1];
        let current = points[i];
        ba = p5.Vector.sub(previous,prevprev);
        bc = p5.Vector.sub(previous,current);
        if(ba.angleBetween(bc) < minAngle || (maxAngle < ba.angleBetween(bc) && ba.angleBetween(bc) < 180)){
            let newPoint = previous;
            // b += 0.5*ba + 0.5*bc
            newPoint.add(ba.mult(-0.5)).add(bc.mult(-0.5));
            previous=newPoint;
        }
        if(ba.angleBetween(bc) < minAngle && i < points.length-3){
            done = false;
        }
        if(dist(previous.x, previous.y, prevprev.x, prevprev.y) < minD){
            points.splice(i-1, 1);
        }
    }
}


// Button is clicked to clear_canvas
function clear_canvas(){
    points = [];
}


// Send list of points
function send(){
    if (location.hostname === "localhost" || location.hostname === "127.0.0.1") {
        let listPoints = [];

        for(let i = 0; i<points.length; i++){
            let point = [];
            point.push(points[i].x);
            point.push(points[i].y);
            listPoints.push(point);
        }

        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({
            id: "abc",
            password: "qob",
            points: listPoints
        }));

        print("sent");
    }
}
