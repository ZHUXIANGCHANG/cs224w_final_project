import csv
import sys
import os
import glob
import datetime

CUMULATIVE_CONFIRMED = 'Total confirmed cases'

"""
Parse all the raw csvs containing Liberia data
to generate a single csv containing the change in 
cumulative confirmed cases over time in each county.
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
        date, data = parseDate(line[0]), line[3:]
        for i in xrange(len(csvCounties)):
          countyData[csvCounties[i]] = data[i] if data[i] else 0
        datesToCountyData[date] = countyData
        break

  # Convert counties to list to impose an ordering
  counties = list(counties)
  # Remove "County" suffix if there
  trimmedCounties = [trimCounty(c) for c in counties]
  # We now have the data for each date: time to output a csv
  writer.writerow(['date'] + trimmedCounties)
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
    # Omit rows with entirely 0s
    if (sum([int(num) for num in row[1:]]) == 0): continue
    writer.writerow(row)

  # Restore
  os.chdir(currwd)

def trimCounty(c):
  countyStr = ' County'
  return c[:-len(countyStr)] if c.endswith(countyStr) else c

"""
Takes a date in month/day/year format and converts it to YYYY-MM-DD format.
"""
def parseDate(d):
  date = None
  try:
    date = datetime.datetime.strptime(d, '%m/%d/%Y')
  except ValueError:
    date = datetime.datetime.strptime(d, '%m/%d/%y')
  return date.strftime('%Y-%m-%d')

def printUsage():
  print "Usage: python parse_lib_csvs <path to directory containing input csv files>"

def main(outFilename='lib_parsed.csv'):
  if len(sys.argv) != 2:
    printUsage()
    sys.exit(1)
  
  parseCsvs(sys.argv[1], open(outFilename, 'wb'))

if __name__ == '__main__':
  main()