import csv
import sys
import os
import glob

CUMULATIVE_CONFIRMED = 'Total cases of confirmed'

"""
Parse all the raw csvs containing Guinea data
to generate a single csv containing the change in 
cumulative confirmed cases over time in each county.

This is tricky because the schema of each raw csv file is different.
"""
def parseCsvs(inPath, outFile):
  # Setup
  writer = csv.writer(outFile)
  currwd = os.getcwd()
  os.chdir(inPath)

  inFiles = glob.glob('*.csv')
  counties, datesToCountyData = set(), {}
  for inName in inFiles:
    inFile = csv.reader(open(inName, 'rU'))
    header = inFile.next()
    csvCounties = header[3:]
    # Update set of counties
    for c in csvCounties:
      counties.add(c)
    # Look for line of interest
    for line in inFile:
      if line[1] == CUMULATIVE_CONFIRMED:
        # Parse out data
        countyData = {}
        date, data = line[0], line[3:]
        for i in xrange(len(csvCounties)):
          countyData[csvCounties[i]] = data[i] if data[i] else 0
        datesToCountyData[date] = countyData
        break

  # Convert counties to list to impose an ordering
  counties = list(counties)
  # We know have the data for each date: time to output a csv
  writer.writerow(['date'] + counties)
  prevCases = {}
  for date in sorted(datesToCountyData.keys()):
    countyData = datesToCountyData[date]
    row = [date]
    currCases = {} # Mapping from county to cases
    for county in counties:
      cases = countyData[county] if county in countyData else 0
      if county in prevCases and int(cases) < int(prevCases[county]):
        cases = prevCases[county]
      currCases[county] = cases
      row.append(cases)
    prevCases = dict(prevCases.items() + currCases.items())
    writer.writerow(row)

  # Restore
  os.chdir(currwd)

def printUsage():
  print "Usage: python parse_guin_csvs <path to directory containing input csv files>"

def main(outFilename='guin_parsed.csv'):
  if len(sys.argv) != 2:
    printUsage()
    sys.exit(1)
  
  parseCsvs(sys.argv[1], open(outFilename, 'wb'))

if __name__ == '__main__':
  main()