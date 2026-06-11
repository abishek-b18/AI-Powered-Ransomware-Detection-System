// AI Ransomware Detection System

console.log("System Initialized");

// Threat Alert

function showAlert(){

alert(
"⚠️ Potential Ransomware Activity Detected!"
);

}

// Live Clock

function updateClock(){

let now = new Date();

document.getElementById("clock").innerHTML =
now.toLocaleString();

}

setInterval(updateClock,1000);