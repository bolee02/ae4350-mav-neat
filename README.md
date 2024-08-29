# NEAT MAVs

This project is a simulation of autonomous drones navigating through obstacles, using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm to evolve their neural networks. The simulation is built using Pygame and NEAT-Python, with visualizations provided by Matplotlib.

## Overview

The project simulates a "CyberZoo," where multiple drones navigate through a field of poles. The NEAT algorithm is employed to evolve the control strategies for these drones over generations, aiming to maximize the distance traveled without collisions.

### Key Features:
- **Drone Navigation:** Drones start at a fixed position and move around the screen, avoiding poles.
- **Dynamic Environment:** Poles periodically change their positions, increasing the challenge for the drones.
- **Fitness Evaluation:** Drones are rewarded based on the distance they travel before colliding with poles or the screen boundary.
- **NEAT Integration:** The neural networks controlling the drones are evolved using NEAT, with fitness evaluated over generations.
- **Visualization:** Fitness evolution across generations is visualized with Matplotlib.

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

   The script will run multiple configurations of the NEAT algorithm. After each run, it will display the evolution of the best and mean fitness across generations using Matplotlib.

### Code Structure

- `CyberZooSim`: The main simulation class that initializes the game environment, handles the logic for drones and poles, and evaluates fitness.
- `Drone`: A class representing the drones, including their movement and collision detection.
- `Pole`: A class representing the obstacles the drones must avoid.
- `run(config_path)`: The main function to run the NEAT algorithm with a given configuration.
- `eval_genomes(genomes, config)`: Evaluates the fitness of each genome in the population by running the simulation.

### Visualization

The results of the NEAT algorithm are visualized using Matplotlib with two subplots:
- **Best Fitness Over Generations:** Tracks the highest fitness achieved by any genome in each generation.
- **Mean Fitness Over Generations:** Tracks the average fitness of all genomes in each generation.

## References and Resources

- [NEAT Python repository](https://neat-python.readthedocs.io/)
- [Original paper on NEAT](https://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf)
- [NEAT applied to games example 1](https://arxiv.org/pdf/2207.14140)
- [NEAT applied to games example 2](https://arxiv.org/pdf/2208.13632)
- [MAV Lab repository](https://github.com/MAV-Lab23)
- [PyTorch NEAT](https://github.com/uber-research/PyTorch-NEAT)

This project is inspired by the research and resources provided by the MAV Lab and the broader NEAT and AI community.

---

This README provides a clear overview of the project, how to get started, and additional resources for further exploration.
