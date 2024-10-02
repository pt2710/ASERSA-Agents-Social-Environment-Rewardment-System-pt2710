import os
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import pandas as pd
import numpy as np
import pickle
from agent import *
from network import create_agent_network
from parameters import *
from functions import *
from policy import apply_tax_policy

class Simulation:
    def __init__(self, agent_id):
        self.agents = []
        self.agent_id = agent_id
        self.time_step = 0
        self.running = False
        self.agent_histories = {}
        self.network = None
        self.initialize_simulation()
        self.wealth_history = []
        self.time_series = []
        self.gini_history = []
        self.avg_competence_history = []
        self.current_policy = 'flat'
        self.FLAT_TAX_RATE = 0.2
        self.total_tax_collected = 0
        self.ASPREV = 0
    
    def initialize_simulation(self):
        initial_tokens = {
            'type 1': np.random.uniform(W_MIN, W_MAX, NUM_AGENTS),
            'type 2': np.random.uniform(W_MIN, W_MAX, NUM_AGENTS),
        }
        for i in range(NUM_AGENTS):
            self.tokens = {k: initial_tokens[k][i] for k in initial_tokens}
            agent = Agent(
                agent_id=i,
                initial_tokens=self.tokens,
                delta_tokens=DELTA_W_CONSTANT
            )
            self.agents.append(agent)

    def start(self):
        self.running = True
        logging.info("Simulation started.")

    def pause(self):
        self.running = False
        logging.info("Simulation paused.")

    def stop(self):
        self.running = False
        self.time_step = 0
        self.initialize_simulation()
        self.wealth_history.clear()
        self.time_series.clear()
        self.gini_history.clear()
        self.avg_competence_history.clear()
        logging.info("Simulation stopped and reset.")

    def step(self):
        if not self.running:
            self.update()

    def update(self):
        if self.running:
            self.time_step += 1
            self.total_tax_collected = {k: 0 for k in self.agents[0].tokens.keys()}
            
            for agent in self.agents:
                self.delta_tokens = {
                    'type 1': min(DELTA_W_CONSTANT['type 1'], MAX_TOKEN_CHANGE),
                    'type 2': min(DELTA_W_CONSTANT['type 2'], MAX_TOKEN_CHANGE)
                }
            
                tax_paid = agent.update_state()
                for k, v in tax_paid.items():
                    self.total_tax_collected[k] += v
                self.community_contribution = sum(tax_paid.values())

            logger.info(f"Total tax collected before redistribution: {self.total_tax_collected}")
            apply_tax_policy(self.current_policy, self.agents, self.total_tax_collected, self)
            logger.info(f"Total tax collected after redistribution: {self.total_tax_collected}")

            G = self.get_network()
            # Update variables, rewards and weights
            for agent in self.agents:
                self.AS, self.SS, self.SI, self.AI = compute_DFIA(self.agents)
                self.R, self.S, self.V, self.A, self.IN, self.C, self.AL = agent.update_variables(G, self.agents)
                self.C = compute_competence(G, agent.agent_id, self.agents)
                self.AL = compute_action_level(self.C, self.V, self.A)
        
                if self.ASPREV is None:
                    self.ASPREV = ASINI
                else:
                    self.DELTA_AS = self.AS - self.ASPREV
                agent.compute_reward(self)
                agent.collect_data()

            avg_wealth = np.mean([sum(agent.tokens.values()) for agent in self.agents])
            self.wealth_history.append(avg_wealth)
            logging.info(f"Average Wealth: {avg_wealth}")
            self.time_series.append(self.time_step)
            logging.info(f"Time Step {self.time_step}:")
            avg_competence = np.mean([agent.C if agent.C is not None else 0 for agent in self.agents])
            self.avg_competence_history.append(avg_competence)
            logging.info(f"Average Competence: {avg_competence}")
            wealths = [sum(agent.tokens.values()) for agent in self.agents]
            logging.info(f"Agents' Wealth: {[sum(agent.tokens.values()) for agent in self.agents]}")
            gini = gini_coefficient(wealths)
            self.gini_history.append(gini)
            logging.info(f"Gini Coefficient: {gini}")

    def apply_policy(self, policy_name):
        self.current_policy = policy_name
        # Ensure total_tax_collected is a dictionary
        if not isinstance(self.total_tax_collected, dict):
            self.total_tax_collected = {k: 0 for k in self.agents[0].tokens.keys()}
        apply_tax_policy(self.current_policy, self.agents, self.total_tax_collected, self)
        logging.info(f"Policy set to: {self.current_policy}")
    
    def get_agents(self):
        return self.agents

    def get_agent_by_id(self, agent_id):
        for agent in self.agents:
            if agent.agent_id == agent_id:
                return agent
        return None

    def get_time_series(self):
        return self.time_series

    def get_wealth_time_series(self):
        return self.wealth_history

    def get_gini_coefficient(self):
        return self.gini_history[-1] if self.gini_history else 0

    def get_average_wealth(self):
        return self.wealth_history[-1] if self.wealth_history else 0

    def get_average_competence(self):
        return self.avg_competence_history[-1] if self.avg_competence_history else 0

    def get_network(self):
        if self.network is None:
            self.network = create_agent_network()
        return self.network

    def export_data(self):
        export_dir = EXPORT_DIR
        os.makedirs(export_dir, exist_ok=True)
        
        # Export aggregate data
        aggregate_data = pd.DataFrame({
            'Time Step': self.time_series,
            'Average Wealth': self.wealth_history,
            'Gini Coefficient': self.gini_history,
            'Average Competence': self.avg_competence_history
        })
        
        aggregate_data.to_csv(os.path.join(export_dir, 'aggregate_data.csv'), index=False)
        
        # Export individual agent data
        for agent in self.agents:
            agent_data = pd.DataFrame({
                'Time Step': self.time_series,
                'Tokens type 1': [tokens.get('type 1', 0) for tokens in agent.history['tokens']],
                'Tokens type 2': [tokens.get('type 2', 0) for tokens in agent.history['tokens']],
                'SF': agent.history['SF'],
                'AF': agent.history['AF'],
                'SI': agent.history['SI'],
                'AI': agent.history['AI'],
                'SS': agent.history['SS'],
                'AS': agent.history['AS'],
                'R': agent.history['R'],
                'S': agent.history['S'],
                'IN': agent.history['IN'],
                'V': agent.history['V'],
                'A': agent.history['A'],
                'C': agent.history['C'],
                'AL': agent.history['AL'],
            })
            
            agent_data.to_csv(os.path.join(export_dir, f'agent_{agent.agent_id}_data.csv'), index=False)
        
        logging.info(f"Data exported to {export_dir}.")

    @staticmethod
    def load_simulation(filename):
        with open(filename, 'rb') as f:
            simulation = pickle.load(f)
        logging.info(f"Simulation loaded from {filename}.")
        return simulation
