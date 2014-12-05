import sys
import subprocess

if __name__ == '__main__':
  dataFiles = sys.argv[1:]
  for d in dataFiles:
    subprocess.call(['sort', d, '-o', d])
