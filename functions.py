import numpy as np
from parameters import *
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import gui
import networkx as nx
import math

def compute_DFIA(agents):
    z = 100 # Zone consisting of 100% - (This is alfa null(an infinite scaleable theoretical space which always can be interpretted as 100% no matter the number of X's or the size of the force("F": value of variables)))
    Xn = len(agents)  # Total number(n) of agents(X)
    Xz = z / Xn  # Theoretical volume per agent
    for agent in agents:
        agent.XF_t = sum(agent.tokens.values()) # Relative force(F) of agent(X) - (number of tokens the specific agent currently holds)
        agent.XnF_t = sum(sum(a.tokens.values()) for a in agents)  # Total relative force of all agents summed together
        agent.XrnF_t = agent.XnF_t - agent.XF_t # # Total force of all agents summed together(XnF), exclusive the force of the specific agent(XF) currently under consideration
        agent.Sigma_Xi_t = (agent.XnF_t * (Xn - 1)) / (agent.XrnF_t * Xn)
        agent.Xz_t = Xz * agent.Sigma_Xi_t # Xz_t represents relative volume (Agent Status)
        agent.Xzo_t = agent.Xz_t - Xz # Xzo_t represents relative Influence
        """
        Changing names of DFIA variables
        """
        agent.SF = agent.XrnF_t # Relative society force(SF)
        agent.AF = agent.XF_t # Relative Agent force(AF)
        agent.SS = z - agent.Xz_t # Relative society status(SS)
        agent.AS = agent.Xz_t # Relative agent status(AS)
        agent.SI = agent.Sigma_Xi_t # Relative society influence(SI)
        agent.AI = agent.Xzo_t # # Relative influence(I)
    
    return agent.AS, agent.SS, agent.SI, agent.AI

def compute_responsibility(AF, SF):
    if AF == 0 or SF == 0:
        return 0
    force_ratio = AF / SF
    normalized_ratio = force_ratio / (1 + force_ratio)
    R = normalized_ratio * ROPT
    return R

def compute_self_esteem(SS, AS):
    if AS == 0:
        return 0
    status_ratio = AS / (SS + AS)
    S = (status_ratio ** 2) * SOPT
    return S

def compute_inspiration(AI, SI):
    influence_ratio = AI / SI
    result = influence_ratio * IOPT
    if result >= 0:
        IN = math.sqrt(result)
    else:
        IN = 0
    return IN

def compute_willpower(S, IN):
    if VOPT is None or S == 0 or IN == 0:
        return 0 
    motivation = S * IN
    V = VOPT * (1 - math.exp(-motivation))
    return V

def compute_ambition(IN, R):
    K6 = gui.K6
    if IN == 0 or R == 0:
        return 0
    ratio = IN / R if R != 0 else 0
    A = K6 * (1 - math.exp(-ratio))
    return A

def compute_action_level(C, V, A):
    if C == 0 or V == 0 or A == 0:
        return 0
    motivation = (C * V * A) ** (1/3)
    AL = PSI * (1 - math.exp(-motivation))
    return AL

def calculate_tax_rate(AS, tokens):
    wealth_component = OMEGA_W * (sum(tokens.values()))
    status_component = OMEGA_AS * AS / ASOPT if ASOPT != 0 else 0
    economic_component = OMEGA_E * E
    tau = TAU_MAX * (wealth_component + status_component + economic_component)
    tau = min(tau, TAU_MAX)
    return tau

def compute_competence(G, agent_id, agents):
    K7 = gui.K7
    COPT = gui.COPT 
    neighbors = list(G.neighbors(agent_id))
    if not neighbors:
        return agents[agent_id].C if hasattr(agents[agent_id], 'C') else 0
    neighbor_competences = [agents[n].C for n in neighbors if hasattr(agents[n], 'C')]
    if not neighbor_competences:
        return agents[agent_id].C if hasattr(agents[agent_id], 'C') else 0
    avg_neighbor_competence = np.mean(neighbor_competences)
    if avg_neighbor_competence > 0:
        normalized_avg = avg_neighbor_competence / (avg_neighbor_competence + 1)
    else:
        normalized_avg = 0
    C = K7 * COPT * (1 - normalized_avg)
    C = max(0, min(C, COPT))
    logging.info(f"Agent {agent_id}: Avg neighbor competence: {avg_neighbor_competence}, Normalized: {normalized_avg}, Calculated C: {C}")
    return C

def redistribute_taxes(agents, total_tax_collected):
    W_avg = np.mean([sum(agent.tokens.values()) for agent in agents])
    RD_indices = []
    for agent in agents:
        RD = (W_avg - sum(agent.tokens.values())) / W_avg if W_avg != 0 else 0
        RD_indices.append(RD)
    RD_indices_theta = [RD ** THETA if RD > 0 else 0 for RD in RD_indices]
    total_RD = sum(RD_indices_theta)
    if total_RD == 0:
        return
    for i, agent in enumerate(agents):
        share = (RD_indices_theta[i] / total_RD) * sum(total_tax_collected.values()) if total_RD != 0 else 0
        agent.tokens['type 1'] += share

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