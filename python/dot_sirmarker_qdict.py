from math import *
from random import random
from collections import defaultdict
from itertools import combinations


def box_muller():
    return sqrt(-2 * log(random())) * cos(2 * pi * random())

class Dots:
    def __init__(self):
        self.box_size = 30
        self.N = 900
        self.day = [0]
        self.susceptible = [900]
        self.infected = [0]
        self.removed = [0]
        self.R = [0]
        self.inf_duration = 0
        self.inf_prob = 0
        self.inf_rad_sqr = 0
        self.step = 0
        self.x, self.y, self.vx, self.vy = [], [], [], []
        self.infected_no, self.infected_time = [], []
        self.q_state = defaultdict(list)
        self.q_state['Not q'] = list(range(self.N))
        for _ in range(self.N - 1):
            self.x.append(random() * 30)
            self.y.append(random() * 30)
            self.vx.append(0.2 * box_muller())
            self.vy.append(0.2 * box_muller())
            self.infected_no.append(0)
            self.infected_time.append(0)
        rand_angle = random() * 2 * pi
        self.x.append(15)
        self.y.append(15)
        self.vx.append(0.5*cos(rand_angle))
        self.vy.append(0.5*sin(rand_angle))
        self.infected_no.append(0)
        self.infected_time.append(0)
        self.ij_pairs = combinations(range(self.N), 2)
        self.si_marker = self.N - 1
        self.ir_marker = self.N

    def force_scale(self, i, j):
        self.dist_sqr(i, j)

    def move(self):
        for i in range(len(self.x)):
            self.x[i], self.y[i] = self.x[i] + self.vx[i], self.y[i] + self.vy[i]
            if self.x[i] < 0:
                self.x[i], self.vx[i] = -self.x[i], -self.vx[i]
            elif self.x[i] > self.box_size:
                self.x[i], self.vx[i]= self.box_size * 2 - self.x[i], -self.vx[i]
            if self.y[i] < 0:
                self.y[i], self.vy[i] = -self.y[i], -self.vy[i]
            elif self.y[i] > self.box_size:
                self.y[i], self.vy[i] = self.box_size * 2 - self.y[i], -self.vy[i]

    def change_state(self, i, state):
        if state == 1:
            self.si_marker -= 1
            self.move_position(i, self.si_marker)
        if state == 2:
            self.ir_marker -= 1
            self.move_position(i, self.ir_marker)

    def move_position(self, i, j):
        self.x.insert(j, self.x.pop(i))
        self.y.insert(j, self.y.pop(i))
        self.vx.insert(j, self.vx.pop(i))
        self.vy.insert(j, self.vy.pop(i))
        self.infected_no.insert(j, self.infected_no.pop(i))
        self.infected_time.insert(j, self.infected_time.pop(i))

    def infect(self):
        # loop through infected
        for i in range(self.si_marker, self.ir_marker):
            # loop through susceptible
            for j in reversed(range(self.si_marker)):
                if random() < self.inf_prob and self.dist_sqr(i, j) < self.inf_rad_sqr:
                    self.change_state(j, 1)

    def update_infection_time(self):
        for i in reversed(range(self.si_marker, self.ir_marker)):
            self.infected_time[i] += 1
            if self.infected_time >= self.inf_duration:
                self.change_state(i, 2)

    def append_sir_data(self):
        self.day.append(self.day[-1] + 1)
        self.susceptible.append(self.si_marker)
        self.infected.append(self.ir_marker - self.si_marker)
        self.removed.append(self.N - self.ir_marker)

    def update_R_value(self):
        self.R = 0
        for i in range(self.si_marker, self.N):
            self.R += self.infected_no[i] / self.infected_time[i] * self.inf_duration
        self.R /= self.N - self.si_marker

    def quarantine(self, incubation_day, quar_prob):
        for i, time in enumerate(self.infected_time):
            if time >= incubation_day:
                self.q_state['Not q'].remove(i)
                if random() < quar_prob:
                    self.q_state['In q'].append(i)
                else:
                    self.q_state['Escaped'].append(i)

    def dist_sqr(self, i, j):
        dx = self.x[i] - self.x[j]
        dy = self.y[i] - self.y[j]
        return dx * dx + dy * dy
