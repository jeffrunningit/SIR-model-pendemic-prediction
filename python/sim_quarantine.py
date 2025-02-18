from dot_np_array import Dots
from time import time
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def do_step():    # settings for simulation
    D.qmove()
    D.infect()
    D.update_infection_time()
    if len(D.state_1) > threshold:
        D.quar = True
    if D.quar:
        D.quarantine(incub, q_prob)

def sim_sir_data():
    while True:
        print(D.step)
        # do steps for a day
        for _ in range(D.steps_per_day):
            do_step()
        # output data
        D.append_sir_data()
        if D.infected[-1] == 0:
            break

def plot_sir():
    ax.cla()
    ax.set_ylabel('Count')
    ax.set_xlabel('Day')
    title = 'SIR plot (r=%.1f, p=%.2f, d=%f)' % (rad, prob, duration)
    ax.set_title(title)
    ax.stackplot(D.day, D.infected, D.removed, D.susceptible, colors=['red', 'grey', 'green'])

def animate_sir():
    # Add sir data
    # Plot data in animation
    D.append_sir_data()
    ax1.cla()
    ax1.set_ylabel('Count')
    ax1.set_xlabel('Day')
    title = 'SIR plot (r=%.1f, p=%.2f, d=%.0f)' % (rad, prob, duration)
    ax1.set_title(title)
    ax1.stackplot(D.day, D.infected, D.removed, D.susceptible, colors=['red', 'grey', 'green'])

color_map = np.array(['green', 'red', 'grey'])
marker_map = np.array(['o','+','o'])
def animate_dots():
    # Output frame
    ax2.cla()
    ax2.set_xlim([0, 30])
    ax2.set_ylim([0, 30])
    ax2.set_xticks([])
    ax2.set_yticks([])
    state = np.zeros(D.N, dtype=int)
    state[D.state_1] = 1
    state[D.state_2] = 2
    ax2.scatter(np.array(D.x)[D.q_state_0], np.array(D.y)[D.q_state_0],
                c=color_map[state[D.q_state_0]], marker=marker_map[0])
    ax2.scatter(np.array(D.x)[D.q_state_1], np.array(D.y)[D.q_state_1],
                c=color_map[state[D.q_state_1]], marker=marker_map[1])
    ax2.scatter(np.array(D.x)[D.q_state_2], np.array(D.y)[D.q_state_2],
                c=color_map[state[D.q_state_2]], marker=marker_map[2])


def animation(i):
    # do a step
    do_step()
    # plot data onto both graphs
    animate_dots()
    animate_sir()
    # check for termination
    if len(D.state_1) == 0:
        ani.event_source.stop()
        end_time1 = time() - start_time
        print('Simulation completed in %f seconds.' % end_time1)


mode = input('1 = animate: ')
if mode == '1':
    animate = True
else:
    animate = False

last_input = []     # create list to store last input for restart
while True:
    # take input
    input_string = input("Enter 3 parameters threshold, q_prob, incubday: ")
    # check for restart
    if not input_string:
        if not last_input:
            print('No input yet.')
            continue
        else:
            threshold, q_prob, incub = last_input
            print('Restart simulation.')
    else:
        rpd = input_string.split()
        threshold, q_prob, incub = float(rpd[0]), float(rpd[1]), float(rpd[2])
        last_input = [threshold, q_prob, incub]

    start_time = time()         # record starting time
    rad, prob, duration = 3, 0.2, 6
    D = Dots()                  # create dots
    D.inf_rad_sqr = rad * rad
    D.inf_prob = prob / D.steps_per_day
    D.inf_duration = duration * D.steps_per_day

    if not animate:

        sim_sir_data()

        end_time2 = time() - start_time
        print('Simulation completed in %f seconds.' % end_time2)
        fig = plt.figure(figsize=(7, 5))
        ax = fig.add_subplot(111)
        plot_sir()
        plt.show()

    if animate:
        fig = plt.figure(figsize=(10, 5))
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        ani = FuncAnimation(fig, animation, interval=2)
        print('Animation showing.')
        plt.show()
