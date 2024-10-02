import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from functions import gini_coefficient
from parameters import NUM_TIMESTEPS, EXPORT_PLOTS_DIR
import os

def analyze_results(simulation):
    agents = simulation.get_agents()
    wealth_data = np.array([sum(agent.history['tokens'][-1].values()) for agent in agents])

    plt.figure(figsize=(10, 6))
    sns.histplot(wealth_data, kde=True, bins=20)
    plt.title('Wealth Distribution at Final Timestep')
    plt.xlabel('Total Tokens')
    plt.ylabel('Number of Agents')
    plt.tight_layout()
    plot_path = os.path.join(EXPORT_PLOTS_DIR, "wealth_distribution_final_timestep.png")
    plt.savefig(plot_path)
    plt.show()

    average_competence = simulation.avg_competence_history
    plt.figure(figsize=(10, 6))
    plt.plot(simulation.time_series, average_competence, label='Average Competence')
    plt.title('Average Competence Over Time')
    plt.xlabel('Time Step')
    plt.ylabel('Average Competence')
    plt.legend()
    plt.tight_layout()
    plot_path = os.path.join(EXPORT_PLOTS_DIR, "average_competence_over_time.png")
    plt.savefig(plot_path)
    plt.show()

    average_influence = np.mean([agent.history['I'] for agent in agents], axis=0)
    plt.figure(figsize=(10, 6))
    plt.plot(simulation.time_series, average_influence, label='Average Influence', color='orange')
    plt.title('Average Influence Over Time')
    plt.xlabel('Time Step')
    plt.ylabel('Average Influence')
    plt.legend()
    plt.tight_layout()
    plot_path = os.path.join(EXPORT_PLOTS_DIR, "average_influence_over_time.png")
    plt.savefig(plot_path)
    plt.show()

    gini_over_time = []
    for t in range(len(simulation.time_series)):
        wealth_at_t = [sum(agent.history['tokens'][t].values()) for agent in agents]
        gini = gini_coefficient(wealth_at_t)
        gini_over_time.append(gini)

    plt.figure(figsize=(10, 6))
    plt.plot(simulation.time_series, gini_over_time, label='Gini Coefficient', color='green')
    plt.title('Gini Coefficient Over Time')
    plt.xlabel('Time Step')
    plt.ylabel('Gini Coefficient')
    plt.legend()
    plt.tight_layout()
    plot_path = os.path.join(EXPORT_PLOTS_DIR, "gini_coefficient_over_time.png")
    plt.savefig(plot_path)
    plt.show()

