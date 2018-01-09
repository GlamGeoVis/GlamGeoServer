from flask import jsonify, request, Blueprint
import json
import numpy as np
from flask_cors import cross_origin
from GlamGeoServer.filters import filterData
from GlamGeoServer.clustering import clusterInRadius, clusterJava
from GlamGeoServer.data import getData


routes = Blueprint('routes', 'routes')

year_bins = np.arange(1700, 2010 + 50, 50)


def buildGlyph(dataFrame):
    # This will need to change depending on the columns on the .csv file
    counts, years = np.histogram(dataFrame['year'], bins=year_bins)
    # yearCounts = { str(y): int(c) for y, c in zip(years, counts) }
    return {
        'lat': round(dataFrame['latitude'].mean(), 8),
        'lng': round(dataFrame['longitude'].mean(), 8),
        'count': len(dataFrame),
        'years': counts.tolist(),
        'id': int(dataFrame['location'].iloc[0])
    }

def aggregateClusters(dataFrame):
    result = []
    for cluster in dataFrame.groupby('cluster'):
        result.append(buildGlyph(cluster[1]))  # cluster[1] contains actual dataFrame

    return result


def aggregateLocations(dataFrame, noKeys=True):
    print('aggregating locations')
    result = []
    for group in dataFrame.groupby('location'):
        glyph = buildGlyph(group[1])
        if noKeys:
            glyph = [glyph[key] for key in glyph]
        result.append(glyph)

    print('aggregating done')


    return result



def aggregateYears(dataFrame):
    return {str(index): int(value) for index, value in dataFrame['year'].value_counts().iteritems()}


def query(params):
    filters = {
        # 'latitude': [params['viewport']['southWest']['lat'], params['viewport']['northEast']['lat']],
        # 'longitude': [params['viewport']['southWest']['lng'], params['viewport']['northEast']['lng']]
    }
    filters.update({'years': [params['range']['start'], params['range']['end']]})

    if 'title' in params:
        filters['title'] = params['title']

    if 'author' in params:
        filters['author'] = params['author']

    # return clusterInRadius(filterData(filters, getData()), params['viewport'])
    # return clusterJava(filterData(filters, getData()), params['viewport'])
    return filterData(filters, getData())


@routes.route('/jsonData', methods=['POST'])
@cross_origin()
def getClusters():
    dataFiltered = query(request.get_json())
    print('after filtering: ' + str(dataFiltered.shape[0]) + ' data points')
    yearsData = aggregateYears(dataFiltered)

    result = jsonify({
        'total': len(dataFiltered),
        'clusters': json.loads(clusterJava(dataFiltered, request.get_json()['viewport'])),
        # 'data': json.loads(locations.reset_index().to_json()),
        'data': aggregateLocations(dataFiltered),
        'years': yearsData
    })

    return result

@routes.route('/clusterDetails', methods=['POST'])
@cross_origin()
def clusterDetails():
    params = request.get_json()
    data = query(params)
    clusters = list(data.groupby('cluster'))
    cluster = clusters[params['id']][1]  # cluster[1] contains actual dataFrame
    return cluster.to_json(orient="records")

