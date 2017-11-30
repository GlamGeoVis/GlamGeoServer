from sklearn.cluster import DBSCAN

from GlamGeoServer.utils import viewportToWebMercator


def clusterDBSCAN(dataFrame, viewport):
    print('starting clusterer')
    north = viewport['northEast']['lat']
    south = viewport['southWest']['lat']
    west = viewport['southWest']['lng']
    east = viewport['northEast']['lng']

    data_matrix = dataFrame.as_matrix(columns=('x', 'y'))

    # clusterer = KMeans(n_clusters=100)
    clusterer = DBSCAN(eps=(east-west) * 3e3, min_samples=10)
    print("starting fit")
    clusterer.fit(data_matrix)
    dataFrame['cluster'] = clusterer.labels_
    print('clustering done')


def clusterInRadius(dataFrame, viewport):
    #  picks the first unclustered point from data, and groups everything within a radius
    #  of cluster_parameter * viewport.width in a cluster.
    print('starting clusterer')
    dataFrame['cluster'] = None
    cluster_parameter = .1
    (x0, y0), (x1, y1) = viewportToWebMercator(viewport)

    if x0 > 1e10 or x1 > 1e10 or y0 > 1e10 or y1 > 1e10:
        raise Exception('error in viewport coordinates')

    for i in range(0, len(dataFrame)):
        data_unclustered = dataFrame.loc[dataFrame['cluster'].isnull()]
        if len(data_unclustered) == 0:
            break
        currentPoint = data_unclustered.iloc[0]
        dataFrame.loc[
            dataFrame['cluster'].isnull() &
            ((
                 (dataFrame['x'] - currentPoint['x']) ** 2 +
                 (dataFrame['y'] - currentPoint['y']) ** 2
            ) < (cluster_parameter*(x1-x0))**2)
            , 'cluster'] = i

    print('custering done')
    return dataFrame

