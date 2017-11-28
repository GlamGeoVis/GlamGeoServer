from haversine import haversine
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN

def clusterDBSCAN(data, viewport):
    print('starting clusterer')
    north = viewport['northEast']['lat']
    south = viewport['southWest']['lat']
    west = viewport['southWest']['lng']
    east = viewport['northEast']['lng']

    data_matrix = data.as_matrix(columns=('x', 'y'))

    # clusterer = KMeans(n_clusters=100)
    clusterer = DBSCAN(eps=(east-west) * 3e3, min_samples=10)
    print("starting fit")
    clusterer.fit(data_matrix)
    data['cluster'] = clusterer.labels_
    print('clustering done')




def distance(loc1, loc2):
    return haversine((loc1['latitude'], loc1['longitude']),
                     (loc2['latitude'], loc2['longitude'])
                     )

def get_close_points(point, data, delta):
    distances = data[['latitude', 'longitude']].apply(lambda x: haversine(x, (point['latitude'], point['longitude'])), axis=1)
    return data[distances < delta]


def clusterTom(data, viewport):
    print('starting clusterer')
    print(type(data))
    diagonal_distance = haversine((viewport['northEast']['lat'], viewport['northEast']['lng']),
                                  (viewport['southWest']['lat'], viewport['southWest']['lng'])
                                  )

    delta = diagonal_distance / 10

    # clusters = []
    data.loc[0, 'cluster'] = 0
    while True:
        currentPoint = data.loc[0]
        close_points = get_close_points(currentPoint, data[data['cluster'].isnull()], delta)
        print('a')
        #
        # current = dataset[0]
        # current_cluster.append(current)
        # dataset.remove(current)
        # clusters.append(current_cluster)
        # close_points = get_close_points(current, dataset, delta)
        # for id, point in enumerate(close_points):
        #     print(point)
        #     dataset.remove(point)
        # current_cluster += close_points

