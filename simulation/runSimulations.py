import argparse
import csv
from datetime import datetime
import json
import os
import sys
import numpy as np
sys.path.insert(0, '../macro_graph')
from macro_graph import MacroGraph

COUNTRY_NAME_TO_PREFIX = {'Sierra Leone':'sl', 'Liberia':'lib', 'Guinea':'guin'}

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

def computeRootMeanSquareError(simAllInfectedCounts, countryName):
  '''
  @author Aaron Nagao

  @param dict from date => infectedCounts from that date
  @param countryName, e.g. 'Liberia'
  @return root-mean-squared-error of this simulation
  '''
  countryPrefix = COUNTRY_NAME_TO_PREFIX[countryName]
  
  # Import the csv to create trueAllInfectedCounts
  trueAllInfectedCounts = {} # same type as simAllInfectedCounts
  cwd = os.getcwd()
  os.chdir( os.path.join('..', 'reference', 'data', countryPrefix) )
  with open(countryPrefix + '_parsed.csv', mode='r') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
      date = row.pop('date')
      trueAllInfectedCounts[ date ] = {county: int(trueCount) for county,trueCount in row.iteritems()}
  os.chdir(cwd)

  # Create a difference vector to calculate root-mean-squared-error
  diff = np.fromiter( buildErrorVector(simAllInfectedCounts, trueAllInfectedCounts), dtype=np.int )
  rmse = np.linalg.norm(diff) / np.sqrt(len(diff))
  return rmse

def buildErrorVector(simAllInfectedCounts, trueAllInfectedCounts):
  '''
  For every date and for every county, yield simInfectedCount-trueInfectedCount
  In computeRootMeanSquareError(), this is passed into np.fromiter to build a vector containing all these differences.

  TODO: some true data is invalid ( 12 => 0 => 13 ), we should clean data BEFORE using this function
  '''
  for date,simInfectedCounts in simAllInfectedCounts.iteritems():
    try:
      trueInfectedCounts = trueAllInfectedCounts[date]
    except KeyError: # we simulated this date, but we don't have actual data for this date
      continue
    for county,simInfectedCount in simInfectedCounts.iteritems():
      trueInfectedCount = trueInfectedCounts[county]
      yield simInfectedCount-trueInfectedCount

def main():
  simulations = parseSimulationFile(parseArgs())
  #random.seed(0)

  # keep track of best value of parameters
  bestSimResults = {countryName: ('', float('inf')) for countryName in COUNTRY_NAME_TO_PREFIX} # dict: 'Sierra Leone' => (simulation['title'], rmse)
  
  for simulation in simulations:
    print 'Starting simulation: ', simulation['title']
    countryName = str(simulation['countryName'])
    G = MacroGraph(simulation)
    allInfectedCounts = G.simulate()
    
    # calculate RMSE, and keep a record ONLY IF its the lowest error so far
    rmse = computeRootMeanSquareError(allInfectedCounts, countryName)
    print 'Root-mean-squared-error was %.4f \n' % rmse
    if rmse < bestSimResults[countryName][1]:
      bestSimResults[countryName] = (simulation['title'], rmse)

  # write ONLY the best values of the parameters to bestSimulationResults.txt 
  with open('bestSimulationResults.txt', 'a') as outputfile: # append (keep all prior runs)
    outputfile.write( '# Simulation run on ' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '\n' )
    for countryName, bestSimResult in bestSimResults.iteritems():
      outputfile.write(bestSimResult[0] + '\t' + str(bestSimResult[1]) + '\n')
    outputfile.write('\n')

if __name__ == '__main__':
  main()
