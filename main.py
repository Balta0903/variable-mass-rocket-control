
"""
Variable Mass Rocket Control Simulation
Baltazar Villasol
This program simulates the vertical motion of a rocket with changing mass.
A PID-style controller adjusts the fuel mass flow rate to try to maintain
a target velocity. The rocket is affected by thrust, gravity, and drag.
"""
#imports
import numpy as np
import matplotlib.pyplot as plt
from fontTools.varLib.instancer import verticalMetricsKeptInSync

#Constants
mass = 500
mass_fuel = 400
initial_velocity = 100
initial_position = 0
initial_acceleration = 0
gravity = 9.81
drag_constant = 0.01 #Simplification of the non velocity terms in the drag equation
time_step = 0.01
time_final = 100
n_steps = int(time_final / time_step)
velocity_mass = 500/2
target_velocity = 60
max_mass_flowrate = 40
kp=1
kd=1
ki=0.05

#Variables
mass_flowrate = 10
integral = 0
derivative = 0
proportional = 0
controllers = integral + derivative + proportional
velocity_n = initial_velocity
acceleration_n = initial_acceleration
position_n = initial_position
drag_force = 0
error_n = target_velocity -initial_velocity
time_n = 0

#arrays:
velocity = np.zeros(n_steps)
error = np.zeros(n_steps)
time = np.zeros(n_steps)

acceleration = np.zeros(n_steps)
position = np.zeros(n_steps)

velocity[0] = initial_velocity
error[0] = target_velocity - velocity[0]
acceleration[0] = initial_acceleration
position[0] = initial_position

for n in range(n_steps):

    #Controller
    if n==0:
        derivative = 0
    else:
        derivative = kd * (error_n - error[n-1]) / time_step
    integral = ki * np.sum(error) * time_step
    proportional = error_n * kp
    controllers = integral + derivative + proportional
    #physical limitations stop the flow rate from being higher that a max and smaller than zero
    if controllers > max_mass_flowrate:
        mass_flowrate = max_mass_flowrate
    elif controllers < 0:
        mass_flowrate = 0

    else:
        mass_flowrate = controllers


    #Update mass
    if mass_fuel != 0:
        mass = mass - mass_flowrate * time_step
        mass_fuel = mass_fuel - mass_flowrate * time_step
    #This is done to make sure no more fuel mass than possible is consumed
    if mass_fuel <= 0:
        print(mass_fuel)
        mass_flowrate = - mass_fuel / time_step
        mass = mass - mass_fuel
        mass_fuel = 0
    #Update arrays
    if velocity_n >= 0:
        drag_force = drag_constant * velocity_n ** 2
    else:
        drag_force = - drag_constant * velocity_n ** 2
    acceleration[n] = ( - gravity * mass - drag_force + velocity_mass * mass_flowrate ) / mass
    velocity[n] = velocity_n + time_step * acceleration[n]
    error[n] = target_velocity - velocity[n]
    position[n] = position_n + time_step * velocity[n]

    #Get values for next time step
    acceleration_n = acceleration[n]
    velocity_n = velocity[n]
    position_n = position[n]
    error_n = error[n]
    time[n] = time_n + time_step
    time_n = time[n]


plt.plot(time, velocity)
plt.plot(time, error)
plt.title("Velocity Vs Time")
plt.show()
plt.plot(time, acceleration)
plt.title("Acceleration Vs Time")
plt.show()
plt.plot(time, position)
plt.title("Position Vs Time")
plt.show()