import argparse
import json
import os
import random
import sys

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
    simulations = json.loads(f.read())["Simulations"]
    return simulations

def printSimulationInfo(simulation):
  print json.dumps(simulation, indent=4, separators=(',',' : '))

def main():
  simulations = parseSimulationFile(parseArgs())
  for simulation in simulations:
    printSimulationInfo(simulation)

if __name__ == '__main__':
  main()