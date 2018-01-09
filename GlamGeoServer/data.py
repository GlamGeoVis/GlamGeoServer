import pandas as pd

from GlamGeoServer.utils import setEuclideanCoordinates

_data = None

def loadData(fileName):
    global _data
    print('reading %s' % fileName)
    _data = pd.read_csv(fileName, delimiter='\t')
    print(str(_data.shape[0]) + ' data points')
    print('data loaded, calculating euclidean coordinates')
    setEuclideanCoordinates(_data)
    groups = _data.groupby(['latitude', 'longitude'])
    _data['location'] = groups.grouper.group_info[0]
    print(str(groups.ngroups) + ' locations')

def getData():
    if _data is None:
        raise Exception("No data loaded")
    else:
        return _data
