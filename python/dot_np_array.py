from math import *
from random import random
import numpy as np
from itertools import combinations
from itertools import product
from collections import deque


def box_muller():
    return sqrt(-2 * log(random())) * cos(2 * pi * random())

def constrain(value, max):
    if value >= max:
        return max
    elif value <= -max:
        return -max
    else:
        return value

class Dots:
    def __init__(self):
        self.box_size = 40
        self.N = 400
        self.maxspd = 0.05
        self.steps_per_day = 10
        self.day = [0]                      # record dates for plotting
        self.susceptible = [self.N]         # record susceptible count
        self.infected = [0]                 # record infected count
        self.removed = [0]                  # record removed count
        self.R = [0]                        # record R value
        self.inf_duration = 0               # duration of disease
        self.inf_prob = 0                   # probability of infection
        self.inf_rad = 0
        self.inf_rad_sqr = 0                # radius of infection
        self.step = 0                       # count no of steps
        rand_angle = random() * 2 * pi
        # initiate positions
        # set last one at center
        self.x = np.array([random() * self.box_size for _ in range(self.N - 1)]+[self.box_size/2], dtype=float)
        self.y = np.array([random() * self.box_size for _ in range(self.N - 1)]+[self.box_size/2], dtype=float)
        # initiate velocities using the box muller transform
        # fix the velocity of the first patient
        self.vx = np.array([box_muller() * 0.02 for _ in range(self.N - 1)]+[cos(rand_angle) * 0.02], dtype=float)
        self.vy = np.array([box_muller() * 0.02 for _ in range(self.N - 1)]+[sin(rand_angle) * 0.02], dtype=float)
        # initiate acceleration arrays
        self.ax = np.zeros(self.N, dtype=float)
        self.ay = np.zeros(self.N, dtype=float)
        self.new_ax = np.zeros(self.N, dtype=float)
        self.new_ay = np.zeros(self.N, dtype=float)
        # record number each one infected
        self.infected_no = np.zeros(self.N, dtype=np.int16)
        # record time since infection
        self.infected_time = np.zeros(self.N, dtype=np.int16)
        # signals broadcasted
        self.broadcasted = np.array([deque([1 for _ in range(7)]) for _ in range(self.N)])
        # signals received
        self.received = np.array([set() for _ in range(self.N)])
        # arrays of indices of different states (0=s, 1=i, 2=r)
        self.state_0 = list(range(self.N - 1))
        self.state_1 = [self.N - 1]
        self.state_2 = []
        # arrays of quarantine states
        self.q_state_0 = list(range(self.N))    # not in quarantine
        self.q_state_1 = []                     # in quarantine
        self.q_state_2 = []                     # escaped quarantine
        self.quar = False                       # trigger quarantine
        self.socdist = False                    # trigger social distancing
        self.socdistdate = 0
        self.ij_pairs = combinations(range(self.N), 2)

    # move all dots
    def move(self):
        self.step += 1
        for i in range(self.N):
            self.x[i], self.y[i] = self.x[i] + self.vx[i], self.y[i] + self.vy[i]
            if self.x[i] < 0:
                self.x[i], self.vx[i] = -self.x[i], -self.vx[i]
            elif self.x[i] > self.box_size:
                self.x[i], self.vx[i] = self.box_size * 2 - self.x[i], -self.vx[i]
            if self.y[i] < 0:
                self.y[i], self.vy[i] = -self.y[i], -self.vy[i]
            elif self.y[i] > self.box_size:
                self.y[i], self.vy[i] = self.box_size * 2 - self.y[i], -self.vy[i]

    # move dots not in quarantine
    def qmove(self):
        self.step += 1
        for i in self.q_state_0 + self.q_state_2:
            self.x[i], self.y[i] = self.x[i] + self.vx[i], self.y[i] + self.vy[i]
            if self.x[i] < 0:
                self.x[i], self.vx[i] = -self.x[i], -self.vx[i]
            elif self.x[i] > self.box_size:
                self.x[i], self.vx[i] = self.box_size * 2 - self.x[i], -self.vx[i]
            if self.y[i] < 0:
                self.y[i], self.vy[i] = -self.y[i], -self.vy[i]
            elif self.y[i] > self.box_size:
                self.y[i], self.vy[i] = self.box_size * 2 - self.y[i], -self.vy[i]

    # move dots with force
    def update_force(self):
        self.new_ax = np.zeros(self.N)
        self.new_ay = np.zeros(self.N)
        for i, j in self.ij_pairs:
            r = sqrt(self.dist_sqr(i, j))
            if r < 1:
                ascale = 0.5 / r
                self.new_ax[i] += ascale * (self.x[i] - self.x[j])
                self.new_ax[j] += -ascale * (self.x[i] - self.x[j])
                self.new_ay[i] += ascale * (self.y[i] - self.y[j])
                self.new_ay[j] += -ascale * (self.y[i] - self.y[j])

    def fmove(self):
        self.step += 1
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        for i in range(self.N):
            self.x[i], self.y[i] = self.x[i] + self.vx[i], self.y[i] + self.vy[i]
            if self.x[i] < 0:
                self.x[i], self.vx[i] = -self.x[i], -self.vx[i]
            elif self.x[i] > self.box_size:
                self.x[i], self.vx[i] = self.box_size * 2 - self.x[i], -self.vx[i]
            if self.y[i] < 0:
                self.y[i], self.vy[i] = -self.y[i], -self.vy[i]
            elif self.y[i] > self.box_size:
                self.y[i], self.vy[i] = self.box_size * 2 - self.y[i], -self.vy[i]
        for i in range(self.N):
            self.vx[i] = constrain(self.vx[i] + (random()-0.5) * 0.05, self.maxspd)
            self.vy[i] = constrain(self.vy[i] + (random()-0.5) * 0.05, self.maxspd)
        if self.socdist:
            for i, j in self.ij_pairs:
                ang = atan2(self.y[i] - self.y[j], self.x[i] - self.y[j])
                dist = sqrt(self.dist_sqr(i, j))
                if dist < 10:
                    force = 40 * (1 - dist / self.inf_rad)
                    self.vx[i] += force * cos(ang)
                    self.vy[i] += force * sin(ang)

    def infect(self):
        init_state_1 = [i for i in self.state_1 if i in self.q_state_0]
        # loop through susceptible
        for i in [i for i in self.state_0 if i in self.q_state_0]:
            # loop through infected
            for j in init_state_1:
                if random() < self.inf_prob and self.dist_sqr(i, j) < self.inf_rad_sqr:
                    self.state_0.remove(i)
                    self.state_1.append(i)
                    break

    def broadcast_receive(self):
        for i in self.state_1:
            self.broadcasted[i].popleft()                                           # remove old broadcast
            self.broadcasted[i].append(self.step + random())                        # add new broadcast
        for i in range(self.N):
            self.received[i] = [num for num in self.received[i]
                                if num > self.step - self.inf_duration]             # remove old signals
        for i, j in product(self.state_1, self.q_state_0 + self.q_state_2):
            if self.dist_sqr(i, j) < self.inf_rad_sqr:
                self.received[j].add(self.broadcasted[i][-1])                       # add signal to received

    def update_infection_time(self):
        self.infected_time[self.state_1] += 1
        for i in self.state_1:
            if self.infected_time[i] >= self.inf_duration:
                self.state_1.remove(i)
                self.state_2.append(i)

    def append_sir_data(self):
        self.day.append(self.day[-1] + 1)
        self.susceptible.append(len(self.state_0))
        self.infected.append(len(self.state_1))
        self.removed.append(len(self.state_2))

    def update_R_value(self):
        self.R = 0
        self.R = sum(self.infected_no / self.infected_time * self.inf_duration)
        self.R /= len(self.state_1)+len(self.state_2)

    def quarantine(self, incubation_day, quar_prob):
        for i in self.q_state_0:
            if self.infected_time[i]*self.steps_per_day >= incubation_day:
                print(i)
                self.q_state_0.remove(i)
                if random() < quar_prob/self.steps_per_day:
                    self.q_state_1.append(i)
                else:
                    self.q_state_2.append(i)

    def dist_sqr(self, i, j):
        dx = self.x[i] - self.x[j]
        dy = self.y[i] - self.y[j]
        return dx * dx + dy * dy
