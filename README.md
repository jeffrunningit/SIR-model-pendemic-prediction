![#SIR Pandemic Simulation](sir_logo.png)
---
This project is a simulation of a pandemic based on the classic SIR (Susceptible, Infected, Removed) model. It was built using Python, Flask, and JavaScript, and features real‑time visualization of the simulation via a web interface. The simulation demonstrates data modeling, numerical methods and programming skills.

## Overview

The simulation models the spread of an infectious disease in a closed population. Key features include:

- **Dynamic Visualization:** A live simulation is rendered on an HTML canvas, with updated positions of individuals.
- **Data Tracking:** Real-time charts display the evolution of the susceptible, infected, and removed populations.
- **Customizable Parameters:** Users can adjust parameters like infection radius, infection probability, and infectious period via a web interface.

## Demo

The simulation is hosted online. You can view and interact with it here:  
[https://sir-model-pendemic-prediction-production.up.railway.app/](https://sir-model-pendemic-prediction-production.up.railway.app/)

<img src="sim_image.png" alt="Description" width="300"/>

Running the app locally is recommended for best performance.

## Requirements

- Python 3.7+
- Flask
- NumPy
- SciPy
- Chart.js (loaded via CDN in the HTML)

## Installation

To run the simulation locally:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/jeffrunningit/SIR-model-pendemic-prediction-python.git
    cd SIR-pandemic-simulation-python

2. **Install the required packages**

    ```bash
    pip install -r requirements.txt

3. **Run the flask app**

    ```bash
    python3 app.py

4. 	Open your browser and navigate to http://localhost:8000 to see the simulation in action.

## Project structure

    .
    ├── README.md
    ├── sim_latest.py
    ├── app.py
    ├── railwayapp.py
    ├── requirements.txt
    ├── results
    │   ├── ani.png
    │   ├── frame0.png
    │   ├── ...
    │   ├── original_2.4_0.15_6.png
    │   ├── ...
    ├── static
    │   ├── animation.js
    │   ├── animation_nofpsslider.js
    │   ├── cmunbx.ttf
    │   ├── cmunrb.ttf
    │   ├── cmunrm.ttf
    │   ├── styles.css
    └── templates
        ├── siminterface.html
        └── siminterface_nofpsslider.html

## How it works

The simulation logic is encapsulated in a `Population` class that initializes a fixed number of individuals distributed evenly in a 30m x 30m area using Poisson Disk sampling. Each individual is assigned a random velocity and an initial state: Susceptible, Infected, or Removed. (with one starting as infected near the center), and during each time step, they move while reflected at the boundaries, similar to physical particles. 

To simulate the spread of the disease, a KDTree is used to efficiently locate susceptible individuals within an infection radius around each infected person, allowing for probabilistic transmission of the disease at each "day" interval. After a full day’s worth of steps, the infection duration for each infected individual is updated, and those exceeding the infectious period are transitioned to the Removed state, while the simulation continuously tracks and updates the counts of susceptible, infected, and removed individuals.

# The SIR Model: A Mathematical Approach to Epidemic Spread

The **Susceptible-Infectious-Recovered (SIR) model** is a fundamental mathematical framework used to describe the spread of infectious diseases. It categorizes a population into three compartments:

- **Susceptible (S)**: Individuals who can contract the disease.
- **Infected (I)**: Individuals who have the disease and can transmit it.
- **Recovered (R)**: Individuals who have recovered and gained immunity.

## Differential Equations of the SIR Model
The SIR model is governed by the following differential equations:

```math
\frac{dS}{dt} = -\beta S I
```
```math
\frac{dI}{dt} = \beta S I - \gamma I
```
```math
\frac{dR}{dt} = \gamma I
```

where:
- **$\beta$** (infection rate) represents the rate at which susceptible individuals become infected.
- **$\gamma$** (recovery rate) is the rate at which infected individuals recover and move to the recovered compartment.

The basic reproduction number, **$R_0$**, is given by:
```math
R_0 = \frac{\beta}{\gamma}
```
If **$R_0 > 1$**, the disease spreads; if **$R_0 < 1$**, the outbreak diminishes.

## Simulation Parameters Analogy in Real-Life 
1. **Infection Radius**: In spatial models, this represents how far an infected person can spread the disease. It is analogous to physical distancing—larger infection radii correspond to high-contact environments.
2. **Infection Probability**: This measures how likely a susceptible person becomes infected upon contact. It depends on factors such as immunity and pathogen strength.
3. **Infectious Duration $1/\gamma$**: This defines how long an individual remains infectious before recovery. It correlates to real-world disease recovery periods.

## Applications and Significance
The SIR model is used in epidemiology to predict disease outbreaks, inform public health policies, and simulate containment strategies. By adjusting parameters, we can assess the impact of interventions like vaccination, social distancing, and quarantine measures. 

In summary, the SIR model provides a mathematical foundation to understand how diseases spread, how interventions alter transmission, and how outbreaks can be controlled.

## Further Reading

For more detailed explanation of the SIR model and epidemiological modeling, consider these resources:

- Beckley R, Weatherspoon C, Alexander M, Chandler M, Johnson A, Bhatt GS (2013). "Modeling epidemics with differential equations". Tennessee State University Internal Report

- Wikipedia page on [Compartmental models in epidemiology](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SIR_model)

