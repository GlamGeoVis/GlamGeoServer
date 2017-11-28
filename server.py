from __future__ import division

import time
import json
from flask import Flask, send_from_directory, jsonify, request
import numpy as np
import pandas as pd
from flask_cors import cross_origin

from filters import filterData
from clustering import clusterDBSCAN, clusterTom

from pyproj import Proj

projection = Proj(init='EPSG:3857')  # https://gis.stackexchange.com/questions/44928/what-is-the-default-projection-in-leaflet

app = application = Flask(__name__, static_url_path='/')

# Load data for demo -- this will need to go at some point...
data_file = 'trove-dump-uniq-cleaned.tsv-authors.csv'
# data_file = 'glammap-risse-dump-authors.csv'
print('reading %s' % data_file)
risse_data = pd.read_csv(data_file, delimiter='\t')
print('data loaded, calculating euclidean coordinates')
xy = map(lambda x: projection(x[0], x[1]), zip(risse_data['latitude'], risse_data['longitude']))
x, y = zip(*xy)
risse_data['x'] = x
risse_data['y'] = y

def buildGlyphFromPoints(cluster):
    # This will need to change depending on the columns on the .csv file
    bins = np.arange(1700, 1940 + 50, 50)
    counts, years = np.histogram(cluster['year'], bins=bins)
    yearCounts = { str(y): int(c) for y, c in zip(years, counts) if c > 0}
    return {
        'lat': cluster['latitude'].mean(),
        'lng': cluster['longitude'].mean(),
        'count': len(cluster),
        'years': yearCounts
    }

def aggregateClusters(data):
    result = []
    for cluster in data.groupby('cluster'):
        glyphData = buildGlyphFromPoints(cluster[1])
        result.append(glyphData)

    return result

def aggregateYears(data):
    return {str(index): int(value) for index, value in data['year'].value_counts().iteritems()}

@app.route('/test', methods=['POST'])
def option():
    return jsonify(request.get_json())
    # return jsonify(['ok'])


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

    data_filtered = filterData(filters, risse_data)
    clusterTom(data_filtered, params['viewport'])

    return data_filtered


@app.route('/jsonData', methods=['POST'])
@cross_origin()
def buildData():
    data_filtered = query(request.get_json())

    yearsData = aggregateYears(data_filtered)
    clusterData = aggregateClusters(data_filtered)

    return jsonify({
        'total': len(data_filtered),
        'clusters': clusterData,
        'years': yearsData
    })

@app.route('/clusterDetails', methods=['POST'])
@cross_origin()
def clusterDetails():
    params = request.get_json()
    data = query(params)
    print(data)

    # return jsonify(clusters[params['id']])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True, use_reloader = True)
    # app.run(host='0.0.0.0', port=8000, debug=False, use_reloader = False)


# {
#   "viewport": {
#     "northEast": {
#       "lat": 51.951036645095904,
#       "lng": 10.228271484375002
#     },
#     "southWest": {
#       "lat": 46.98774725646568,
#       "lng": 0.9228515625000001
#     }
#   },
#   "range": {
#     "start": 1592,
#     "end": 1881
#   }
# }