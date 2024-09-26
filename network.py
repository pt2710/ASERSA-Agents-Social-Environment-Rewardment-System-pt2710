# network.py
import networkx as nx
from parameters import NUM_AGENTS, NETWORK_PROBABILITY

def create_agent_network():
    # Create a random network of agents
    G = nx.erdos_renyi_graph(n=NUM_AGENTS, p=NETWORK_PROBABILITY)
    return G
