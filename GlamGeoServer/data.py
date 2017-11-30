import pandas as pd

from GlamGeoServer.utils import setEuclideanCoordinates

_data = None

def loadData(fileName):
    global _data
    print('reading %s' % fileName)
    _data = pd.read_csv(fileName, delimiter='\t')
    print('data loaded, calculating euclidean coordinates')
    setEuclideanCoordinates(_data)

def getData():
    if _data is None:
        raise Exception("No data loaded")
    else:
        return _data
