"""
This script will look at the parsed csvs and generate the
.tab and .plt files needed for gnuplot to generate the
plots of total confirmed cases over time.
"""
import sys
import os
import csv
import subprocess

def getTabFilename(prefix, county):
  return ('%s %s.tab' % (prefix, county)).replace(' ', '_')

def writeCountyTabFiles(prefix, inName):
  inFile = csv.reader(open(inName, 'rb'))

  # Extract county names
  header = inFile.next()
  counties = header[1:]

  # Extract county data over time
  countyData = []
  for c in counties:
    countyData.append([])
  for line in inFile:
    date = line[0]
    for countyIndex in xrange(len(counties)):
      countyData[countyIndex].append((date, line[countyIndex+1]))
  
  # Write the tab files
  for countyIndex, county in enumerate(counties):
    outName = getTabFilename(prefix, county)
    outFile = open(outName, 'w')
    for dataPoint in countyData[countyIndex]:
      if isAnomaly(prefix, county, dataPoint): continue
      # There is this a weird spike in the data
      
      outFile.write('%s\t%s\n' % dataPoint)
    outFile.close()

  return counties

# Dealing with some ad hoc anomalies in the data
def isAnomaly(prefix, county, dataPoint):
  if prefix == 'lib' and county == 'Maryland' and int(dataPoint[1]) > 1000: return True
  if prefix == 'lib' and county == 'Montserrado' and dataPoint[0] == '2014-10-30': return True
  return False

def getTitle(prefix):
  countryName = 'Sierra Leone'
  if prefix == 'guin':
    countryName = 'Guinea'
  elif prefix == 'lib':
    countryName = 'Liberia'
  return 'Cumulative confirmed cases in %s by County' % countryName

def writeBoilerplate(prefix, outFile):
  title = getTitle(prefix)
  outFile.write('set title "%s"\n' % title)
  outFile.write('set key top left\n')
  outFile.write('set grid\n')
  outFile.write('set xdata time\n')
  outFile.write('set timefmt "%Y-%m-%d"\n')
  outFile.write('set terminal png size 1000,800\n')
  outFile.write('set output "%s.png"\n' % prefix)

def getPlotString(prefix, county):
  return '"%s" using 1:2 title "%s" with lines' % (getTabFilename(prefix, county), county)

def writePltFile(prefix, counties):
  outFile = open('%s.plt' % prefix, 'w')
  writeBoilerplate(prefix, outFile)
  plotParams = [getPlotString(prefix, c) for c in counties]
  outFile.write('plot %s\n' % ','.join(plotParams))
  outFile.close()

def generateFiles(csvFiles, csvSuffix='_parsed.csv'):
  for c in csvFiles:
    prefix = os.path.basename(os.path.normpath(c))[:-len(csvSuffix)]
    counties = writeCountyTabFiles(prefix, c)
    writePltFile(prefix, counties)
    subprocess.call(['gnuplot', '%s.plt' % prefix])

def printUsage():
  print "Usage: python generate_plots.py <parsed data file 1> <parsed data file 2> ... "

def main():
  if len(sys.argv) < 2:
    printUsage()
    sys.exit(1)

  generateFiles(sys.argv[1:])

if __name__ == '__main__':
  main()