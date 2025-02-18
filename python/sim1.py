from dot import Dots
from time import time
from time import sleep
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def do_step():    # settings for simulation
    D.move()
    D.infect()
    D.update_infection_time()
    D.update_sir()
    D.step += 1


def animate_sir():
    # Add sir data
    # Plot data in animation
    t.append(D.step / steps_per_day)
    s_count.append(D.susceptible)
    i_count.append(D.infected)
    r_count.append(D.removed)
    ax1.cla()
    ax1.set_ylabel('Count')
    ax1.set_xlabel('Day')
    title = 'SIR plot (r=%.1f, p=%.2f, d=%f)' % (rad, prob, duration)
    ax1.set_title(title)
    ax1.stackplot(t, i_count, s_count, r_count, colors=['red', 'green', 'grey'])


def animate_dots():
    # Clear all coordinates for 3 states
    x0.clear()
    y0.clear()
    x1.clear()
    y1.clear()
    x2.clear()
    y2.clear()
    # Append coordinates to 3 bins
    for k in range(D.N):
        if D.state[k] == 2:
            x2.append(D.x[k])
            y2.append(D.y[k])
        if D.state[k] == 1:
            x1.append(D.x[k])
            y1.append(D.y[k])
        if D.state[k] == 0:
            x0.append(D.x[k])
            y0.append(D.y[k])
    # Output frame
    ax2.cla()
    ax2.set_xlim([0, 30])
    ax2.set_ylim([0, 30])
    ax2.set_xticks([])
    ax2.set_yticks([])
    if D.removed > 0:
        ax2.scatter(x2, y2, c='grey', label='removed')
    if D.infected > 0:
        ax2.scatter(x1, y1, c='red', label='infected')
    if D.susceptible > 0:
        ax2.scatter(x0, y0, c='green', label='susceptible')


def animation(i):
    # do a step
    do_step()
    # plot data onto both graphs
    animate_dots()
    animate_sir()
    # check for termination
    if D.infected == 0:
        ani.event_source.stop()
        end_time1 = time() - start_time
        print('Simulation completed in %f seconds.' % end_time1)

def sim_sir_data():
    while True:
        print(D.step)
        # do steps for a day
        for _ in range(steps_per_day):
            do_step()
        # output data
        t.append(D.step / steps_per_day)
        s_count.append(D.susceptible)
        i_count.append(D.infected)
        r_count.append(D.removed)
        if D.infected == 0:
            break


mode = input('1 = animate: ')
if mode == '1':
    animate = True
else:
    animate = False

last_input = []     # create list to store last input for restart
while True:
    steps_per_day = 5
    x0, y0 = [], []
    x1, y1 = [], []
    x2, y2 = [], []
    # set sir initial values
    t = [0]
    s_count = [900]
    i_count = [0]
    r_count = [0]
    # take input
    input_string = input("Enter 3 parameters r, p, d: ")
    # check for restart
    if input_string == 're':
        if not last_input:
            print('No input yet.')
            continue
        else:
            rad, prob, duration = last_input
            print('Restart simulation.')
    else:
        rpd = input_string.split()
        rad, prob, duration = float(rpd[0]), float(rpd[1]), float(rpd[2])
        last_input = [rad, prob, duration]
    sleep(1)
    start_time = time()         # record starting time
    D = Dots()                  # create dots
    D.inf_rad_sqr = float(rad) * float(rad)
    D.inf_prob = float(prob) / steps_per_day
    D.inf_duration = float(duration) * steps_per_day
    D.infect_center()           # infect center one

    if not animate:
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111)
        sim_sir_data()
        end_time2 = time() - start_time
        print('Simulation completed in %f seconds.' % end_time2)
        ax.cla()
        ax.set_ylabel('Count')
        ax.set_xlabel('Day')
        title = 'SIR plot (r=%.1f, p=%.2f, d=%f)' % (rad, prob, duration)
        ax.set_title(title)
        ax.stackplot(t, i_count, s_count, r_count, colors=['red', 'green', 'grey'])
        plt.show()

    if animate:
        fig = plt.figure(figsize=(10, 5))
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        ani = FuncAnimation(fig, animation, interval=2)
        print('Animation showing.')
        plt.show()
