# functions.py
import numpy as np
from parameters import *

def compute_influence(W):
    I = I_MAX / (1 + np.exp(-K1 * (W - W0)))
    return I

def compute_agent_status(I):
    AS = K2 * (I ** ALPHA)
    return AS

def compute_responsibility(AS):
    R = R0 * np.exp(K3 * AS)
    return R

def compute_self_esteem(R):
    S = -K4 * ((R - ROPT) ** 2) + SMAX
    return S

def compute_willpower(S):
    V = V_MAX / (1 + np.exp(-K5 * (S - S0)))
    return V

def compute_ambition(V):
    A = K6 * (V ** 2)
    return A

def compute_competence(C, A):
    delta_C = K7 * A * (C_MAX - C)
    C_new = C + delta_C
    return C_new

def compute_inspiration(C):
    IN = PHI * (C_BEST_INITIAL - C)
    return IN

def compute_action_level(IN, V, A):
    AL = PSI * IN * (V + A)
    return AL

def calculate_tax_rate(agent, W_min, W_max, AS_max, E):
    wealth_component = OMEGA_W * (agent.W - W_min) / (W_max - W_min) if W_max != W_min else 0
    status_component = OMEGA_AS * agent.AS / AS_max if AS_max != 0 else 0
    economic_component = OMEGA_E * E
    tau = TAU_MAX * (wealth_component + status_component + economic_component)
    tau = min(tau, TAU_MAX)
    return tau

def redistribute_taxes(agents, total_tax_collected):
    W_avg = np.mean([agent.W for agent in agents])
    RD_indices = []
    for agent in agents:
        RD = (W_avg - agent.W) / W_avg if W_avg != 0 else 0
        RD_indices.append(RD)
    RD_indices_theta = [RD ** THETA if RD > 0 else 0 for RD in RD_indices]
    total_RD = sum(RD_indices_theta)
    if total_RD == 0:
        return
    for i, agent in enumerate(agents):
        share = (RD_indices_theta[i] / total_RD) * total_tax_collected if total_RD != 0 else 0
        agent.W += share

def calculate_C_best(agents, G, agent_id):
    neighbors = list(G.neighbors(agent_id))
    if not neighbors:
        return agents[agent_id].C  # No neighbors, use own competence
    neighbor_competences = [agents[n].C for n in neighbors]
    C_best = np.mean(neighbor_competences)
    return C_best

def gini_coefficient(values):
    sorted_values = np.sort(values)
    n = len(values)
    cumulative_values = np.cumsum(sorted_values)
    cumulative_sum = np.sum(sorted_values)
    if cumulative_sum == 0:
        return 0
    relative_mean = cumulative_values / cumulative_sum
    index = np.arange(1, n+1)
    gini = (n + 1 - 2 * np.sum(relative_mean) / n)
    return gini
