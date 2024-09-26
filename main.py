# main.py
import numpy as np
from agent import Agent
from functions import *
from parameters import *
from network import create_agent_network
from analysis import analyze_results

# Initialize agents
agents = []
initial_wealths = np.random.uniform(W_MIN, W_MAX, NUM_AGENTS)
for i in range(NUM_AGENTS):
    agent = Agent(agent_id=i, initial_wealth=initial_wealths[i])
    agents.append(agent)

# Create agent network
G = create_agent_network()

# Simulation Loop
for t in range(NUM_TIMESTEPS):
    print(f"Time Step {t+1}")
    total_tax_collected = 0
    W_min = min(agent.W for agent in agents)
    W_max = max(agent.W for agent in agents)
    AS_max = max(agent.AS for agent in agents)
    Xn = len(agents)
    z = 100  # Total theoretical capacity (Zone)

    # Update agents' wealth and variables up to ambition
    for agent in agents:
        delta_W = DELTA_W_CONSTANT
        tax_paid = agent.update_state(delta_W, W_min, W_max, AS_max, E)
        total_tax_collected += tax_paid

    # Redistribute taxes
    redistribute_taxes(agents, total_tax_collected)

    # DFIA Calculations
    XnF = sum(agent.I for agent in agents)
    Xz = z / Xn  # Theoretical volume per agent

    for agent in agents:
        XrnF_X = XnF - agent.I
        agent.update_DFIA_values(XnF, Xn, Xz, XrnF_X)

    # Adjust influence based on DFIA
    for agent in agents:
        agent.adjust_influence_based_on_DFIA()

    # Update inspiration and competence
    for agent_id, agent in enumerate(agents):
        C_best = calculate_C_best(agents, G, agent_id)
        agent.update_inspiration(C_best)
        agent.update_competence(C_best)
        agent.AL = compute_action_level(agent.IN, agent.V, agent.A)
        agent.collect_data()  # Collect data for analysis

    # Update rewards and weights
    for agent in agents:
        community_contribution = tax_paid  # Using tax_paid as community contribution
        delta_AS = agent.AS - agent.prev_AS
        agent.prev_AS = agent.AS
        agent.compute_reward(delta_W, community_contribution, delta_AS)

# Analyze results after simulation
analyze_results(agents)
