import numpy as np
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from parameters import *
from functions import *
class Agent:
    def __init__(self, agent_id, initial_tokens, delta_tokens):
        self.agent_id = agent_id
        self.tokens = initial_tokens
        self.delta_tokens = delta_tokens
        self.ASPREV = None
        self.DELTA_AS = 0
        self.initialize_variables()
        
        self.alpha = ALPHA_INITIAL
        self.beta = BETA_INITIAL
        self.gamma = GAMMA_INITIAL
        self.P = 0
        self.r = 0
        self.delta = 0
        self.P_PREV = 0
        self.eta = ETA
        self.lambda_ = LAMBDA_
        self.DELTA_AS = 0
        self.tau = 0

        # Learning from Best Performers
        self.kappa_min = KAPPA_MIN
        self.kappa_max = KAPPA_MAX

        # For data collection
        self.history = {
            'tokens': [],
            'SF': [],
            'AF': [],
            'SI': [],
            'AI': [],
            'SS': [],
            'AS': [],
            'R': [],
            'S': [],
            'IN': [],
            'V': [],
            'A': [],
            'C': [],
            'AL': []    
        }

    def initialize_variables(self):
        self.SF = 0
        self.AF = 0
        self.SS = 0
        self.AS = 0
        self.SI = 0
        self.AI = 0
        self.R = 0
        self.S = 0
        self.V = 0
        self.A = 0
        self.IN = 0
        self.C = 0
        self.AL = 0
        
    def transfer_tokens(self, recipient, token_type, amount):
            if self.tokens.get(token_type, 0) >= amount:
                self.tokens[token_type] -= amount
                recipient.tokens[token_type] = recipient.tokens.get(token_type, 0) + amount
                return True
            return False

    def update_state(self):
        self.tau = calculate_tax_rate(self.AS, self.tokens)
        self.tax_paid = {k: v * self.tau for k, v in self.tokens.items()}
        self.community_contribution = sum(self.tax_paid.values())
        for k, v in self.tax_paid.items():
            self.tokens[k] += self.delta_tokens.get(k, 0) - v
        return self.tax_paid

    def update_variables(self, G, agents):
        self.R = compute_responsibility(self.AF, self.SF)
        self.S = compute_self_esteem(self.SS, self.AS)
        self.IN = compute_inspiration(self.AI, self.SI)
        self.V = compute_willpower(self.S, self.IN)
        self.A = compute_ambition(self.IN, self.R)
        self.C = compute_competence(G, self.agent_id, agents)
        return self.R, self.S, self.V, self.A, self.IN, self.C, self.AL

    def adjust_learning_rate(self):
        self.kappa = self.kappa_min + (self.kappa_max - self.kappa_min)
        self.kappa = max(self.kappa_min, min(self.kappa, self.kappa_max))
        return self.kappa

    def compute_reward(self, simulation):
        self.r = self.alpha * sum(self.delta_tokens.values()) + self.beta * self.community_contribution + self.gamma * self.DELTA_AS
        self.P = (1 - self.lambda_) * self.r + self.lambda_ * self.P_PREV
        self.delta = self.r + self.lambda_ * self.P - self.P_PREV

        # Gradient Calculations
        grad_alpha = sum(self.delta_tokens.values())
        grad_beta = self.community_contribution
        grad_gamma = self.DELTA_AS

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
            self.alpha = self.beta = self.gamma = 1/3
        self.P_PREV = self.P

    def collect_data(self):
        self.history['tokens'].append(self.tokens.copy())
        self.history['SF'].append(self.SF)
        self.history['AF'].append(self.AF)
        self.history['SS'].append(self.SS)
        self.history['AS'].append(self.AS)
        self.history['SI'].append(self.SI)
        self.history['AI'].append(self.AI)
        self.history['R'].append(self.R)
        self.history['S'].append(self.S)
        self.history['IN'].append(self.IN)
        self.history['V'].append(self.V)
        self.history['A'].append(self.A)
        self.history['C'].append(self.C)
        self.history['AL'].append(self.AL)
        print(f"Agent {self.agent_id} collected data at time {len(self.history['tokens'])}")

    def __str__(self):
        return f"Agent {self.agent_id}: Tokens={self.tokens}, AI={self.AI:.2f}, AS={self.AS:.2f}, C={self.C:.2f}"