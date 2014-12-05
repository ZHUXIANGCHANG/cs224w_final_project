from __future__ import division
import csv
from datetime import date, datetime, timedelta
import json
import os
import random
import snap
import sys

# Importing our micro graphs
sys.path.insert(0, '../micro_graph')
from micro_graph import MicroGraph

# Naming constants
SIERRA_LEONE_PREFIX = 'sl'
LIBERIA_PREFIX = 'lib'
GUINEA_PREFIX = 'guin'
COUNTRY_NAME_TO_PREFIX = {'Sierra Leone':SIERRA_LEONE_PREFIX, 'Liberia':LIBERIA_PREFIX, 'Guinea':GUINEA_PREFIX}
PREFIX_TO_SIMULATION_INTERVAL = {SIERRA_LEONE_PREFIX:(date(2014,8,12), date(2014,11,6)), LIBERIA_PREFIX:(date(2014,6,16), date(2014,11,2)), GUINEA_PREFIX:(date(2014,8,4), date(2014, 10, 01))}

"""
Class definition for the macro graph.
"""
class MacroGraph:
  def __init__(self, simulationInfo):
    self.simulationInfo = simulationInfo
    self.title = simulationInfo['title']
    self.countryPrefix = COUNTRY_NAME_TO_PREFIX[ str(simulationInfo['countryName']) ]
    self.startDate, self.endDate = PREFIX_TO_SIMULATION_INTERVAL[self.countryPrefix]
    self.duration = (self.endDate-self.startDate).days
    """
    q is the probability of a county infecting its neighbors given 
    that all nodes in the county are infected. This bounds from above
    the probability of nodes spreading across counties.
    """
    self.q = simulationInfo['q']
    
    # number of nodes in graph = county's actual population / scalingFactor
    # note: this is also used by micro_graph to determine desired degree of nodes
    self.scalingFactor = 10

    # Populate the macro graph structure
    cwd = os.getcwd()
    os.chdir('../macro_graph')
    self.G, self.labels = MacroGraph.loadGraphAndLabels(self.countryPrefix)
    os.chdir(cwd)
    # Generate the county graphs
    beta, delta = simulationInfo['beta'], simulationInfo['delta']
    countyGraphType = simulationInfo['countyGraphType']
    self.countyGraphs = {}
    self.totalNumNodes = 0
    for nID, countyName in self.labels.iteritems():
      numNodes = simulationInfo['countiesToPopulation'][countyName] // self.scalingFactor # TODO: see how algorithm scales to larger graph sizes
      countyG = MicroGraph(beta, delta, countyGraphType, numNodes, self.scalingFactor)
      self.totalNumNodes += numNodes
      self.countyGraphs[nID] = countyG

  def simulate(self):
    '''
    Run the simulation.
    @return allInfectedCounts: dict from date => upscaled infectedCounts from that date
           e.g. '2014-10-18': {'Gbarpolu': 80000, 'Grand Gedeh': 120000, ... }
    '''
    # Initialize counters
    self.crossCountyInfections = self.crossCountyAttempts = 0
    self.allInfectedCounts = {} # keeps track of all infectedCounts

    # Open an output data file for each county
    countyIDToOutputFile = self.initializeOutputFiles()

    # Infect initial random county
    startCountyID, startCountyG = random.sample(self.countyGraphs.items(), 1)[0]
    startCountyG.infect()

    print "This simulation will run for %d days" % self.duration
    print "Day Counter: ",
    for day in xrange(self.duration):
      print "%d" % (day+1),
      # Get number infected from each county
      infectedCounts = self.getInfectedCounts()
      # Flush infected counts data for this day to the .tab files for each county, and to allInfectedCounts
      self.flushInfectedCounts(infectedCounts, day, countyIDToOutputFile)

      # Advance a day
      for countyID, countyGraph in self.countyGraphs.iteritems():
        countyGraph.advanceDay()

      # Attempt to infect neighbors
      self.infectCrossCounty()

    # Close all the output data files
    for countyID, outputFile in countyIDToOutputFile.iteritems():
      outputFile.close()

    # Generate the .png plot file
    cwd = os.getcwd()
    os.chdir('results')
    os.chdir(self.outputDir)
    subprocess.call(['gnuplot', '%s.plt' % self.title])

    print '%s: %d cross-county infections on %d attempts (probability: %f)' % (self.title, self.crossCountyInfections, self.crossCountyAttempts, self.crossCountyInfections/self.crossCountyAttempts)
    return self.allInfectedCounts

  def initializeOutputFiles(self):
    cwd = os.getcwd()

    # Create output directory
    os.chdir('results')
    outputDir = self.generateOutputDirName()
    os.makedirs(outputDir)
    os.chdir(outputDir)
    self.outputDir = outputDir

    # Dump simulation info to a README
    readmeF = open('README.txt', 'w')
    readmeF.write(str(self))
    readmeF.close()

    # Open an output data file for each country
    outputFiles = {}
    for countyID, county in self.labels.iteritems():
      f = open('%s.tab' % cleanse(county), 'w')
      f.write('%s\n' % commentify(self.title))
      f.write('%s\n' % commentify(county))
      outputFiles[countyID] = f

    # Create a .plt file to plot the simulation results
    self.genPltFile()

    # Return to original working directory
    os.chdir(cwd)

    return outputFiles

  def generateOutputDirName(self):
    timestamp = [datetime.now().strftime('%Y-%m-%d_%H-%M-%S')]
    return '_'.join(self.title.split() + timestamp)

  def genPltFile(self):
    outFile = open('%s.plt' % self.title, 'w')

    # Write boilerplate
    outFile.write('set title "%s"\n' % self.title)
    outFile.write('set key top left\n')
    outFile.write('set grid\n')
    outFile.write('set xdata time\n')
    outFile.write('set timefmt "%Y-%m-%d"\n')
    outFile.write('set terminal png size 1000,800\n')
    outFile.write('set output "%s.png"\n' % self.title)

    # Write plotting lines
    plotLines = ['"%s" using 1:2 title "%s" with lines' % ('%s.tab' % cleanse(county), county) for countyID, county in self.labels.iteritems()]
    outFile.write('plot %s\n' % ','.join(plotLines))
    outFile.close()

  def getInfectedCounts(self):
    return {countyID: countyGraph.getNumInfected() for (countyID, countyGraph) in self.countyGraphs.iteritems()}

  def flushInfectedCounts(self, infectedCounts, day, countyIDToOutputFile):
    '''
    0) Multiply all infectedCounts by self.scalingFactor
    1) Flush infected counts data for this day to the .tab files for each county
    2) Add infected counts to self.allInfectedCounts (for calculating mean-squared-error metric)
    '''
    # dict from county name => upscaled infected count, e.g. Lola=>207
    upscaledInfectedCounts = {self.labels[countyID]: infectedCount*self.scalingFactor for countyID, infectedCount in infectedCounts.iteritems()}
    
    todayDate = self.startDate + timedelta(days=day)
    todayDateString = todayDate.strftime('%Y-%m-%d')
    for countyID, outputFile in countyIDToOutputFile.iteritems():
      outputFile.write('%s\t%d\n' % (todayDateString, infectedCounts[countyID]*self.scalingFactor))

    self.allInfectedCounts[todayDateString] = upscaledInfectedCounts

  def infectCrossCounty(self):
    infectedCounts = self.getInfectedCounts()
    for countyNode in self.G.Nodes():
      for neighborID in countyNode.GetOutEdges():
        countyID = countyNode.GetId()
        if self.infectionSpreads(countyID, infectedCounts[countyID]):
          self.crossCountyInfections += 1
          self.countyGraphs[neighborID].infect()
        self.crossCountyAttempts += 1

  def infectionSpreads(self, countyID, numInfected):
    probSpreading = self.q*(numInfected/(self.countyGraphs[countyID].getNumNodes()))
    return random.random() < probSpreading

  def __str__(self):
    return json.dumps(self.simulationInfo, sort_keys=True, indent=4, separators=(',',' : '))

  @staticmethod
  def loadGraphAndLabels(prefix):
    G = snap.LoadEdgeList(snap.PUNGraph, prefix + "_graph.txt", 0, 1)
    labels = MacroGraph.loadNodeLabels(prefix + "_labels.csv")
    return G, labels

  @staticmethod
  def loadNodeLabels(fn):
    inputFile = csv.reader(open(fn, 'rb'))
    labels = {}
    for n in inputFile:
      labels[int(n[0])] = n[1]
    return labels

