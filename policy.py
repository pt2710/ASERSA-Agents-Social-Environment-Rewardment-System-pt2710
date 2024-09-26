# policy.py
from functions import redistribute_taxes, calculate_tax_rate
from parameters import *

# Here, you can implement different tax policies and redistribution mechanisms

def calculate_flat_tax_rate(agent):
    flat_rate = 0.2  # Flat tax rate of 20%
    tax_paid = flat_rate * agent.W
    return tax_paid

def redistribute_ubi(agents, total_tax_collected):
    ubi_payment = total_tax_collected / len(agents)
    for agent in agents:
        agent.W += ubi_payment
