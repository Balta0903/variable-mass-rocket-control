# Variable Mass Rocket Control

This project simulates the vertical motion of a rocket with changing mass and a PID-style velocity controller. The controller adjusts the rocket's fuel mass flow rate in order to bring the rocket velocity toward a target velocity.

The goal of the project is to model a simplified rocket system where fuel is consumed over time, thrust depends on mass flow rate, and the rocket is affected by gravity and drag.

## Project Overview

A rocket is different from many basic dynamics problems because its mass changes during flight. As fuel is burned, the total mass of the rocket decreases. This means the acceleration of the rocket changes even if the thrust stays the same.

This simulation models:

* Variable rocket mass
* Fuel consumption
* Gravity
* Aerodynamic drag
* Thrust from mass flow rate
* PID-style velocity control
* Physical limits on fuel flow rate

The controller attempts to maintain a target velocity by increasing or decreasing the fuel mass flow rate.

## Control System

The control system compares the rocket's current velocity to the target velocity.

```text
error = target_velocity - current_velocity
```

The error is passed through a PID-style controller:

```text
controller_output = proportional + integral + derivative
```

The controller output is then used as the desired mass flow rate. Since a real rocket engine has physical limits, the mass flow rate is constrained between zero and a maximum value:

```text
0 <= mass_flowrate <= max_mass_flowrate
```

If the rocket is moving too slowly, the controller increases the mass flow rate to produce more thrust. If the rocket is moving too fast, the controller reduces the mass flow rate.

## Rocket Dynamics

The rocket acceleration is calculated using a simplified force balance:

```text
acceleration = (thrust - gravity_force - drag_force) / mass
```

In the simulation:

```text
gravity_force = mass * gravity
```

```text
drag_force = drag_constant * velocity^2
```

```text
thrust = velocity_mass * mass_flowrate
```

The velocity and position are updated using Euler integration:

```text
velocity_new = velocity_old + acceleration * time_step
```

```text
position_new = position_old + velocity_new * time_step
```

The rocket mass is updated as fuel is consumed:

```text
mass_new = mass_old - mass_flowrate * time_step
```

The simulation also prevents the rocket from consuming more fuel than is available.

## Main Parameters

| Variable            | Description                         |
| ------------------- | ----------------------------------- |
| `mass`              | Initial total rocket mass           |
| `mass_fuel`         | Initial fuel mass                   |
| `initial_velocity`  | Starting rocket velocity            |
| `initial_position`  | Starting rocket altitude            |
| `gravity`           | Gravitational acceleration          |
| `drag_constant`     | Simplified drag coefficient         |
| `time_step`         | Simulation time step                |
| `time_final`        | Total simulation time               |
| `target_velocity`   | Desired rocket velocity             |
| `max_mass_flowrate` | Maximum allowed fuel mass flow rate |
| `kp`                | Proportional controller gain        |
| `ki`                | Integral controller gain            |
| `kd`                | Derivative controller gain          |

## Simulation Outputs

The program generates plots for:

1. Velocity and velocity error over time
2. Acceleration over time
3. Position over time

These plots help show how well the controller is able to regulate the rocket velocity.

## How to Run

First, install the required Python libraries:

```bash
pip install numpy matplotlib
```

Then run the simulation:

```bash
python rocket_control.py
```

## Example Results

The simulation starts with an initial velocity of 100 m/s and a target velocity of 60 m/s. Since the rocket is initially moving faster than the target velocity, the controller reduces the mass flow rate. Gravity and drag slow the rocket down until the controller begins adjusting thrust to approach the target velocity.

The behavior of the system depends heavily on the PID gains:

```python
kp = 1
kd = 1
ki = 0.05
```

Changing these values affects overshoot, settling time, and how aggressively the controller responds.

## What I Learned

This project demonstrates how a PID controller can be applied to a variable-mass rocket system. It also shows the importance of physical constraints in control systems. The controller may request a mass flow rate, but the actual mass flow rate must stay within realistic engine limits and cannot exceed the remaining fuel.

This project also connects rocket dynamics to basic numerical simulation methods, including Euler integration and force-based acceleration modeling.

## File Structure

```text
rocket-velocity-pid-control/
│
├── rocket_control.py
├── README.md
└── plots/
```

## Project Status

This is the first version of the variable mass rocket control simulation. The current model is simplified, but it provides a strong foundation for exploring rocket dynamics and control systems.

