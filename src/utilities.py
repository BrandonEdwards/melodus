from .agent import Agent

def hashNestingHabitat(agentDB):
	nestingHash = dict()
	i = 0
	for agent in agentDB:
		if agent.getHabitatType() == 2:
			nestingHash[i] = agent.getAgentID()
			i += 1

	return nestingHash