from dot_np_array import Dots
from time import time
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def do_step():    # settings for simulation
    D.move()
    D.infect()
    D.update_infection_time()

def sim_sir_data():
    while True:
        print(D.step)
        # do steps for a day
        for _ in range(steps_per_day):
            do_step()
        # output data
        D.append_sir_data()
        if D.infected[-1] == 0:
            break

def plot_sir():
    ax.cla()
    ax.set_ylabel('Count')
    ax.set_xlabel('Day')
    title = 'SIR plot (r=%.1f, p=%.2f, d=%d)' % (rad, prob, duration)
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
    ax2.set_xlim([0, D.box_size])
    ax2.set_ylim([0, D.box_size])
    ax2.set_xticks([])
    ax2.set_yticks([])
    state = np.zeros(D.N, dtype=int)
    state[D.state_1] = 1
    state[D.state_2] = 2
    ax2.scatter(np.array(D.x), np.array(D.y),c=color_map[state])
    ax2.scatter(np.array(D.x), np.array(D.y),c=color_map[state])
    ax2.scatter(np.array(D.x), np.array(D.y),c=color_map[state])


def animation(i):
    # do a step
    do_step()
    # plot data onto both graphs
    animate_dots()
    if i % 20 == 0:
        fig.savefig('frame'+str(i)+'.png')
    # animate_sir()
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
    steps_per_day = 5
    # take input
    input_string = input("Enter 3 parameters r, p, d: ")
    # check for restart
    if not input_string:
        if not last_input:
            print('No input yet.')
            continue
        else:
            rad, prob, duration = last_input
            print('Restart simulation.')
    else:
        rpd = input_string.split()
        rad, prob, duration = float(rpd[0]), float(rpd[1]), int(rpd[2])
        last_input = [rad, prob, duration]

    sleep(1)
    start_time = time()         # record starting time

    D = Dots()                  # create dots
    D.inf_rad_sqr = rad * rad
    D.inf_prob = prob / steps_per_day
    D.inf_duration = duration * steps_per_day

    if not animate:

        sim_sir_data()

        end_time2 = time() - start_time
        print('Simulation completed in %f seconds.' % end_time2)
        fig = plt.figure(figsize=(7, 5))
        ax = fig.add_subplot(111)
        plot_sir()
        plt.show()

    if animate:
        sleep(1)
        i = 0
        while D.state_1:
            # ani = FuncAnimation(fig, animation, interval=10, save_count=200)
            do_step()
            if i % 20 == 0:
                fig = plt.figure(figsize=(5, 5))
                # ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot()
                animate_dots()
                plt.show()
            i += 1
        print('Animation showing.')
