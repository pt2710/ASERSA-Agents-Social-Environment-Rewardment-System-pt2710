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
        self.XF = self.I
        self.Xz = 0
        self.Xzo = 0
        self.Sigma_i = 0

        # Previous Agent Status for delta_AS
        self.prev_AS = self.AS

        # For data collection
        self.history = {'W': [], 'I': [], 'AS': [], 'C': []}

    def initialize_variables(self):
        self.I = compute_influence(self.W)
        self.AS = compute_agent_status(self.I)
        self.R = compute_responsibility(self.AS)
        self.S = compute_self_esteem(self.R)
        self.V = compute_willpower(self.S)
        self.A = compute_ambition(self.V)
        self.C = compute_competence(0, self.A)
        self.IN = compute_inspiration(self.C)
        self.AL = compute_action_level(self.IN, self.V, self.A)

    def update_state(self, delta_W, W_min, W_max, AS_max, E):
        # Calculate tax rate
        tau = calculate_tax_rate(self, W_min, W_max, AS_max, E)
        self.tax_paid = tau * self.W  # Store tax_paid as an attribute
        self.W += delta_W - self.tax_paid

        # Update Influence
        self.I = compute_influence(self.W)

        # Update Agent Status
        self.AS = compute_agent_status(self.I)

        # Update Responsibility
        self.R = compute_responsibility(self.AS)

        # Update Self-Esteem
        self.S = compute_self_esteem(self.R)

        # Update Willpower
        self.V = compute_willpower(self.S)

        # Update Ambition
        self.A = compute_ambition(self.V)

        return self.tax_paid

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

    def update_DFIA_values(self, XnF, Xn, Xz, XrnF_X):
        if XrnF_X == 0 or Xn == 0:
            self.Sigma_i = 1
        else:
            self.Sigma_i = (XnF * (Xn - 1)) / (XrnF_X * Xn)
        self.Xz = Xz * self.Sigma_i
        self.Xzo = self.Xz - Xz

    def adjust_influence_based_on_DFIA(self):
        adjustment_factor = 1 + (self.Xzo / 100)
        self.I *= adjustment_factor
        self.I = max(0, min(self.I, I_MAX))

    def collect_data(self):
        self.history['W'].append(self.W)
        self.history['I'].append(self.I)
        self.history['AS'].append(self.AS)
        self.history['C'].append(self.C)

    def __str__(self):
        return f"Agent {self.agent_id}: W={self.W:.2f}, I={self.I:.2f}, AS={self.AS:.2f}, C={self.C:.2f}"
