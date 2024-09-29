# simulation.py
import numpy as np
import networkx as nx
from agent import Agent
from parameters import *
from functions import compute_DFIA, redistribute_taxes, calculate_C_best, compute_action_level, gini_coefficient
import pickle
import csv
import pandas as pd  # We'll use pandas for easier data manipulation

class Simulation:
    def __init__(self):
        self.agents = []
        self.time_step = 0
        self.running = False
        self.network = None
        self.agent_histories = {}  # Initialize agent_histories here
        self.initialize_simulation()
        self.wealth_history = []
        self.time_series = []
        self.gini_history = []
        self.avg_competence_history = []

    def initialize_simulation(self):
        initial_wealths = np.random.uniform(W_MIN, W_MAX, NUM_AGENTS)
        self.agents = []
        for i in range(NUM_AGENTS):
            agent = Agent(agent_id=i, initial_wealth=initial_wealths[i])
            self.agents.append(agent)
            self.agent_histories[i] = {'W': [], 'I': [], 'AS': [], 'C': [], 'Xz': [], 'Xzo': []}
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
            compute_DFIA(self.agents, z)

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
                self.agent_histories[agent_id]['Xz'].append(agent.Xz)
                self.agent_histories[agent_id]['Xzo'].append(agent.Xzo)

            # Update rewards and weights
            for agent in self.agents:
                community_contribution = agent.tax_paid
                delta_AS = agent.AS - agent.prev_AS
                agent.prev_AS = agent.AS
                agent.compute_reward(DELTA_W_CONSTANT, community_contribution, delta_AS)

            # Collect aggregate data
            avg_wealth = np.mean([agent.W for agent in self.agents])
            self.wealth_history.append(avg_wealth)
            self.time_series.append(self.time_step)
            avg_competence = np.mean([agent.C for agent in self.agents])
            self.avg_competence_history.append(avg_competence)
            # Compute Gini coefficient
            wealths = [agent.W for agent in self.agents]
            gini = gini_coefficient(wealths)
            self.gini_history.append(gini)

            # Logging for debugging
            print(f"Time Step {self.time_step}:")
            print(f"  Average Wealth: {avg_wealth}")
            print(f"  Gini Coefficient: {gini}")
            print(f"  Average Competence: {avg_competence}")
            print(f"  Agents' Wealth: {[agent.W for agent in self.agents]}")

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
        print("Exporting Aggregate Data:")
        print(aggregate_data.head())
        aggregate_filename = f"{filename_prefix}_aggregate_data.csv"
        aggregate_data.to_csv(aggregate_filename, index=False)
        print(f"Aggregate data exported to {aggregate_filename} with {len(aggregate_data)} rows.")

        # Export individual agent data
        # Create a multi-index DataFrame
        agent_data = []
        for agent_id, history in self.agent_histories.items():
            df = pd.DataFrame(history)
            df['Time'] = self.time_series
            df['Agent ID'] = agent_id
            agent_data.append(df)
        if agent_data:
            all_agents_data = pd.concat(agent_data)
            print("Exporting Agent Data:")
            print(all_agents_data.head())
            agent_filename = f"{filename_prefix}_agent_data.csv"
            all_agents_data.to_csv(agent_filename, index=False)
            print(f"Agent data exported to {agent_filename} with {len(all_agents_data)} rows.")
        else:
            print("No agent data to export.")
    def get_agents(self):
        return self.agents
    
    def get_average_wealth(self):
        return np.mean([agent.W for agent in self.agents])
    
    def get_gini_coefficient(self):
        wealths = [agent.W for agent in self.agents]
        return gini_coefficient(wealths)
    
    def get_average_competence(self):
        return np.mean([agent.C for agent in self.agents])
    
    def get_time_series(self):
        return self.time_series
    
    def get_wealth_time_series(self):
        return self.wealth_history
    
    def get_network(self):
        return self.network
    
    def get_agent_by_id(self, agent_id):
        return next((a for a in self.agents if a.agent_id == agent_id), None)
    
    def adjust_parameter(self, value):
        for agent in self.agents:
            agent.some_property = value