import os
# Simulation Parameters
NUM_AGENTS = 100
NUM_TIMESTEPS = 50
ASINI = 100.0
ASOPT = 100.0
ROPT = 100.0
SOPT = 100.0
IOPT = 100.0
VOPT = 100.0
COPT = 100.0
CINI = 100.0

W_MIN = 0
W_MAX = 100
      
# Conversion Rates for Tokens to Force Values
TOKEN_CONVERSION_RATES = {
    'type 1': 1.0,      # Each resource token equals 1 force unit
    'type 2': 2.0,     # Each influence token equals 2 force units
}
MAX_TOKEN_CHANGE = 100
MAX_TOKENS = 1000000
# Learning and Reward Parameters
ALPHA_INITIAL = 0.4
BETA_INITIAL = 0.3
GAMMA_INITIAL = 0.3
ETA = 0.05
LAMBDA_ = 0.9

# Adaptive Reward Function Variables
KAPPA_MIN = 0.01
KAPPA_MAX = 0.2

# Tax and Redistribution Parameters
FLAT_TAX_RATE = 0.2  # Adjust as needed
TAU_MAX = 0.4        # Maximum tax rate
OMEGA_W = 0.5        # Weight for wealth in tax calculation
OMEGA_AS = 0.3       # Weight for agent status in tax calculation
OMEGA_E = 0.2        # Weight for economic stability in tax calculation
THETA = 2            # Redistribution sensitivity parameter
E = 0.2              # Economic stability factor

DELTA_W_CONSTANT = {
    'type 1': 5,     # Constant income for resource tokens
    'type 2': 3     # Constant income for influence tokens
}

# Network Parameters
NETWORK_PROBABILITY = 0.05  # Probability for edge creation in the network

# Other Constants
PHI = 0.5            # Sensitivity to inspiration
PSI = 0.01           # Proportionality constant for action level

# File Paths
EXPORT_DIR = os.path.join("simulation_data", "exported_data")
EXPORT_PLOTS_DIR = os.path.join("simulation_data", "exported_plots")
