# Constants and Parameters

I_MAX = 100          # Maximum influence
R0 = 1               # Base responsibility
ROPT = 30            # Optimal responsibility level
S_BASE = 1          # Base level of self esteem
SMAX = 100           # Maximum self-esteem
V_MAX = 100          # Maximum willpower
C_MAX = 100          # Maximum competence

# K1 = 0.0001             # Growth rate for influence
# K2 = 0.0001               # Proportionality constant for agent status
# K3 = 0.0001          # Growth rate for responsibility
# K4 = 0.0001          # Constant controlling curve width for self-esteem
# K5 = 0.1             # Growth rate for willpower
# K6 = 0.001           # Proportionality constant for ambition
# K7 = 0.01            # Learning rate for competence

W0 = 50              # Wealth value at which influence is half of I_MAX
S0 = 50              # Self-esteem value at which willpower is half of V_MAX

ALPHA = 1.2          # Exponent controlling non-linearity for agent status
PHI = 0.5            # Sensitivity to inspiration
PSI = 0.01           # Proportionality constant for action level
C_BEST_INITIAL = 80  # Initial average competence of the best-performing agents

# Tax and Redistribution Parameters
TAU_MAX = 0.4        # Maximum tax rate
OMEGA_W = 0.5        # Weight for wealth in tax calculation
OMEGA_AS = 0.3       # Weight for agent status in tax calculation
OMEGA_E = 0.2        # Weight for economic stability in tax calculation
THETA = 2            # Redistribution sensitivity parameter
E = 0.2              # Economic stability factor

# Simulation Parameters
NUM_AGENTS = 100
NUM_TIMESTEPS = 50

DELTA_W_CONSTANT = 5 # Constant income for simplicity
W_MIN = 20           # Minimum initial wealth
W_MAX = 80           # Maximum initial wealth

# Network Parameters
NETWORK_PROBABILITY = 0.05  # Probability for edge creation in the network
