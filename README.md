# ASERSA Model Simulation

**ASERSA** (Agents’ Social Environment Rewarding System Algorithm) is an innovative agent-based socio-economic model simulation inspired by real-world socio-economic systems. ASERSA is designed as a versatile platform for simulating, testing, training, and interpreting agent behavior across various contexts. It integrates key socio-economic principles such as wealth distribution, influence, competence development, taxation, and redistribution policies to create a dynamic and responsive simulation environment.

This project allows you to explore and analyze how different parameters and policies affect the dynamics of a simulated socio-economic system, providing valuable insights into complex social interactions and economic mechanisms.

## Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Current Development Focus](#current-development-focus)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Option 1: Using pip](#option-1-using-pip)
  - [Option 2: Using Conda](#option-2-using-conda)
- [Running the Simulation](#running-the-simulation)
- [Customization and Experimentation](#customization-and-experimentation)
- [Data Analysis and Visualization](#data-analysis-and-visualization)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Common Issues and Troubleshooting](#common-issues-and-troubleshooting)

---

## Project Overview

ASERSA (Agents’ Social Environment Rewarding System Algorithm) is a comprehensive agent-based socio-economic model that simulates interactions among agents within a society. The model incorporates various socio-economic principles, including wealth distribution, influence, competence development, taxation, and redistribution policies.

The ASERSA model simulation provides a platform to:

- **Simulate** socio-economic interactions among agents over time.
- **Analyze** the effects of different parameters and policies on wealth distribution, agent performance, and system stability.
- **Visualize** the dynamics of the system through various plots and charts.
- **Experiment** with network effects and agent behaviors.

---

## Key Features

ASERSA boasts a range of innovative and versatile features designed to facilitate in-depth simulation and analysis of socio-economic systems:

1. **Dynamic Force Index Algorithm (DFIA):**
   - A lightweight and innovative algorithm that calculates agents' individual stats by considering the entire system of agents.
   - Provides real-time calculations of values interpreted as volume, influence, and force for each agent, enabling a dynamic and responsive simulation environment.

2. **Versatile Simulation Environment:**
   - Not limited to economic tasks; offers a flexible platform for testing and training agent-based systems.
   - Leverages the DFIA to manage and interpret agent behavior effectively across various contexts.

3. **Scalability:**
   - Performance-efficient, capable of handling simulations with 100 agents.
   - Potential to scale up to 1,000 or even 10,000 agents due to its lightweight design.

4. **Parameter Experiments:**
   - Users can adjust model parameters to observe different behaviors and outcomes.
   - Facilitates experimentation and discovery by allowing customization of economic factors, agent behaviors, and simulation settings.

5. **Network Effects:**
   - Agents interact and learn from their network neighbors.
   - Allows for the exploration of complex network dynamics and their impact on agent interactions.

6. **Policy Simulations:**
   - Supports testing different tax policies and redistribution mechanisms.
   - Provides insights into the impacts of various policies on wealth distribution and agent development.

7. **Advanced Analysis:**
   - Utilize data analysis techniques to explore patterns and trends within the simulation.
   - Includes calculations of metrics like the Gini coefficient to assess wealth inequality.

8. **User Interface:**
   - A PyQt5-based GUI allows for easy interaction and visualization of the simulation.
   - Accessible to users with varying levels of expertise, facilitating intuitive control and monitoring of the simulation.

9. **Extensibility:**
   - The modular code structure allows for easy customization and extension.
   - Enables users to tailor the simulation to their specific needs and incorporate new features seamlessly.

---

## Current Development Focus

The current phase of the ASERSA project is concentrated on interpreting the agent system's behavior with different kinds of tokens. This involves exploring how various token types influence agent interactions and system dynamics, further enhancing the simulation's versatility and applicability. Key areas of focus include:

- **Token Diversity:** Implementing multiple token types to represent different aspects of agent wealth and influence.
- **Behavioral Analysis:** Assessing how different tokens affect agent decision-making and interactions.
- **System Dynamics:** Understanding the interplay between various token types and their collective impact on the socio-economic environment.
- **Enhanced Visualization:** Developing more comprehensive visual tools to represent the complexities introduced by multiple token types.

---

## Project Structure

---

ASERSA/
├── analysis.py         # Code for data analysis and visualization
├── agent.py            # Defines the Agent class and agent behaviors
├── functions.py        # Definitions for calculations and relationships
├── gui.py              # PyQt5-based GUI for interacting with the simulation
├── license             # License information for the project
├── main.py             # Main script to run the simulation
├── network.py          # Handles the network effects between agents
├── parameters.py       # Defines all constants and parameters used in the model
├── policy.py           # Contains different tax and redistribution policies
├── README.md           # Project documentation
├── requirements.txt    # Python packages required for the project (for pip users)
└── environment.yml     # Specifies the Conda environment configuration

---

## Setup Instructions

You can set up the project using either `pip` or `conda` for package management. Choose the option that best suits your preferences.

### Prerequisites

- **Python 3.6 or higher** installed on your system.
- **Virtual environment tool** like `virtualenv` or `conda` (recommended) to manage project dependencies.

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
```

The `requirements.txt` file includes:

```plaintext
numpy
matplotlib
seaborn
networkx
PyQt5
pandas
```

These packages are necessary for numerical computations, data visualization, network operations, and GUI functionalities.

#### Step 4: Configure the Project (Optional)

- **Verify Parameters:** Open `parameters.py` and adjust parameters if needed.
- **Check File Paths:** Ensure all file paths in the code are correct and accessible.

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
  - PyQt5
  - pandas
```

This command will create an environment with the specified Python version and packages.

#### Step 4: Activate the Environment

Activate the newly created Conda environment:

```bash
conda activate asersa_env
```

#### Step 5: Configure the Project (Optional)

- **Verify Parameters:** Open `parameters.py` and adjust parameters if needed.
- **Check File Paths:** Ensure all file paths in the code are correct and accessible.

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

Upon running `main.py`, the simulation will execute over the predefined number of time steps. The GUI provides controls for starting, pausing, stopping, and stepping through the simulation. The console will display progress updates, and real-time visualizations will reflect the ongoing dynamics.

### Output Visualizations Include

- **Dynamic Force Index Algorithm (DFIA):** Real-time calculations of agents' volume, influence, and force.
- **Average Wealth Over Time:** Plot showing the evolution of average wealth across all agents.
- **Gini Coefficient Over Time:** Assess wealth inequality within the simulation.
- **Agent Status Dashboard:** Interactive table displaying individual agent metrics.
- **Network Visualization:** 3D representation of agent connections and interactions.

**Note:** Ensure that your Python environment supports graphical display. If you're running the script in a non-GUI environment (like a remote server), you may need to adjust the matplotlib backend or configure the script to save plots to files instead of displaying them.

---

## Customization and Experimentation

ASERSA is designed for flexibility and experimentation. You can customize various aspects of the simulation to explore different scenarios and gain deeper insights.

### Adjust Parameters

Modify values in `parameters.py` to experiment with different settings:

- **Economic Factors:** Change `E`, `TAU_MAX`, `OMEGA_W`, etc.
- **Agent Behavior:** Adjust learning rates (`K7`, `kappa_min`, `kappa_max`), ambition factors (`K6`), and more.
- **Simulation Settings:** Alter `NUM_AGENTS`, `NUM_TIMESTEPS`, `DELTA_W_CONSTANT` to simulate different population sizes or durations.

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

- **Progressive Taxation:** Implement a tax rate that increases with wealth.
- **Universal Basic Income (UBI):** Distribute collected taxes equally among all agents.

**Remember** to integrate these policies into `main.py` by replacing or adding to the existing functions.

### Extend Agent Behavior

Enhance the `Agent` class in `agent.py`:

- **Add New Attributes:** Introduce variables like trust, reputation, or risk tolerance.
- **Define New Methods:** Create functions for additional behaviors or interactions, such as trading, forming alliances, or competing for resources.

### Visualization

In `analysis.py`, customize existing plots or add new ones:

- **Time Series Plots:** Visualize the evolution of other variables over time.
- **Network Visualization:** Use `networkx` and `matplotlib` to visualize the agent network.
- **Correlation Analysis:** Plot scatter plots to explore relationships between variables.

---

## Data Analysis and Visualization

ASERSA collects comprehensive data on agents' wealth, influence, competence, and other attributes over time. You can analyze this data to:

- **Assess Wealth Inequality:** Use the Gini coefficient or Lorenz curves.
- **Identify Patterns:** Observe how different policies affect agent development.
- **Predict Trends:** Apply machine learning techniques to forecast future states.

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

**Solution:**

- Ensure your environment supports GUI operations.
- If running on a headless server, configure matplotlib to use a non-interactive backend (e.g., Agg) and save plots to files instead of displaying them.

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

The ASERSA model simulation provides a rich environment for exploring socio-economic dynamics within an agent-based framework. By adjusting parameters, experimenting with different policies, and analyzing the resulting data, you can gain insights into complex systems and the effects of various interventions.

Whether you're a researcher, student, or enthusiast, this project offers a platform for learning and discovery.

**Happy simulating!**

---

**Note:** Replace placeholders like `https://github.com/yourusername/asera-model-simulation.git` with your actual repository URL and `[Budd McCrackn]` with your actual name if different.
