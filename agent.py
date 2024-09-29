# agent.py
import numpy as np
from parameters import *
from functions import *

class Agent:
    def __init__(self, agent_id, initial_wealth):
        self.agent_id = agent_id
        self.W = initial_wealth
        self.initialize_variables()
        
        # Adaptive Reward Function Variables
        self.alpha = 0.4
        self.beta = 0.3
        self.gamma = 0.3
        self.P = 0
        self.r = 0
        self.delta = 0
        self.prev_P = 0
        self.eta = 0.05
        self.lambda_ = 0.9

        # Learning from Best Performers
        self.kappa = 0.1
        self.kappa_min = 0.01
        self.kappa_max = 0.2

        # DFIA Variables
        self.Sigma_i = 0
        self.Xz = 0
        self.Xzo = 0

        # Previous Agent Status for delta_AS
        self.prev_AS = self.AS

        # For data collection
        self.history = {
            'W': [],
            'I': [],
            'AS': [],
            'C': [],
            'Xz': [],
            'Xzo': [],
            'S': [],
            'R': [],
            'V': [],
            'A': []    
        }

    def initialize_variables(self):
        # Initialize variables (I and AS will be updated via DFIA)
        self.I = 0
        self.AS = 0
        self.R = 0
        self.S = 0
        self.V = 0
        self.A = 0
        self.C = 0
        self.IN = 0
        self.AL = 0

    def update_state(self, delta_W, W_min, W_max, AS_max, E):
        # Calculate tax rate
        tau = calculate_tax_rate(self, W_min, W_max, AS_max, E)
        self.tax_paid = tau * self.W  # Store tax_paid as an attribute
        self.W += delta_W - self.tax_paid

        # Responsibility, Self-Esteem, Willpower, and Ambition will be updated after DFIA

        return self.tax_paid

    def update_psychological_variables(self):
        self.R = compute_responsibility(self.I)
        self.S = compute_self_esteem(self.R)
        self.V = compute_willpower(self.S)
        self.A = compute_ambition(self.V)

    def update_inspiration(self, C_best):
        self.IN = compute_inspiration(self.C)

    def adjust_learning_rate(self, competence_gap):
        normalized_gap = competence_gap / C_MAX
        new_kappa = self.kappa_min + (self.kappa_max - self.kappa_min) * normalized_gap
        new_kappa = max(self.kappa_min, min(new_kappa, self.kappa_max))
        return new_kappa

    def update_competence(self, C_best):
        competence_gap = C_best - self.C
        self.kappa = self.adjust_learning_rate(competence_gap)
        delta_C_self = K7 * (self.A + self.IN) * (C_MAX - self.C)
        delta_C_best = self.kappa * competence_gap
        self.C += delta_C_self + delta_C_best
        self.C = max(0, min(self.C, C_MAX))

    def compute_reward(self, delta_W, community_contribution, delta_AS):
        self.r = self.alpha * delta_W + self.beta * community_contribution + self.gamma * delta_AS
        self.P = (1 - self.lambda_) * self.r + self.lambda_ * self.prev_P
        self.delta = self.r + self.lambda_ * self.P - self.prev_P

        # Gradient Calculations
        grad_alpha = delta_W
        grad_beta = community_contribution
        grad_gamma = delta_AS

        # Update Weights
        self.alpha += self.eta * self.delta * grad_alpha
        self.beta += self.eta * self.delta * grad_beta
        self.gamma += self.eta * self.delta * grad_gamma

        # Normalize Weights
        total_weight = self.alpha + self.beta + self.gamma
        if total_weight != 0:
            self.alpha /= total_weight
            self.beta /= total_weight
            self.gamma /= total_weight
        else:
            # Avoid division by zero
            self.alpha = self.beta = self.gamma = 1/3

        # Update Previous Performance
        self.prev_P = self.P

    def collect_data(self):
        self.history['W'].append(self.W)
        self.history['I'].append(self.I)
        self.history['AS'].append(self.AS)
        self.history['C'].append(self.C)
        self.history['Xz'].append(self.Xz)
        self.history['Xzo'].append(self.Xzo)
        self.history['S'].append(self.S)
        self.history['R'].append(self.R)
        self.history['V'].append(self.V)
        self.history['A'].append(self.A)
        print(f"Agent {self.agent_id} collected data at time {len(self.history['W'])}")


    def __str__(self):
        return f"Agent {self.agent_id}: W={self.W:.2f}, I={self.I:.2f}, AS={self.AS:.2f}, C={self.C:.2f}"
