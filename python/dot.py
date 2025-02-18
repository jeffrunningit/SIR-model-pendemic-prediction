import math
from random import random
from itertools import combinations


def box_muller():
    return math.sqrt(-2 * math.log(random())) * math.cos(2 * math.pi * random())

class State_bin:
    def __init__(self):
        self.x, self.y, self.vx, self.vy = [], [], [], []
        self.infected_no, self.infected_time = [], []
def change_state(i, j):



class Dots:

    def __init__(self):
        self.box_size = 30
        self.N = 900
        self.susceptible = 900
        self.infected = 0
        self.removed = 0
        self.R = 0
        self.inf_duration = 0
        self.inf_prob = 0
        self.inf_rad_sqr = 0
        self.index_pairs = list(combinations(range(self.N), 2))
        self.step = 0
        self.state = [State_bin(), State_bin(), State_bin()]
        for _ in range(self.N):
            self.state[0].x.append(random() * 30)
            self.state[0].y.append(random() * 30)
            self.state[0].vx.append(0.2 * box_muller())
            self.state[0].vy.append(0.2 * box_muller())
            self.state[0].infected_no.append(0)
            self.state[0].infected_time.append(0)

    def move(self):
        for i in range(self.N):
            self.x[i] += self.vx[i]
            self.y[i] += self.vy[i]
            if self.x[i] < 0:
                self.x[i] = -self.x[i]
                self.vx[i] = -self.vx[i]
            elif self.x[i] > self.box_size:
                self.x[i] = self.box_size * 2 - self.x[i]
                self.vx[i] = -self.vx[i]
            if self.y[i] < 0:
                self.y[i] = -self.y[i]
                self.vy[i] = -self.vy[i]
            elif self.y[i] > self.box_size:
                self.y[i] = self.box_size * 2 - self.y[i]
                self.vy[i] = -self.vy[i]

    def infect_center(self):
        least_dist = 1000
        marker = 0
        for i in range(self.N):
            if self.dist_from_cent(i) < least_dist:
                marker = i
                least_dist = self.dist_from_cent(i)
        self.state[marker] = 1

    def infect(self):
        for (i, j) in self.index_pairs:
            if self.state[i] == 1 and self.state[j] == 0:
                if random() < self.inf_prob:
                    if self.distsqr(i, j) < self.inf_rad_sqr:
                        self.state[j] = 1
            elif self.state[j] == 1 and self.state[i] == 0:
                if random() < self.inf_prob:
                    if self.distsqr(i, j) < self.inf_rad_sqr:
                        self.state[i] = 1

    def update_infection_time(self):
        for i in range(self.N):
            if self.state[i] == 1 or self.state[i] == 3:
                self.infected_time[i] += 1
            if self.infected_time[i] > self.inf_duration:
                self.state[i] = 2

    def update_sir(self):
        self.susceptible = 0
        self.infected = 0
        self.removed = 0
        self.R = 0
        for i in range(self.N):
            if self.state[i] == 1:
                self.infected += 1
                self.R += self.infected_no[i] / self.infected_time[i] * self.inf_duration
            elif self.state[i] == 0:
                self.susceptible += 1
            else:
                self.removed += 1
        if self.infected > 0:
            self.R /= (self.infected + self.removed)

    def quarantine(self, trigger_day, incubation_day, quar_prob):
        for i in range(self.N):
            if self.infected_time >= incubation_day:
                self.quarantine_state[i] = True

    def distsqr(self, i, j):
        dx = self.x[i] - self.x[j]
        dy = self.y[i] - self.y[j]
        return dx * dx + dy * dy

    def dist_from_cent(self, i):
        dx = self.x[i] - self.box_size / 2
        dy = self.y[i] - self.box_size / 2
        return math.sqrt(dx * dx + dy * dy)
