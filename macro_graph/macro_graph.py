import csv
import json
import snap

SIERRA_LEONE_PREFIX = 'sl'
LIBERIA_PREFIX = 'lib'
GUINEA_PREFIX = 'guin'

"""
Class definition for the macro graph.
"""
class MacroGraph:
  def __init__(self, simulationInfo):
    self.simulationInfo = simulationInfo
    # TODO: Instantiate the graph

  def __str__(self):
    return json.dumps(self.simulationInfo, indent=4, separators=(',',' : '))

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