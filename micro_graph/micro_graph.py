import math
import random
import snap

SUSCEPTIBLE, INFECTED, RECOVERED = 'S', 'I', 'R'

class MicroGraph:
  '''
  Class for all the county-level graph representations.
  @author Aaron Nagao
  
  Parameters that can be tweaked: 
    * degree of nodes in the graph
    * small-world rewire probability
    * SIR beta,delta parameters
  '''

  def __init__(self, graphType='random', numNodes=100):
    self.graphType = graphType
    self.numNodes = numNodes

    # initialize snap.py graph: self.G
    nodeDeg = int( math.log(numNodes) )
    if graphType == 'random':
      numEdges = numNodes * nodeDeg / 2
      self.G = snap.GenRndGnm(snap.PUNGraph, numNodes, numEdges)
      #self.G = snap.GenRndDegK(numNodes, nodeDeg)
    elif graphType == 'small world':
      rewireProb = 0.01 # probability that an edge will be rewired in Watts-Strogatz model
      self.G = snap.GenSmallWorld(numNodes, nodeDeg/2, rewireProb) # divide degree by 2 b/c graph is undirected
    elif graphType == 'complete':
      self.G = snap.GenFull(snap.PUNGraph, numNodes)
    elif graphType == 'scale free':
      self.G = snap.GenPrefAttach(numNodes, nodeDeg)
    else:
      raise NotImplementedError("graphType argument must be in {'random', 'small world', 'complete', 'scale free}")

    # initialize variables for SIR model
    # inital beta, delta values from https://grantbrown.github.io/Ebola-2014-Analysis-Archive/Oct_02_2014/Ebola2014/Ebola2014.html
    self.beta = 0.259 / 2
    self.delta = 0.08
    self.state = dict.fromkeys(xrange(numNodes), SUSCEPTIBLE) # dict: int nodeID => string SUSCEPTIBLE or INFECTED or RECOVERED
    self.countyHasBeenInfected = False

  '''
  The infect method is called when an infection has spread from another county
  to this county. This county must then infect a node according to the protocol.
  '''
  def infect(self):
    self.countyHasBeenInfected = True

    infectedNodeID = random.randrange(self.numNodes)
    if self.state[infectedNodeID] == SUSCEPTIBLE:
      self.state[infectedNodeID] = INFECTED

  '''
  Returns the number of currently infected nodes in this county.
  '''
  def getNumInfected(self):
    return sum(1 for nodeID in self.state if self.state[nodeID]==INFECTED)

  '''
  Advance the infection cascades on this micro-graph by one timestep.
  Currently an Susceptible-Infected-Recovered (SIR) model.
  TODO: Consider an SEIR model?
  '''
  def advanceDay(self):
    if not self.countyHasBeenInfected:
      # ebola has not yet spread to this county: infect() hasn't been called yet.
      # minor optimization: do not need to run any SIR simulation (since we know everyone will remain SUSCEPTIBLE)
      return

    # TODO: randomly shuffle the order which we go through the nodes
    randomOrdering = random.shuffle( range(self.numNodes) )
    for currID in randomOrdering:
      NI = self.G.GetNI(currID)

      if self.state[currID] == SUSCEPTIBLE:
        # each of its infected neighbors can infect it with probability beta
        numInfectedNeighbors = sum(1 for neighborID in NI.GetOutEdges() if self.state[neighborID]==INFECTED)
        if random.random() > math.pow(1-self.beta, numInfectedNeighbors): # Pr(not infected) = (1-beta)^numNeigbors
          self.state[currID] = INFECTED
      
      elif self.state[currID] == INFECTED:
        # TODO: take into account how long the node has had the disease?
        # (e.g. can't recover until minimum of 5 days have passed?)

        # recover with probability delta
        if random.random() < self.delta:
          self.state[currID] == RECOVERED

  '''
    Returns the number of nodes in the graph.
  '''
  def getNumNodes(self):
    return self.numNodes

  '''
  Returns <String>'random' or 'small world'
  '''
  def getType(self):
    return self.graphType
