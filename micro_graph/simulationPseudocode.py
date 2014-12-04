"""
Pseudo-code for one iteration of an SIR simulation on a micro-graph

Variables:
Graph: snap.py
state: dict, int nodeID => string SUSCEPTIBLE or INFECTED or RECOVERED
beta, delta: SIR parameters
"""
import random

for NI in Graph.Nodes():
    currID = NI.GetId()

    if state[currID] == SUSCEPTIBLE:
        # each of its neighbors infect it with probability beta
        infectedNeighbors = [neighborID for neighborID in NI.GetOutEdges() if state[neighborID]==INFECTED]
        for neighborID in infectedNeighbors: # can avoid this for loop by Pr(not infected) = (1-beta)^numNeigbors
            if random.random() < beta:
                state[currID] = INFECTED
                break
    elif state[currID] == INFECTED:
        # TODO: take into account how long the node has had the disease?
        # (e.g. can't recover until minimum of 5 days have passed?)
        
        # recover with probability delta
        if random.random() < delta:
            state[currID] == RECOVERED