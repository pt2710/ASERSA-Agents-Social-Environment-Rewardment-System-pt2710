# main.py
import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow
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
    # [Simulation logic]
    pass

# Analyze results after simulation
analyze_results(agents)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
