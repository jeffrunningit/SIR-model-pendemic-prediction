const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const boxSize = 30;  // Match Python simulation size
const N = 900;  // Number of particles
const FPS = 30;  // Frames per second

canvas.width = 500;
canvas.height = 500;

let stepsPerDay = 5;
let daysPerSec = 30/5;

let infectionRadius;
let infectionProb;
let infectiousPeriodDay;

// For cumulative chart data
let timeLabels = [0];  // Stores the days elapsed
let susData = [899];  // Stores the number of susceptible people
let infData = [1];  // Stores the number of infected people
let remData = [0];  // Stores the number of removed people

// Initialize Chart.js chart variable
let stateChart;

// Flow control variables
let isPaused = true;
let reachedEnd = false;


startSim(); // Start simulation
initializeChart();

// Restart button
document.getElementById("restartBtn").addEventListener("click", function() {
    startSim();
    initializeChart();
    document.getElementById("pauseBtn").innerText = isPaused ? "Begin" : "Pause";
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
    stepsPerDay = Math.round(FPS / daysPerSec);
    document.getElementById("simSpeed").innerText = parseInt(daysPerSec);
    //document.getElementById("daysPerSec").innerText = (fps/15).toFixed(1);
});

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
            console.log("Simulation restarted:", data);
            fetchData();
        });
    
}

function fetchData() {
    fetch("/data")  // Request new positions from Flask
        .then(response => response.json())
        .then(data => {
            drawParticles(data.boxsize, data.positions, data.states, data.state_count);
            document.getElementById("totalInfected").innerText = ((data.state_count[1] + data.state_count[2]) / N * 100).toFixed(1);
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
            }
        });
}

function runSim() {
    if (isPaused) return;

    fetch(`/step?stepsPerDay=${stepsPerDay}`)  // ✅ Send stepsPerFrame to Flask
        .then(response => response.json())  // ✅ Expect JSON response
        .then(() => fetchData()) 
        .catch(error => console.error("Error in runSim:", error));
    
    if (!isPaused){
        setTimeout(runSim, 1000 / FPS);  // ✅ Always render at 30 FPS max
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

function initializeChart() {
    timeLabels = [];  // Stores the days elapsed
    susData = [];  // Stores the number of susceptible people
    infData = [];  // Stores the number of infected people
    remData = [];  // Stores the number of removed people

    if (stateChart) {
        stateChart.destroy();
        console.log("Previous chart destroyed");
    }

    const ctx = document.getElementById("stateChart").getContext("2d");
    stateChart = new Chart(ctx, {
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
                    borderWidth: 1
                },
                {
                    label: "Infected",
                    data: infData,
                    backgroundColor: "red",
                    borderColor: "red",
                    fill: true,
                    borderWidth: 1
                },
                {
                    label: "Susceptible",
                    data: susData,
                    backgroundColor: "green",
                    borderColor: "green",
                    fill: true,
                    borderWidth: 1
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
}

function updateChart(day, stateCounts) {
    timeLabels.push(day);
    susData.push(stateCounts[0]);
    infData.push(stateCounts[1]);
    remData.push(stateCounts[2]);

    // Ensure chart updates
    stateChart.data.labels = [...timeLabels];  // Copy to force update
    stateChart.data.datasets[0].data = [...remData];
    stateChart.data.datasets[1].data = [...infData];
    stateChart.data.datasets[2].data = [...susData];

    stateChart.update();  // 🔥 Force Chart.js to refresh
}

function updateAnimatedValue(elementId, newValue) {
    let element = document.getElementById(elementId);
    if (element.innerText != newValue) {  
        element.innerText = newValue; 
        element.classList.add("flash");
        setTimeout(() => element.classList.remove("flash"), 600);
    }
}


