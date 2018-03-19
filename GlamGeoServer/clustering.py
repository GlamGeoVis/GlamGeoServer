from random import randint
from datetime import datetime

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


def clusterJava(dataFrame):
    def get_nodes(node, max_depth, depth):
        leafs = []
        children = node.getChildren()
        if children and depth < max_depth:
            for child in children:
                childleafs = get_nodes(child, max_depth, depth+1)
                leafs = leafs + childleafs
        else:
            leafs.append(node)
        return leafs


    dataFrame['cluster'] = None
    from py4j.java_gateway import JavaGateway, GatewayParameters
    gateway = JavaGateway(gateway_parameters=GatewayParameters(auto_convert=True))

    grouped = dataFrame.groupby('location')
    locations = grouped.size().to_frame('size')
    locations['x'] = grouped.first()['x']
    locations['y'] = grouped.first()['y']

    locations_flat = locations.reset_index().as_matrix()

    print('starting java clusterer')
    cluster_result_json = gateway.entry_point.run(locations_flat)
    print('java clusterer done')
    gateway.close()

    # clusters = get_nodes(cluster_result, 9, 0)

    # i = 0
    # for cluster in clusters:
    #     locations = [node.getData().getGlyph().getID() for node in get_nodes(cluster, 10, 0)]
    #     dataFrame.loc[dataFrame['location'].isin(locations), 'cluster'] = i
    #     i += 1



    # return dataFrame
    return cluster_result_json












