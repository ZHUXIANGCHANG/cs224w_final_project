import csv
import sys
import os
import glob

CUMULATIVE_CONFIRMED = 'cum_confirmed'
NUM_COUNTIES = 12

"""
Parse all the raw csvs containing Sierra Leone data
to generate a single csv containing the change in 
cumulative confirmed cases over time in each county.
"""
def parseCsvs(inPath, outFile):
  # Setup
  writer = csv.writer(outFile)
  currwd = os.getcwd()
  os.chdir(inPath)

  inFiles = glob.glob('*.csv')
  firstFile = True
  for inName in inFiles:
    inFile = csv.reader(open(inName, 'rU'))
    firstLine = True
    for line in inFile:
      if (firstLine and firstFile) or line[1] == CUMULATIVE_CONFIRMED:
        writer.writerow(line[0:1] + line[2:2+NUM_COUNTIES])
        if not firstLine: break
        if firstLine: firstLine = False
        if firstFile: firstFile = False

  # Restore
  os.chdir(currwd)

def printUsage():
  print "Usage: python parse_sl_csvs <path to directory containing input csv files>"

def main(outFilename='sl_parsed.csv'):
  if len(sys.argv) != 2:
    printUsage()
    sys.exit(1)
  
  parseCsvs(sys.argv[1], open(outFilename, 'wb'))

if __name__ == '__main__':
  main()