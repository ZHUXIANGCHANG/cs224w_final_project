import csv
from datetime import date, datetime, timedelta
import json
import os
import random
import snap
import sys

# Importing our micro graphs
sys.path.insert(0, '../micro_graph')
'''
Every time a new type of micro graph is created, be sure to add the necessary
import statement and update the GRAPH_TYPE_TO_CLASS dictionary accordingly.
'''
from micro_graph import MicroGraph

# Naming constants
SIERRA_LEONE_PREFIX = 'sl'
LIBERIA_PREFIX = 'lib'
GUINEA_PREFIX = 'guin'
COUNTRY_NAME_TO_PREFIX = {'sierra leone':SIERRA_LEONE_PREFIX, 'liberia':LIBERIA_PREFIX, 'guinea':GUINEA_PREFIX}
PREFIX_TO_SIMULATION_INTERVAL = {SIERRA_LEONE_PREFIX:(date(2014,8,12), date(2014,11,6)), LIBERIA_PREFIX:(date(2014,6,16), date(2014,11,2)), GUINEA_PREFIX:(date(2014,8,4), date(2014, 10, 01))}

"""
Class definition for the macro graph.
"""
class MacroGraph:
  def __init__(self, simulationInfo):
    self.simulationInfo = simulationInfo
    self.title = simulationInfo['Title']
    self.countryPrefix = COUNTRY_NAME_TO_PREFIX[simulationInfo["Country"].strip().lower()]
    self.startDate, self.endDate = PREFIX_TO_SIMULATION_INTERVAL[self.countryPrefix]
    self.duration = (self.endDate-self.startDate).days

    # Populate the macro graph structure
    cwd = os.getcwd()
    os.chdir('../macro_graph')
    self.G, self.labels = MacroGraph.loadGraphAndLabels(self.countryPrefix)
    os.chdir(cwd)
    # Generate the county graphs
    countyGraphTypes = simulationInfo['Counties']
    self.countyGraphs = {}
    for nID, county in self.labels.iteritems():
      countyInfo = countyGraphTypes[county] # dict, e.g. {"population": 358190, "graphType": "Small World"}
      graphType = countyInfo['graphType'].strip().lower()
      numNodes = countyInfo['population'] / 1000 # TODO: see how algorithm scales to larger graph sizes
      countyG = MicroGraph(graphType, numNodes)
      self.countyGraphs[nID] = countyG

  def simulate(self):
    # Open an output data file for each county
    countyIDToOutputFile = self.initializeOutputFiles()

    # Infect initial random county
    startCountyID, startCountyG = random.sample(self.countyGraphs.items(), 1)[0]
    startCountyG.infect()

    for day in xrange(self.duration):
      # Get number infected from each county
      infectedCounts = self.getInfectedCounts()
      # Flush infected counts data for this day to the .tab files for each county
      self.flushInfectedCounts(infectedCounts, day, countyIDToOutputFile)

      # Advance a day
      for countyID, countyGraph in self.countyGraphs.iteritems():
        countyGraph.advanceDay()

      # Attempt to infect neighbors
      self.infectCrossCounty()

    # Close all the output data files
    for countyID, outputFile in countyIDToOutputFile.iteritems():
      outputFile.close()

  def initializeOutputFiles(self):
    # Create output directory
    outputDir = self.generateOutputDirName()
    cwd = os.getcwd()
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

    # Return to original working directory
    os.chdir(cwd)

    return outputFiles

  def generateOutputDirName(self):
    timestamp = [datetime.now().strftime('%Y-%m-%d_%H-%M-%S')]
    return '_'.join(self.title.split() + timestamp)

  def getInfectedCounts(self):
    return {countyID : countyGraph.getNumInfected() for countyID, countyGraph in self.countyGraphs.iteritems()}

  def flushInfectedCounts(self, infectedCounts, day, countyIDToOutputFile):
    todayDate = self.startDate + timedelta(days=day)
    todayDateString = todayDate.strftime('%Y-%m-%d')
    for countyID, outputFile in countyIDToOutputFile.iteritems():
      outputFile.write('%s\t%d\n' % (todayDateString, infectedCounts[countyID]))

  def infectCrossCounty(self):
    infectedCounts = self.getInfectedCounts()
    for countyNode in self.G.Nodes():
      for neighborID in countyNode.GetOutEdges():
        if MacroGraph.infectionSpreads(infectedCounts[countyNode.GetId()]):
          self.countyGraphs[neighborID].infect()

  @staticmethod
  def infectionSpreads(numInfected):
    # TODO: Make this probabilistic
    return True

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