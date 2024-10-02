from parameters import *
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_flat_tax_rate(agent, token_type, simulation):
    flat_rate = simulation.FLAT_TAX_RATE
    tokens = agent.tokens.get(token_type, 0)
    tax_paid = min(flat_rate * tokens, MAX_TOKEN_CHANGE)
    return tax_paid

def redistribute_ubi(agents, total_tax_collected):
    num_agents = len(agents)
    if num_agents == 0:
        logger.warning("No agents to redistribute taxes to.")
        return
    
    for token_type, total_tax in total_tax_collected.items():
        ubi_payment = total_tax / num_agents
        for agent in agents:
            agent.tokens[token_type] = min(agent.tokens[token_type] + ubi_payment, MAX_TOKENS)
    
    logger.info(f"Taxes redistributed as UBI: {total_tax_collected}")

def redistribute_progressive(agents, total_tax_collected):
    num_agents = len(agents)
    if num_agents == 0:
        logger.warning("No agents to redistribute taxes to.")
        return
    for token_type, total_tax in total_tax_collected.items():
        total_tokens = sum(agent.tokens.get(token_type, 0) for agent in agents)
        if total_tokens == 0:
            logger.warning(f"No tokens of type '{token_type}' to redistribute.")
            continue
        base_share = total_tax / num_agents
        progressive_total = total_tax - base_share * num_agents
        total_inverse_tokens = sum(1 / (agent.tokens.get(token_type, 0) + 1) for agent in agents)
        for agent in agents:
            tokens = agent.tokens.get(token_type, 0)
            progressive_share = (1 / (tokens + 1)) / total_inverse_tokens * progressive_total
            total_share = base_share + progressive_share
            share = min(max(total_share, 0), MAX_TOKEN_CHANGE)
            agent.tokens[token_type] = min(agent.tokens[token_type] + share, MAX_TOKENS)
    logger.info("Taxes redistributed progressively.")

def apply_tax_policy(policy_name, agents, total_tax_collected, simulation):
    if policy_name == 'flat':
        for agent in agents:
            for token_type in agent.tokens.keys():
                tax = calculate_flat_tax_rate(agent, token_type, simulation)
                agent.tokens[token_type] -= tax
                total_tax_collected[token_type] += tax
        logger.info("Flat tax policy applied.")
    elif policy_name == 'ubi':
        for agent in agents:
            for token_type in agent.tokens.keys():
                tax = calculate_flat_tax_rate(agent, token_type, simulation)
                agent.tokens[token_type] -= tax
                total_tax_collected[token_type] += tax
        redistribute_ubi(agents, total_tax_collected)
    elif policy_name == 'progressive':
        for agent in agents:
            for token_type, tokens in agent.tokens.items():
                tax_rate = min(0.3, max(0.1, 0.1 + (tokens / 100) * 0.2))
                tax = min(tax_rate * tokens, MAX_TOKEN_CHANGE)
                agent.tokens[token_type] -= tax
                total_tax_collected[token_type] += tax
        redistribute_progressive(agents, total_tax_collected)
    else:
        logger.error(f"Unknown tax policy: {policy_name}")