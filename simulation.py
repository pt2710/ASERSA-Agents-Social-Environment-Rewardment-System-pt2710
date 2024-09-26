# simulation.py
import numpy as np
import networkx as nx
from agent import Agent
from parameters import *
from functions import redistribute_taxes, calculate_C_best, compute_action_level, gini_coefficient
import pickle
import csv
import pandas as pd  # We'll use pandas for easier data manipulation

class Simulation:
    def __init__(self):
        self.agents = []
        self.time_step = 0
        self.running = False
        self.network = None
        self.initialize_simulation()
        self.wealth_history = []
        self.time_series = []
        self.gini_history = []
        self.avg_competence_history = []
        self.agent_histories = {}  # To store individual agent histories

    def initialize_simulation(self):
        initial_wealths = np.random.uniform(W_MIN, W_MAX, NUM_AGENTS)
        self.agents = []
        for i in range(NUM_AGENTS):
            agent = Agent(agent_id=i, initial_wealth=initial_wealths[i])
            self.agents.append(agent)
            self.agent_histories[i] = {'W': [], 'I': [], 'AS': [], 'C': []}
        self.network = nx.erdos_renyi_graph(NUM_AGENTS, NETWORK_PROBABILITY)
    
    def start(self):
        self.running = True
    
    def pause(self):
        self.running = False
    
    def stop(self):
        self.running = False
        self.time_step = 0
        self.initialize_simulation()
        self.wealth_history.clear()
        self.time_series.clear()
        self.gini_history.clear()
        self.avg_competence_history.clear()
    
    def step(self):
        if not self.running:
            self.update()
    
    def update(self):
        if self.running:
            self.time_step += 1
            total_tax_collected = 0
            W_min = min(agent.W for agent in self.agents)
            W_max = max(agent.W for agent in self.agents)
            AS_max = max(agent.AS for agent in self.agents)
            Xn = len(self.agents)
            z = 100  # Total theoretical capacity (Zone)

            # Update agents' wealth and variables up to ambition
            for agent in self.agents:
                delta_W = DELTA_W_CONSTANT
                tax_paid = agent.update_state(delta_W, W_min, W_max, AS_max, E)
                total_tax_collected += tax_paid

            # Redistribute taxes
            redistribute_taxes(self.agents, total_tax_collected)

            # DFIA Calculations
            XnF = sum(agent.I for agent in self.agents)
            Xz = z / Xn  # Theoretical volume per agent

            for agent in self.agents:
                XrnF_X = XnF - agent.I
                agent.update_DFIA_values(XnF, Xn, Xz, XrnF_X)

            # Adjust influence based on DFIA
            for agent in self.agents:
                agent.adjust_influence_based_on_DFIA()

            # Update inspiration and competence
            for agent_id, agent in enumerate(self.agents):
                C_best = calculate_C_best(self.agents, self.network, agent_id)
                agent.update_inspiration(C_best)
                agent.update_competence(C_best)
                agent.AL = compute_action_level(agent.IN, agent.V, agent.A)
                agent.collect_data()
                # Store agent's history
                self.agent_histories[agent_id]['W'].append(agent.W)
                self.agent_histories[agent_id]['I'].append(agent.I)
                self.agent_histories[agent_id]['AS'].append(agent.AS)
                self.agent_histories[agent_id]['C'].append(agent.C)

            # Update rewards and weights
            for agent in self.agents:
                community_contribution = agent.tax_paid  # Assuming tax_paid is stored in agent
                delta_AS = agent.AS - agent.prev_AS
                agent.prev_AS = agent.AS
                agent.compute_reward(DELTA_W_CONSTANT, community_contribution, delta_AS)

            # Collect data
            avg_wealth = np.mean([agent.W for agent in self.agents])
            self.wealth_history.append(avg_wealth)
            self.time_series.append(self.time_step)
            avg_competence = np.mean([agent.C for agent in self.agents])
            self.avg_competence_history.append(avg_competence)
            # Compute Gini coefficient
            wealths = [agent.W for agent in self.agents]
            gini = gini_coefficient(wealths)
            self.gini_history.append(gini)

    def export_data(self, filename_prefix):
        """
        Exports simulation data to CSV files.
        - filename_prefix: A string prefix for the filenames.
        """
        # Export aggregate data
        aggregate_data = pd.DataFrame({
            'Time': self.time_series,
            'Average Wealth': self.wealth_history,
            'Gini Coefficient': self.gini_history,
            'Average Competence': self.avg_competence_history
        })
        aggregate_filename = f"{filename_prefix}_aggregate_data.csv"
        aggregate_data.to_csv(aggregate_filename, index=False)
        print(f"Aggregate data exported to {aggregate_filename}")

        # Export individual agent data
        # Create a multi-index DataFrame
        agent_data = []
        for agent_id, history in self.agent_histories.items():
            df = pd.DataFrame(history)
            df['Time'] = self.time_series
            df['Agent ID'] = agent_id
            agent_data.append(df)
        all_agents_data = pd.concat(agent_data)
        agent_filename = f"{filename_prefix}_agent_data.csv"
        all_agents_data.to_csv(agent_filename, index=False)
        print(f"Agent data exported to {agent_filename}")

        # Alternatively, save each agent's data to separate files (optional)
        # Uncomment the following code if desired
        """
        for agent_id, history in self.agent_histories.items():
            df = pd.DataFrame(history)
            df['Time'] = self.time_series
            agent_filename = f"{filename_prefix}_agent_{agent_id}_data.csv"
            df.to_csv(agent_filename, index=False)
            print(f"Agent {agent_id} data exported to {agent_filename}")
        """