from pyproj import Proj

projection = Proj(init='EPSG:3857')


def parseRange(range_s):
    low_s, high_s = range_s.split('-')
    low = float(low_s)
    high = float(high_s)
    return low, high

def viewportToWebMercator(viewport):
    return (
        projection(min(180, viewport['northEast']['lng']), min(90, viewport['northEast']['lat'])),
        projection(max(-180, viewport['southWest']['lng']), max(-90, viewport['southWest']['lat']))
    )

def setEuclideanCoordinates(data):
    xy = map(lambda x: projection(x[0], x[1]), zip(data['longitude'], data['latitude']))
    x, y = zip(*xy)
    data['x'] = x
    data['y'] = y
