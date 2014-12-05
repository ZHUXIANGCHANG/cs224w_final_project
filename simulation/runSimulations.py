import argparse
import json
import os
import sys
import random
sys.path.insert(0, '../macro_graph')
from macro_graph import MacroGraph

def parseArgs():
  parser = argparse.ArgumentParser(description='Run Ebola infection simulations.')
  parser.add_argument('simulationFile', help='The JSON file defining the parameters for the simulations.')
  args = parser.parse_args()
  simulationFile = args.simulationFile
  if not os.path.isfile(simulationFile) or not isJson(simulationFile):
    print >> sys.stderr, 'ERROR: Provided simulationFile must be a real JSON file'
    sys.exit(-1)
  return simulationFile

def isJson(f):
  return len(f) > 5 and f[-5:] == '.json'

def parseSimulationFile(simulationFile):
  with open(simulationFile, 'r') as f:
    simulations = json.loads( f.read() )
    return simulations

def main():
  simulations = parseSimulationFile(parseArgs())
  #random.seed(0)
  for simulation in simulations:
    print 'Starting simulation: ', simulation['title']
    G = MacroGraph(simulation)
    G.simulate()
    print ''

if __name__ == '__main__':
  main()