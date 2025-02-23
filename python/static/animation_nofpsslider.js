const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const boxSize = 30;  // Match Python simulation size
const N = 600;  // Number of particles
let FPS = 10;  // Frames per second

canvas.width = 500;
canvas.height = 500;

let stepsPerDay = 5;
let daysPerSec = 6;

let infectionRadius;
let infectionProb;
let infectiousPeriodDay;

// For cumulative chart data
let timeLabels = [0];  // Stores the days elapsed
let susData = [N-1];  // Stores the number of susceptible people
let infData = [1];  // Stores the number of infected people
let remData = [0];  // Stores the number of removed people

// Initialize Chart.js chart variable
let stackedChart, normalChart;

// Flow control variables
let isPaused = true;
let reachedEnd = false;

let currentSimData;


startSim(); // Start simulation
initializeCharts();

// Restart button
document.getElementById("restartBtn").addEventListener("click", function() {
    isPaused = true;
    startSim();
    initializeCharts();
    document.getElementById("pauseBtn").innerText = "Begin";
});
// Pause button
document.getElementById("pauseBtn").addEventListener("click", function() {
    isPaused = !isPaused;  
    document.getElementById("pauseBtn").innerText = isPaused ? "Resume" : "Pause";
    if (!isPaused) {
        runSim();  
    }
});
// Speed slider
document.getElementById("speedSlider").addEventListener("input", function() {
    daysPerSec = this.value;
    document.getElementById("simSpeed").innerText = parseInt(daysPerSec);
    //document.getElementById("daysPerSec").innerText = (fps/15).toFixed(1);
});
// fps slider
// document.getElementById("fpsSlider").addEventListener("input", function() {
//     FPS = this.value;
//     document.getElementById("fps").innerText = parseInt(FPS);
//     //document.getElementById("daysPerSec").innerText = (fps/15).toFixed(1);
// });

function startSim() {
    // initialize or restarts the simulation
    infectionRadius = parseFloat(document.getElementById("infectionRadius").value);
    infectionProb = parseFloat(document.getElementById("infectionProb").value)/100;
    infectiousPeriodDay = parseFloat(document.getElementById("infectiousPeriodDay").value);
    
    updateAnimatedValue("currentRad", infectionRadius);
    updateAnimatedValue("currentProb", infectionProb*100);
    updateAnimatedValue("currentPeriod", infectiousPeriodDay);

    reachedEnd = false;
    document.getElementById("diseaseStatus").classList.add("hidden");
    document.getElementById("pauseBtn").classList.remove("hidden")

    fetch("/start", { 
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            infectionRadius: parseFloat(infectionRadius),
            infectionProb: parseFloat(infectionProb),
            infectiousPeriodDay: parseFloat(infectiousPeriodDay)
        })
    })
        .then(response => response.json())
        .then(data => {
            fetchData();
            console.log("Simulation restarted:", data);
        });
}

function fetchData() {
    fetch("/data")  // Request new positions from Flask
        .then(response => response.json())
        .then(data => {
            drawParticles(data.boxsize, data.positions, data.states, data.state_count);
            document.getElementById("totalInfected").innerText = ((data.state_count[1] + data.state_count[2]) / N * 100).toFixed(1);
            // Update chart if day has changed
            if (document.getElementById("simulationDay").innerText != data.day){
                document.getElementById("simulationDay").innerText = data.day
                updateChart(data.day, data.state_count);
            };
            if (data.state_count[1] === 0 && !reachedEnd) {
                reachedEnd = true;
                isPaused = true;
                document.getElementById("pauseBtn").classList.add("hidden");
                document.getElementById("pauseBtn").innerText = "Begin";
                document.getElementById("diseaseStatus").classList.remove("hidden");

                controller.abort();  // Stop any pending fetch request
                console.log("Simulation ended. No more infected.");
            }
        });
}

let controller = new AbortController();

function runSim() {
    if (isPaused || reachedEnd) return;

    controller = new AbortController();
    
    let daysPerStep = daysPerSec / FPS;
    fetch(`/step?daysPerStep=${daysPerStep}`, { signal: controller.signal })  // Send stepsPerFrame to Flask
        .then(response => response.json())
        .then(() => fetchData()) 
        .catch(error => {
            if (error.name === "AbortError") {
                console.log("Fetch aborted due to pause.");
            } else {
                console.error("Error in runSim:", error);
            }
        });

    if (!isPaused && !reachedEnd) {
        setTimeout(runSim, 1000 / FPS);  // render every 1/FPS seconds
    }
}

