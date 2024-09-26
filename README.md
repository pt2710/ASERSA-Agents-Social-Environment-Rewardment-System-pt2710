# ASERSA Model Simulation

**ASERSA** (Agents’ Social Environment Rewarding System Algorithm) is a comprehensive agent-based socio-economic model that simulates interactions among agents within a society. The model incorporates various socio-economic principles, including wealth distribution, influence, competence development, taxation, and redistribution policies.

This project allows you to explore and analyze how different parameters and policies affect the dynamics of a simulated socio-economic system.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Option 1: Using pip](#option-1-using-pip)
  - [Option 2: Using Conda](#option-2-using-conda)
- [Running the Simulation](#running-the-simulation)
- [Customizing the Simulation](#customizing-the-simulation)
- [Data Analysis and Visualization](#data-analysis-and-visualization)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Common Issues and Troubleshooting](#common-issues-and-troubleshooting)

---

## Project Overview

The ASERSA model simulation provides a platform to:

- **Simulate** socio-economic interactions among agents over time.
- **Analyze** the effects of different parameters and policies on wealth distribution, agent performance, and system stability.
- **Visualize** the dynamics of the system through various plots and charts.
- **Experiment** with network effects and agent behaviors.

---

## Features

- **Parameter Experiments**: Adjust model parameters to observe different behaviors and outcomes.
- **Network Effects**: Agents interact and learn from their network neighbors.
- **Policy Simulations**: Test different tax policies and redistribution mechanisms.
- **Advanced Analysis**: Utilize data analysis techniques to explore patterns and trends.
- **User Interface Considerations**: Structured to be easily extended for GUI applications.
- **Extensibility**: Modular code structure allows for easy customization and extension.

---

## Project Structure

- `main.py` - Main script to run the simulation.
- `agent.py` - Defines the `Agent` class and agent behaviors.
- `functions.py` - Contains function definitions for calculations and relationships.
- `parameters.py` - Defines all constants and parameters used in the model.
- `network.py` - Handles the network effects between agents.
- `policy.py` - Contains different tax and redistribution policies.
- `analysis.py` - Code for data analysis and visualization.
- `README.md` - Project documentation.
- `requirements.txt` - Lists Python packages required for the project (for `pip` users).
- `environment.yml` - Specifies the Conda environment configuration (for `conda` users).
- `LICENSE` - License information for the project.

---

## Setup Instructions

You can set up the project using either `pip` or `conda` for package management. Choose the option that best suits your preferences.

### Prerequisites

- Python 3.6 or higher installed on your system.
- (Optional but recommended) Virtual environment tool like `virtualenv` or `conda` to manage project dependencies.

### Option 1: Using pip

#### Step 1: Clone or Download the Project

Clone the repository or download the project files to your local machine.

```bash
git clone https://github.com/yourusername/asera-model-simulation.git
```

#### Step 2: Create a Virtual Environment (Recommended)

Creating a virtual environment helps manage project-specific dependencies.

Using `virtualenv`:

```bash
# Install virtualenv if you haven't already
pip install virtualenv

# Create a virtual environment named 'venv'
virtualenv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

#### Step 3: Install Required Libraries

Install the required Python packages using `pip` and the `requirements.txt` file.

```bash
pip install -r requirements.txt

The `requirements.txt` file includes:

language=python
numpy
matplotlib
seaborn
networkx
```

These packages are necessary for numerical computations, data visualization, and network operations.

#### Step 4: Configure the Project (Optional)

- **Verify Parameters**: Open `parameters.py` and adjust parameters if needed.
- **Check File Paths**: Ensure all file paths in the code are correct and accessible.

#### Step 5: Run the Simulation

Execute the `main.py` script to start the simulation.

```bash
python main.py
```

#### Step 6: Deactivate the Virtual Environment (Optional)

After you're done, you can deactivate the virtual environment:

```bash
deactivate
```

### Option 2: Using Conda

#### Step 1: Install Anaconda or Miniconda

If you haven't already, download and install [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) from their official websites.

#### Step 2: Clone or Download the Project

Clone the repository or download the project files to your local machine.

```bash
git clone https://github.com/yourusername/asera-model-simulation.git
```

#### Step 3: Create a New Conda Environment

Use the provided `environment.yml` file to create a new Conda environment named `asera_env`.

```bash
conda env create -f environment.yml
```

The `environment.yml` file includes:

```yaml
name: asersa_env
channels:
  - defaults
dependencies:
  - python=3.8
  - numpy
  - matplotlib
  - seaborn
  - networkx
```

This command will create an environment with the specified Python version and packages.

#### Step 4: Activate the Environment

Activate the newly created Conda environment:

```bash
conda activate asersa_env
```

#### Step 5: Configure the Project (Optional)

- **Verify Parameters**: Open `parameters.py` and adjust parameters if needed.
- **Check File Paths**: Ensure all file paths in the code are correct and accessible.

#### Step 6: Run the Simulation

Navigate to the project directory and execute the `main.py` script:

```bash
python main.py
```

#### Step 7: Deactivate the Environment (Optional)

After you're done, you can deactivate the Conda environment:

```bash
conda deactivate
```

---

## Running the Simulation

Upon running `main.py`, the simulation will execute over the predefined number of time steps. The console will display progress updates, and at the end of the simulation, several plots will be generated to visualize the results.

### Output Plots Include

- **Wealth Distribution** at the final time step.
- **Average Competence Over Time**.
- **Average Influence Over Time**.
- **Gini Coefficient Over Time** to assess wealth inequality.

**Note:** Ensure that your Python environment supports graphical display. If you're running the script in a non-GUI environment (like a remote server), you may need to adjust the matplotlib backend or configure the script to save plots to files instead of displaying them.

---

## Customizing the Simulation

### Adjust Parameters

Modify values in `parameters.py` to experiment with different scenarios:

- **Economic Factors**: Change `E`, `TAU_MAX`, `OMEGA_W`, etc.
- **Agent Behavior**: Adjust learning rates (`K7`, `kappa_min`, `kappa_max`), ambition factors (`K6`), and more.
- **Simulation Settings**: Alter `NUM_AGENTS`, `NUM_TIMESTEPS`, `DELTA_W_CONSTANT` to simulate different population sizes or durations.

### Change Network Structure

In `network.py`, you can modify the network creation function to use different network models:

- **Scale-Free Network:**

    ```python
    import networkx as nx

    def create_agent_network():
        G = nx.barabasi_albert_graph(n=NUM_AGENTS, m=2)
        return G
    ```

- **Small-World Network:**

    ```python
    import networkx as nx

    def create_agent_network():
        G = nx.watts_strogatz_graph(n=NUM_AGENTS, k=4, p=0.1)
        return G
    ```

### Implement New Policies

In `policy.py`, you can add new taxation or redistribution policies:

- **Progressive Taxation**: Implement a tax rate that increases with wealth.
- **Universal Basic Income (UBI)**: Distribute collected taxes equally among all agents.

**Remember** to integrate these policies into `main.py` by replacing or adding to the existing functions.

### Extend Agent Behavior

Enhance the `Agent` class in `agent.py`:

- **Add New Attributes**: Introduce variables like trust, reputation, or risk tolerance.
- **Define New Methods**: Create functions for additional behaviors or interactions, such as trading, forming alliances, or competing for resources.

### Visualization

In `analysis.py`, customize existing plots or add new ones:

- **Time Series Plots**: Visualize the evolution of other variables over time.
- **Network Visualization**: Use `networkx` and `matplotlib` to visualize the agent network.
- **Correlation Analysis**: Plot scatter plots to explore relationships between variables.

---

## Data Analysis and Visualization

The simulation collects data on agents' wealth, influence, competence, and other attributes over time. You can analyze this data to:

- **Assess Wealth Inequality**: Use the Gini coefficient or Lorenz curves.
- **Identify Patterns**: Observe how different policies affect agent development.
- **Predict Trends**: Apply machine learning techniques to forecast future states.

Feel free to extend `analysis.py` with additional analyses or integrate tools like `pandas` for data manipulation.

---

## Contributing

Contributions are welcome! If you have ideas for improvements, new features, or bug fixes, please follow these steps:

1. **Fork the Repository**.
2. **Create a New Branch** for your feature or fix.
3. **Commit Your Changes** with descriptive messages.
4. **Submit a Pull Request** with a detailed description of your changes.

---

## License

### Pending License

© **[Budd McCrackn]** **[2024]**. All rights reserved.

This project is currently under development, and all rights are reserved by **[Budd McCrackn]**. The software, including its underlying mathematics and conceptual ideas, is the sole property of the author. No part of this project may be reproduced, distributed, or transmitted in any form or by any means without the prior written permission of the author.

**Planned Open Source Licensing:** Upon completion and readiness for public release, this project will be made available under an open-source license. Please check back later for updates.

---

## Contact

For questions, suggestions, or collaboration opportunities, please contact:

**[Budd McCrackn]**  
Email: [ptxboxone@gmail.com](mailto:ptxboxone@gmail.com)  
GitHub: [@pt2710](https://github.com/pt2710)

---

## Common Issues and Troubleshooting

### ModuleNotFoundError

**Issue:** Encountered when a required module is not found.

**Solution:** Ensure all required packages are installed in your current environment. Activate your virtual or Conda environment before running the script.

### Environment Activation

**Issue:** Commands not recognized, or incorrect Python version/package used.

**Solution:** Activate the appropriate virtual environment or Conda environment before running the simulation.

### Permission Errors

**Issue:** Permission denied when installing packages.

**Solution:** Use a virtual environment or Conda environment to avoid needing administrative privileges.

### Plot Display Issues

**Issue:** Plots do not display, or an error occurs when generating plots.

**Solution:

- Ensure your environment supports GUI operations.
- If running on a headless server, configure matplotlib to use a non-interactive backend (e.g., Agg) and save plots to files.

    ```python
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt

    # After each plot
    plt.savefig('plot_name.png')
    ```

### Slow Performance

**Issue:**

- Simulation runs slowly with a large number of agents or time steps.

**Solution:**

- Optimize code where possible (e.g., avoid unnecessary computations).
- Reduce the number of agents or time steps for testing purposes.
- Consider using more efficient data structures or parallel processing if necessary.

---

## Summary

The ASERA model simulation provides a rich environment for exploring socio-economic dynamics within an agent-based framework. By adjusting parameters, experimenting with different policies, and analyzing the resulting data, you can gain insights into complex systems and the effects of various interventions.

Whether you're a researcher, student, or enthusiast, this project offers a platform for learning and discovery.

**Happy simulating!**