def commentify(s, commentString='#'):
  return (commentString + s).strip().replace('\n', '\n%s' % commentString)

def cleanse(s):
  return s.replace(' ', '_')

"""
Basic graph validation below.
"""
def checkGraph(G, labels, Gname, Gnodes, Gedges, Gdegs):
  assert G.GetNodes() == Gnodes, "%s graph should have %d nodes but had %d" % (Gname, Gnodes, G.GetNodes())
  assert G.GetEdges() == Gedges, "%s graph should have %d edges but had %d" % (Gname, Gedges, G.GetEdges())
  for nId, name in labels.iteritems():
    deg = G.GetNI(nId).GetDeg()
    assert deg == Gdegs[nId], "Node %d (%s) in %s graph should have degree %d but had degree %d" % (nId, name, Gname, Gdegs[nId], deg)
  print "%s county graph is valid!" % Gname

def testSlGraph():
  Gname, Gnodes, Gedges = "Sierra Leone", 12, 20
  Gdegs = {0:2, 1:4, 2:5, 3:2, 4:2, 5:3, 6:5, 7:4, 8:2, 9:4, 10:5, 11:2}
  G, labels = MacroGraph.loadGraphAndLabels(SIERRA_LEONE_PREFIX)
  checkGraph(G, labels, Gname, Gnodes, Gedges, Gdegs)

def testLibGraph():
  Gname, Gnodes, Gedges = "Liberia", 15, 18
  Gdegs = {0:3, 1:4, 2:1, 3:3, 4:1, 5:3, 6:2, 7:1, 8:3, 9:2, 10:2, 11:3, 12:3, 13:3, 14:2}
  G, labels = MacroGraph.loadGraphAndLabels(LIBERIA_PREFIX)
  checkGraph(G, labels, Gname, Gnodes, Gedges, Gdegs)

def testGuinGraph():
  Gname, Gnodes, Gedges = "Guinea", 20, 34
  Gdegs = {0:2, 1:2, 2:6, 3:4, 4:5, 5:3, 6:2, 7:3, 8:3, 9:3, 10:4, 11:2, 12:3, 13:2, 14:4, 15:4, 16:4, 17:4, 18:6, 19:2}
  G, labels = MacroGraph.loadGraphAndLabels(GUINEA_PREFIX)
  checkGraph(G, labels, Gname, Gnodes, Gedges, Gdegs)

if __name__ == '__main__':
  testSlGraph()
  testLibGraph()
  testGuinGraph()