function drawParticles(boxsize, positions, states) {
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    for (let i = 0; i < positions.length; i++) {
        let x = positions[i][0] * canvas.width/boxsize;
        let y = positions[i][1] * canvas.height/boxsize;

        // Choose color based on state
        let color = "green";  // Susceptible
        if (states[i] === 1) color = "red";  // Infected
        if (states[i] === 2) color = "gray";  // Removed

        ctx.beginPath();
        ctx.arc(x, y, 4, 0, Math.PI * 2);  // Draw dot
        ctx.fillStyle = color;
        ctx.fill();
        ctx.closePath();
    }
}

function initializeCharts() {
    // Reset data arrays:
    timeLabels = [];
    susData = [];
    infData = [];
    remData = [];
    
    // Destroy existing charts if they exist:
    if (stackedChart) stackedChart.destroy();
    if (normalChart) normalChart.destroy();
    
    pointRadius = 0;
    // Initialize the stacked chart
    const ctx1 = document.getElementById("stackedChart").getContext("2d");
    stackedChart = new Chart(ctx1, {
        type: "line",
        data: {
            labels: timeLabels,
            datasets: [
                {
                    label: "Removed",
                    data: remData,
                    backgroundColor: "gray",
                    borderColor: "gray",
                    fill: true,
                    borderWidth: 1,
                    pointRadius: pointRadius
                },
                {
                    label: "Infected",
                    data: infData,
                    backgroundColor: "red",
                    borderColor: "red",
                    fill: true,
                    borderWidth: 1,
                    pointRadius: pointRadius
                },
                {
                    label: "Susceptible",
                    data: susData,
                    backgroundColor: "green",
                    borderColor: "green",
                    fill: true,
                    borderWidth: 1,
                    pointRadius: pointRadius
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            scales: {
                x: {
                    title: { display: true, text: "Days" }
                },
                y: {
                    stacked: true,
                    title: { display: true, text: "Population" },
                    beginAtZero: true
                }
            }
        }
    });
    
    // Initialize the normal (non-stacked) chart
    const ctx2 = document.getElementById("normalChart").getContext("2d");
    normalChart = new Chart(ctx2, {
        type: "line",
        data: {
            labels: timeLabels,
            datasets: [
                {
                    label: "Removed",
                    data: remData,
                    backgroundColor: "gray",
                    borderColor: "gray",
                    fill: false,
                    borderWidth: 3,
                    pointRadius: pointRadius
                },
                {
                    label: "Infected",
                    data: infData,
                    backgroundColor: "red",
                    borderColor: "red",
                    fill: false,
                    borderWidth: 3,
                    pointRadius: pointRadius
                },
                {
                    label: "Susceptible",
                    data: susData,
                    backgroundColor: "green",
                    borderColor: "green",
                    fill: false,
                    borderWidth: 3,
                    pointRadius: pointRadius
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            scales: {
                x: {
                    title: { display: true, text: "Days"}
                },
                y: {
                    stacked: false,
                    title: { display: true, text: "Population" },
                    beginAtZero: true
                }
            }
        }
    });
}

function updateChart(day, stateCounts) {
    timeLabels.push(day);
    susData.push(stateCounts[0]);
    infData.push(stateCounts[1]);
    remData.push(stateCounts[2]);

    // Ensure chart updates
    stackedChart.data.labels = [...timeLabels];  // Copy to force update
    stackedChart.data.datasets[0].data = [...remData];
    stackedChart.data.datasets[1].data = [...infData];
    stackedChart.data.datasets[2].data = [...susData];
    stackedChart.update();  // Force Chart.js to refresh

    // Update normal chart
    normalChart.data.labels = [...timeLabels];
    normalChart.data.datasets[0].data = [...remData];
    normalChart.data.datasets[1].data = [...infData];
    normalChart.data.datasets[2].data = [...susData];
    normalChart.update();
}

function updateAnimatedValue(elementId, newValue) {
    let element = document.getElementById(elementId);
    if (element.innerText != newValue) {  
        element.innerText = newValue; 
        element.classList.add("flash");
        setTimeout(() => element.classList.remove("flash"), 600);
    }
}


