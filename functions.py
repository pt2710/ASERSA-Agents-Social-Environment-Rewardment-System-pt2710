# functions.py
import numpy as np
from parameters import *
import gui
import networkx as nx
import math

def compute_DFIA(agents, z=100):
    """
    Compute the DFIA components for all agents.
    - agents: list of Agent objects
    - z: Total theoretical capacity (Zone), default is 100
    """
    Xn = len(agents)  # Number of agents
    XnF = sum(agent.W for agent in agents)  # Total wealth (XF)
    Xz = z / Xn  # Theoretical volume per agent
    epsilon = 1e-5  # To prevent division by zero

    for agent in agents:
        XrnF_t = XnF - agent.W  # Total wealth excluding the agent's own wealth
        if XrnF_t == 0 or Xn == 0:
            Sigma_i = 1
        else:
            Sigma_i = (XnF * (Xn - 1)) / ((XrnF_t * Xn) + epsilon)
        agent.Sigma_i = Sigma_i
        agent.Xz = Xz * Sigma_i
        agent.Xzo = agent.Xz - Xz
        # Update Influence and Agent Status
        agent.I = agent.Xzo  # Xzo[t] represents relative Influence
        agent.AS = agent.Xz  # Xz[t] represents relative volume (Agent Status)

def compute_responsibility(I, Sigma_i): # Calculated from relative influence and relative Social status
    K3_value = gui.K3
    R = R0 * np.exp(K3_value * (I / Sigma_i))
    return R

def compute_self_esteem(Xz, AS, avg_wealth_growth):
    K4_value = gui.K4
    S = K4_value * ((AS / Xz) ** 2) * avg_wealth_growth
    return S

def compute_inspiration(I, I_max):
    IN = PHI * (I_max - I)
    return IN

def compute_willpower(S, R, IN): # Calculated from Self esteem, Responsibility and Inspiration
    K5_value = gui.K5
    V = V_MAX / (1 + np.exp(K5_value * (S + R + IN)))
    return V

def compute_ambition(IN, I, XrnF):
    K6_value = gui.K6
    scaled_XrnF = XrnF / 10000  # Scale down XrnF
    A = K6_value * (IN**2 + I**2 + scaled_XrnF**2)
    return A

def compute_competence(C):
    K7_value = gui.K7
    delta_C = K7_value * (C_MAX - C)
    C_new = C + delta_C
    return C_new

def compute_action_level(C_new, V, A):
    AL = PSI * C_new * (V + A)
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
    # Calculate the average competence of the agent's neighbors in the network G
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
    gini = (n + 1 - 2 * np.sum(relative_mean)) / n
    return gini

