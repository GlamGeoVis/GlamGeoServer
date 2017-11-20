from haversine import haversine

def distance(loc1, loc2):
    return haversine((loc1['latitude'], loc1['longitude']),
                     (loc2['latitude'], loc2['longitude'])
                     )

def get_close_points(point, dataset, delta):
    return list(filter(lambda point2: distance(point, point2) < delta, dataset))

def tomcluster(data, delta=10):
    dataset = data.to_dict('records')

    clusters = []
    while len(dataset) > 0:
        current_cluster = []
        current = dataset[0]
        current_cluster.append(current)
        dataset.remove(current)
        clusters.append(current_cluster)
        close_points = get_close_points(current, dataset, delta)
        for point in close_points:
            dataset.remove(point)
        current_cluster += close_points

    return clusters
