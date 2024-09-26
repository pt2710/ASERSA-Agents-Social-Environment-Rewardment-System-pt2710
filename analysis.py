# analysis.py
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from functions import gini_coefficient
from parameters import NUM_TIMESTEPS

def analyze_results(agents):
    # Collect wealth data from all agents
    wealth_data = np.array([agent.history['W'] for agent in agents])

    # Plot wealth distribution at final timestep
    plt.figure(figsize=(10, 6))
    sns.histplot(wealth_data[:, -1], kde=True, bins=20)
    plt.title('Wealth Distribution at Final Timestep')
    plt.xlabel('Wealth')
    plt.ylabel('Number of Agents')
    plt.show()

    # Plot average competence over time
    average_competence = np.mean([agent.history['C'] for agent in agents], axis=0)
    plt.figure(figsize=(10, 6))
    plt.plot(range(NUM_TIMESTEPS), average_competence)
    plt.title('Average Competence Over Time')
    plt.xlabel('Time Step')
    plt.ylabel('Average Competence')
    plt.show()

    # Plot average influence over time
    average_influence = np.mean([agent.history['I'] for agent in agents], axis=0)
    plt.figure(figsize=(10, 6))
    plt.plot(range(NUM_TIMESTEPS), average_influence)
    plt.title('Average Influence Over Time')
    plt.xlabel('Time Step')
    plt.ylabel('Average Influence')
    plt.show()

    # Calculate Gini coefficient over time
    gini_over_time = []
    for t in range(NUM_TIMESTEPS):
        wealth_at_t = wealth_data[:, t]
        gini = gini_coefficient(wealth_at_t)
        gini_over_time.append(gini)

    # Plot Gini coefficient over time
    plt.figure(figsize=(10, 6))
    plt.plot(range(NUM_TIMESTEPS), gini_over_time)
    plt.title('Gini Coefficient Over Time')
    plt.xlabel('Time Step')
    plt.ylabel('Gini Coefficient')
    plt.show()
