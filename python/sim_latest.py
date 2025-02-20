import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.qmc import PoissonDisk
from scipy.spatial import KDTree
from itertools import product


class Population:
    def __init__(self, infection_radius_m=1, 
                 infection_probability=0.5, 
                 infectious_period_day=3, 
                 N=900, max_speed_mpday=1):
        
        self.N = N  # Number of particles
        self.box_size = 30  # Size of the simulation box
        self.max_speed_mpday = max_speed_mpday  # Maximum speed of particles

        # Infection parameters
        self.infection_radius_m = infection_radius_m
        self.infection_probability = infection_probability
        self.infectious_period_day = infectious_period_day       
        self.infection_r_squared = infection_radius_m ** 2
        
        # Initialize positions, velocities, and states
        # evenly fill the box using PoissonDisk
        poissondisk_radius = 1 / np.sqrt(N) * 0.7
        engine = PoissonDisk(d=2, radius=poissondisk_radius)
        for _ in range(100):
            points = engine.fill_space()
            if len(points) >= N: break
        if len(points) > N: 
            points = points[np.random.choice(len(points), N, replace=False)]
        self.positions = points * self.box_size
        speeds = (np.random.rand(N) * 0.5 + 0.5) * self.max_speed_mpday
        angles = np.random.rand(N) * 2 * np.pi
        self.velocities = np.column_stack((speeds * np.sin(angles), speeds * np.cos(angles)))

        # States: 0 = Susceptible, 1 = Infected, 2 = Removed
        self.states = np.zeros(N, dtype=int)
        center = np.array((0.5, 0.5))
        center_index = np.argmin(np.sum((points - center) ** 2, axis=1))
        # Infect the middle person
        self.states[center_index] = 1  
        self.statescount = np.array([N-1, 1, 0])
        # Make sure the patient 0 is moving at max speed
        self.velocities[center_index] = self.velocities[center_index] * max_speed_mpday/np.linalg.norm(self.velocities[center_index])
        self.infected_time = np.zeros(N, dtype=int)

        # Step tracking
        self.stepcount = 0
        self.day = 0
        
    def step(self, stepsPerday):
        """Move forward by a step"""
        self.move(stepsPerday)
        self.stepcount += 1
        # Infect and update once a day
        if self.stepcount % stepsPerday == 0:
            self.infect()
            self.update_infected_time()
            self.statescount = np.array([
                np.sum(self.states==0),
                np.sum(self.states==1),
                np.sum(self.states==2)
                ])
            self.day += 1
            

    def move(self, stepsPerDay = 1):
        """Update particle positions with periodic boundary conditions"""
        dt = 1 / stepsPerDay
        self.positions += self.velocities * dt
        
        # Reflection at boundaries
        for i in range(2):
            outofbounds_upper = self.positions[:, i] > self.box_size
            outofbounds_lower = self.positions[:, i] < 0

            # reflect positions
            self.positions[outofbounds_upper, i] = 2 * self.box_size - self.positions[outofbounds_upper, i]
            self.positions[outofbounds_lower, i] = -self.positions[outofbounds_lower, i]
            
            # reflect velocities
            self.velocities[outofbounds_upper, i] = -self.velocities[outofbounds_upper, i]
            self.velocities[outofbounds_lower, i] = -self.velocities[outofbounds_lower, i]
            

    def infect(self):
        """Simulate infection spread"""
        infected_indices = np.where(self.states == 1)[0]
        susceptible_indices = np.where(self.states == 0)[0]
        if len(infected_indices) == 0 or len(susceptible_indices) == 0:
            return # no infection possible
        
        ## Build KDTree data structure to find nearest neighbors
        ## O(N log N) complexity
        SItree = KDTree(self.positions[susceptible_indices])
        for i in infected_indices:
            nearby_idx = SItree.query_ball_point(self.positions[i], self.infection_radius_m)
            
            # Infect nearby susceptibles
            for idx in nearby_idx:
                if np.random.rand() < self.infection_probability:
                    self.states[susceptible_indices[idx]] = 1
                    
        ## Brute force method looping over every pair of S and I particles
        ## O(N^2) complexity
        #Ibefore = np.sum(self.states==1)
        # for i, j in product(infected_indices, susceptible_indices):
        #     dist_squared = np.sum((self.positions[j] - self.positions[i])**2)
        #     if dist_squared < self.infection_r_squared and np.random.rand() < self.infection_probability:
        #         self.states[j] = 1
        #Iafter = np.sum(self.states==1)
        #print(f"{Iafter-Ibefore} peopole infected.")
        

    def update_infected_time(self):
        """Update infection duration and move to removed state"""
        self.infected_time = np.where(self.states == 1, self.infected_time + 1, self.infected_time)
        self.states = np.where((self.states == 1) & (self.infected_time > self.infectious_period_day), 2, self.states)

