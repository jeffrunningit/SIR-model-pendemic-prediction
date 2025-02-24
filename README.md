# SIR Pandemic Simulation

This project is a full-stack simulation of a pandemic based on the classic SIR (Susceptible, Infected, Removed) model. It was built using Python, Flask, and JavaScript, and features real‑time visualization of the simulation via a web interface. The simulation demonstrates data modeling, numerical methods, and web development skills.

## Overview

The simulation models the spread of an infectious disease in a closed population. Key features include:

- **Dynamic Visualization:** A live simulation is rendered on an HTML canvas, with updated positions of individuals.
- **Data Tracking:** Real-time charts display the evolution of the susceptible, infected, and removed populations.
- **Customizable Parameters:** Users can adjust parameters like infection radius, infection probability, and infectious period via a web interface.
- **REST API:** The Flask backend handles simulation steps and parameter updates, making it easy to extend or integrate with other systems.

## Demo

The simulation is hosted online. You can view and interact with it here:  
[https://sir-model-pendemic-prediction-production.up.railway.app/](https://sir-model-pendemic-prediction-production.up.railway.app/)

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

    ```
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

# The SIR Model: Analytical Foundations and Simulation Implementation

The SIR model is a cornerstone of mathematical epidemiology, offering a simple yet powerful framework to describe the spread of infectious diseases. In this model, a closed population is divided into three compartments: **Susceptible (S)**, **Infected (I)**, and **Removed (R)**. The evolution of these compartments over time is typically modeled using a system of ordinary differential equations (ODEs):

$$
\frac{dS}{dt} = -\beta SI,\\
\\
\frac{dI}{dt} = \beta SI - \gamma I,\\
\\
\frac{dR}{dt} = \gamma I.
$$


Here, **β** (beta) represents the effective contact rate that combines the average number of contacts per individual and the probability of disease transmission per contact, while **γ** (gamma) is the recovery rate, defined as the reciprocal of the infectious period. An important derived parameter is the basic reproduction number, **\( R_0 \)**, given by:

\[
R_0 = \frac{\beta}{\gamma}.
\]

This value indicates the average number of secondary infections produced by a single infected individual in a fully susceptible population. If \( R_0 > 1 \), the infection will likely spread in the population; if \( R_0 < 1 \), the outbreak will eventually die out.

In our simulation, we implement a discrete, spatial version of the SIR model. Instead of solving the ODEs analytically, the simulation uses numerical methods to mimic the behavior of the SIR system in a two-dimensional space. Here’s how the simulation parameters relate to the analytical model:

- **Infection Radius:**  
  In the simulation, each individual is assigned a position in a 30m x 30m area using Poisson Disk sampling. The **infection_radius** defines the spatial threshold within which an infected individual can potentially transmit the disease to a susceptible one. This parameter influences the effective contact rate by limiting the number of contacts an infected individual can make, analogous to the “contact frequency” component in the beta parameter.

- **Infection Probability:**  
  The **infection_probability** sets the chance that, upon contact (i.e., being within the infection_radius), the disease will be transmitted from an infected individual to a susceptible one. This probability directly corresponds to the transmission efficiency component of beta in the ODE model. A higher infection_probability increases the effective value of β, thereby raising \( R_0 \).

- **Infectious Period Day:**  
  The **infectious_period_day** parameter specifies the duration (in days) that an infected individual remains contagious before transitioning to the Removed state. In the continuous model, the recovery rate γ is defined as the reciprocal of the infectious period (γ ≈ 1/infectious_period_day). Thus, a longer infectious period results in a lower recovery rate, allowing the infection to persist longer in an individual and potentially increasing \( R_0 \).

The simulation discretizes time into small steps, during which individuals move within the simulation box following assigned velocities. A KDTree data structure is employed to efficiently locate all susceptible individuals within the infection_radius of an infected individual. At each step, probabilistic transmission is applied based on the infection_probability. After accumulating enough steps to represent a full day, the simulation updates the state of each individual, moving those who have been infected for longer than the infectious_period_day into the Removed category.

In summary, while the classical SIR model uses differential equations to describe disease dynamics, our simulation translates these continuous processes into discrete steps, capturing spatial interactions through parameters such as infection_radius, infection_probability, and infectious_period_day. This approach not only provides a visual, interactive demonstration of epidemic spread but also reinforces the underlying principles of the analytical model.

# Understanding the SIR Model: A Mathematical Approach to Epidemic Spread

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

## Understanding Parameters in Real-Life Analogy
1. **Infection Radius**: In spatial models, this represents how far an infected person can spread the disease. It is analogous to physical distancing—larger infection radii correspond to high-contact environments.
2. **Infectious Duration (1/\( \gamma \))**: This defines how long an individual remains infectious before recovery. It correlates to real-world disease recovery periods.
3. **Infection Probability**: This measures how likely a susceptible person becomes infected upon contact. It depends on factors such as immunity and pathogen strength.

## Applications and Significance
The SIR model is used in epidemiology to predict disease outbreaks, inform public health policies, and simulate containment strategies. By adjusting parameters, we can assess the impact of interventions like vaccination, social distancing, and quarantine measures. 

In summary, the SIR model provides a mathematical foundation to understand how diseases spread, how interventions alter transmission, and how outbreaks can be controlled.

