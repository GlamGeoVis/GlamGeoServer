from geocluster import GeoCluster

from utils import parseRange

def groupData(data, lat_r, lng_r):
    lat_low, lat_high = parseRange(lat_r)
    lng_low, lng_high = parseRange(lng_r)

    # TODO: check lat / lng are not the wrong way around
    north, west, south, east = lat_low, lng_low, lat_high, lng_high

    cluster = GeoCluster()
    cluster.set_bounds(north, west, south, east)
    cluster.set_grid(15, 15)
    cluster.use_clustering(False)
    cluster.populate(data)

    # Flatten json structure
    clusters = [ c for row in cluster.to_json() for c in row ]
    # Remove empty clusters
    clusters = [ c for c in clusters if len(c['points'])>0 ]

    return clusters
