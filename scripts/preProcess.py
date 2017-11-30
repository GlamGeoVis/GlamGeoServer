import sys

from GlamGeoServer.utils import cleanData

troveData_file = '../trove-dump-uniq.tsv'

print("Usage: preProcess.py <# data lines>")

cutoff = 0 #the entire file, default value
if len(sys.argv) > 1:
    cutoff = int(sys.argv[1])

userData = cleanData(troveData_file,cutoff)
sys.stdout = sys.__stdout__ #revert to print outs
#print(userData)


