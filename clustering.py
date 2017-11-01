from haversine import haversine

from tomcluster import tomcluster

def groupData(data, viewport):
    north = viewport['northEast']['lat']
    south = viewport['southWest']['lat']
    west = viewport['southWest']['lng']
    east = viewport['northEast']['lng']

    diagonal_distance = haversine((viewport['northEast']['lat'], viewport['northEast']['lng']),
                                  (viewport['southWest']['lat'], viewport['southWest']['lng'])
                                  )

    clusters = tomcluster(data, diagonal_distance / 10)

    return clusters
