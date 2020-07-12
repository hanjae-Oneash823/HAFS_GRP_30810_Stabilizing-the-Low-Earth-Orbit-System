import numpy as np
import math
import matplotlib.pyplot as plt

# Settings
h = 0.1
number_of_cycles = int(input("Input number of desired cycles: "))

# Constants
G = 6.67408 * math.pow(10, -11)
M = 1.989 * math.pow(10, 30)

# initial conditions
x_i = 0.0
y_i = 385000000.0
z_i = 0.0
vx_i = 1022.0
vy_i = 0.0
vz_i = 0.0

# Formula
s = math.sqrt(G*M/y_i)
print(s)

# Defining Arrays
X = np.array([x_i])
Y = np.array([y_i])
Z = np.array([z_i])
VX = np.array([vx_i])
VY = np.array([vy_i])
VZ = np.array([vz_i])
time_axis = np.linspace(0, (number_of_cycles-1)*h, number_of_cycles)  # To be used for graphing


# Defining Functions
def r(a, b, c):
    # returns magnitude of position vector (a,b,c)
    return math.sqrt(math.pow(a, 2) + math.pow(b, 2) + math.pow(c, 2))


def f2(pos, dis):
    # returns functions 2 as specified in paper
    return ((-1.0)*G*M*pos)/math.pow(dis, 3)


def lvo(array):
    # returns last value of given array
    length = len(array)
    return array[length-1]


# Calculations
calculation_count = 0
cycle_count = 1
while cycle_count <= number_of_cycles:
    # Stage 1
    r1 = r(lvo(X), lvo(Y), lvo(Z))
    k_1x = lvo(VX)
    k_1y = lvo(VY)
    k_1z = lvo(VZ)
    k_1vx = f2(lvo(X), r1)
    k_1vy = f2(lvo(Y), r1)
    k_1vz = f2(lvo(Z), r1)

    # Stage 2
    r2 = r(lvo(X)+0.5*h*k_1x, lvo(Y)+0.5*h*k_1y, lvo(Z)+0.5*h*k_1z)
    k_2x = lvo(VX)+0.5*h*k_1vx
    k_2y = lvo(VY)+0.5*h*k_1vy
    k_2z = lvo(VZ)+0.5*h*k_1vz
    k_2vx = f2(lvo(X)+0.5*h*k_1x, r2)
    k_2vy = f2(lvo(Y)+0.5*h*k_1y, r2)
    k_2vz = f2(lvo(Z)+0.5*h*k_1z, r2)

    # Stage 3
    r3 = r(lvo(X)+0.5*h*k_2x, lvo(Y)+0.5*h*k_2y, lvo(Z)+0.5*h*k_2z)
    k_3x = lvo(VX)+0.5*h*k_2vx
    k_3y = lvo(VY)+0.5*h*k_2vy
    k_3z = lvo(VZ)+0.5*h*k_2vz
    k_3vx = f2(lvo(X)+0.5*h*k_2x, r3)
    k_3vy = f2(lvo(Y)+0.5*h*k_2y, r3)
    k_3vz = f2(lvo(Z)+0.5*h*k_2z, r3)

    # Stage 4
    r4 = r(lvo(X)+h*k_3x, lvo(Y)+h*k_3y, lvo(Z)+h*k_3z)
    k_4x = lvo(VX)+h*k_3vx
    k_4y = lvo(VY)+h*k_3vy
    k_4z = lvo(VZ)+h*k_3vz
    k_4vx = f2(lvo(X)+h*k_3x, r4)
    k_4vy = f2(lvo(Y)+h*k_3y, r4)
    k_4vz = f2(lvo(Z)+h*k_3z, r4)

    # Phi
    phi_x = k_1x + 2*k_2x + 2*k_3x + k_4x
    phi_y = k_1y + 2*k_2y + 2*k_3y + k_4y
    phi_z = k_1z + 2*k_2z + 2*k_3z + k_4z
    phi_vx = k_1vx + 2*k_2vx + 2*k_3vx + k_4vx
    phi_vy = k_1vy + 2*k_2vy + 2*k_3vy + k_4vy
    phi_vz = k_1vz + 2*k_2vz + 2*k_3vz + k_4vz

    # Next Value
    n_x = lvo(X) + h*phi_x/6
    n_y = lvo(Y) + h*phi_y/6
    n_z = lvo(Z) + h*phi_z/6
    n_vx = lvo(VX) + h*phi_vx/6
    n_vy = lvo(VY) + h*phi_vy/6
    n_vz = lvo(VZ) + h*phi_vz/6

    # Append
    X = np.append(X, [n_x])
    Y = np.append(Y, [n_y])
    Z = np.append(Z, [n_z])
    VX = np.append(VX, [n_vx])
    VY = np.append(VY, [n_vy])
    VZ = np.append(VZ, [n_vz])

    # Counting
    cycle_count += 1
    calculation_count += 4


# Test Area
print(calculation_count)
print(X)
print(Y)
print(Z)

# np.savetxt("x.csv", x_array, delimiter=",", fmt='%10.5f')
# np.savetxt("y.csv", y_array, delimiter=",", fmt='%10.5f')


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(X, Y, Z, c='b', marker='o')
ax.scatter(0, 0, 0, c='k', marker='x')
ax.scatter(lvo(X), lvo(Y), lvo(Z), c='g', marker='x')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
"""
ax.set_xlim(-7000, 7000)
ax.set_ylim(-7000, 7000)
ax.set_zlim(-7000, 7000)
"""
ax.text(0, 0, 0, 'Origin', None)

plt.title('Moon Orbit Test: r('+str(x_i)+', '+str(y_i)+', '+str(z_i)+'), v('+str(vx_i)+', '+str(vy_i)+', '+str(vz_i)+')')
plt.show()
