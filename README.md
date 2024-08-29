# NEAT MAVs

This project is part of the course "AE4350: Bio-Inspired Intelligence and Learning" at Delft University of Technology. It is a simulation of autonomous drones navigating through obstacles, using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm to evolve their neural networks. The simulation is built using Pygame and NEAT-Python, with visualizations provided by Matplotlib.

## Overview

The project simulates a "CyberZoo," where multiple drones navigate through a field of poles. The NEAT algorithm is employed to evolve the control strategies for these drones over generations, aiming to maximize the distance traveled without collisions.

## Getting Started

### Prerequisites

Before running the simulation, make sure you have the following dependencies installed:

- Python 3.12
- Pygame 2.6.0
- Numpy 2.0.0
- Matplotlib 3.9.1
- NEAT-Python 0.92

You can install the required packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Running the Simulation

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd cyberzoo-simulation
   ```

2. **Run the Simulation:**
   Execute the main script to start the simulation:
   ```bash
   python main.py
   ```

## References and Resources

- [NEAT Python repository](https://neat-python.readthedocs.io/)
- [Original paper on NEAT](https://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf)
- [NEAT applied to games example 1](https://arxiv.org/pdf/2207.14140)
- [NEAT applied to games example 2](https://arxiv.org/pdf/2208.13632)
- [MAV Lab repository](https://github.com/MAV-Lab23)
- [PyTorch NEAT](https://github.com/uber-research/PyTorch-NEAT)
