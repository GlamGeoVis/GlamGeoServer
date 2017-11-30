from flask import jsonify, request, Blueprint
import numpy as np
from flask_cors import cross_origin
from GlamGeoServer.filters import filterData
from GlamGeoServer.clustering import clusterInRadius
from GlamGeoServer.data import getData


routes = Blueprint('routes', 'routes')

def buildGlyph(dataFrame):
    # This will need to change depending on the columns on the .csv file
    bins = np.arange(1700, 2010 + 50, 50)
    counts, years = np.histogram(dataFrame['year'], bins=bins)
    yearCounts = { str(y): int(c) for y, c in zip(years, counts) }
    return {
        'lat': dataFrame['latitude'].mean(),
        'lng': dataFrame['longitude'].mean(),
        'count': len(dataFrame),
        'years': yearCounts
    }

def aggregateClusters(dataFrame):
    result = []
    for cluster in dataFrame.groupby('cluster'):
        result.append(buildGlyph(cluster[1]))  # cluster[1] contains actual dataFrame

    return result


def aggregateYears(dataFrame):
    return {str(index): int(value) for index, value in dataFrame['year'].value_counts().iteritems()}


def query(params):
    filters = {
        'latitude': [params['viewport']['southWest']['lat'], params['viewport']['northEast']['lat']],
        'longitude': [params['viewport']['southWest']['lng'], params['viewport']['northEast']['lng']]
    }
    filters.update({'years': [params['range']['start'], params['range']['end']]})

    if 'title' in params:
        filters['title'] = params['title']

    if 'author' in params:
        filters['author'] = params['author']

    return clusterInRadius(filterData(filters, getData()), params['viewport'])


@routes.route('/jsonData', methods=['POST'])
@cross_origin()
def getClusters():
    dataFiltered = query(request.get_json())

    yearsData = aggregateYears(dataFiltered)
    clusterData = aggregateClusters(dataFiltered)

    return jsonify({
        'total': len(dataFiltered),
        'clusters': clusterData,
        'years': yearsData
    })

@routes.route('/clusterDetails', methods=['POST'])
@cross_origin()
def clusterDetails():
    params = request.get_json()
    data = query(params)
    clusters = list(data.groupby('cluster'))
    cluster = clusters[params['id']][1]  # cluster[1] contains actual dataFrame
    return cluster.to_json(orient="records")

