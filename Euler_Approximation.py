import numpy as np
import math
import matplotlib.pyplot as plt
import time

# Settings
time_interval = 0.01
number_of_cycles = int(input("Input number of desired cycles: "))

start_time = time.time()

# Constants
# G = 6.67408 * math.pow(10, -11)
# M = 1.989 * math.pow(10, 30)
G, M = 1, 1

# initial conditions
initial_x = 4
initial_y = 0
raw_initial_vx = 0
raw_initial_vy = 1.9
initial_r = math.sqrt(math.pow(initial_x,2) + math.pow(initial_y,2))  # sqrt(x^2+y+2)
initial_vx = raw_initial_vx - (time_interval/2)*(G * M * initial_x)/math.pow(initial_r,3)  # half of an interval ahead
initial_vy = raw_initial_vy - (time_interval/2)*(G * M * initial_y)/math.pow(initial_r,3)  # half of an interval ahead


# Defining Arrays
x_array = np.array([initial_x])
y_array = np.array([initial_y])
vx_array = np.array([initial_vx])
vy_array = np.array([initial_vy])
time_axis = np.linspace(0, (number_of_cycles-1)*time_interval, number_of_cycles)  # To be used for graphing


# Defining Functions


def position_next(p, v, t):
    n = p + t * v
    return n


def velocity_next(x, y, v, t):
    r = math.sqrt(math.pow(x,2) + math.pow(y,2))
    n = v -(G * M * x)/math.pow(r,3)
    return n


def last_value_of(array):
    length = len(array)
    return array[length-1]


# Calculations
calculation_count = 2
cycle_count = 1
while cycle_count <= number_of_cycles:
    x = position_next(last_value_of(x_array), last_value_of(vx_array), time_interval)
    y = position_next(last_value_of(y_array), last_value_of(vy_array), time_interval)
    x_array  = np.append(x_array, [x])
    y_array = np.append(y_array, [y])
    vx = velocity_next(x, y, last_value_of(vx_array), time_interval)
    vy = velocity_next(y, x, last_value_of(vy_array), time_interval)
    vx_array = np.append(vx_array, [vx])
    vy_array = np.append(vy_array, [vy])
    cycle_count+=1
    calculation_count+=4


# Test Area
print(calculation_count)
print(x_array)
print(y_array)

print("--- %s seconds ---" % (time.time() - start_time))


def my_plotter(ax, data1, data2, param_dict):
    """
    A helper function to make a graph

    Parameters
    ----------
    ax : Axes
        The axes to draw to

    data1 : array
       The x data

    data2 : array
       The y data

    param_dict : dict
       Dictionary of kwargs to pass to ax.plot

    Returns
    -------
    out : list
        list of artists added
    """
    out = ax.plot(data1, data2, 'k', **param_dict)
    return out


fig, ax = plt.subplots(1, 1)
my_plotter(ax, x_array, y_array, {'marker': ','})

ax.plot(0,0, marker='x')
plt.grid()
#plt.text(0,0,'Origin', weight='bold')

np.savetxt("x.csv", x_array, delimiter=",", fmt='%10.5f')
np.savetxt("y.csv", y_array, delimiter=",", fmt='%10.5f')

plt.show()


