from __future__ import division

import time
import json
from flask import Flask, send_from_directory, jsonify, request
import numpy as np
import pandas as pd
from flask_cors import cross_origin

from filters import filterData
from clustering import groupData


app = application = Flask(__name__, static_url_path='/')

# Load data for demo -- this will need to go at some point...
risse_data = pd.read_csv('glammap-risse-dump-authors.csv', delimiter='\t')

def buildGlyphFromPoints(points_json):
    # This will need to change depending on the columns on the .csv file
    pdf = pd.DataFrame(points_json)
    bins = np.arange(1700, 1940 + 50, 50)
    counts, years = np.histogram(pdf['year'], bins=bins)
    yearCounts = { str(y): int(c) for y, c in zip(years, counts) if c > 0}
    return {
        'lat': pdf['latitude'].mean(),
        'lng': pdf['longitude'].mean(),
        'count': len(pdf),
        'years': yearCounts
    }

def aggregateClusters(clusters):
    summary = []
    for cluster in clusters:
        glyphData = buildGlyphFromPoints(cluster)
        summary.append(glyphData)
    return summary

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
    clusters = groupData(data_filtered, params['viewport'])

    return data_filtered, clusters


@app.route('/jsonData', methods=['POST'])
@cross_origin()
def buildData():
    data_filtered, clusters = query(request.get_json())

    yearsData = aggregateYears(data_filtered)
    clusterData = aggregateClusters(clusters)

    return jsonify({
        'total': len(data_filtered),
        'clusters': clusterData,
        'years': yearsData
    })

@app.route('/clusterDetails', methods=['POST'])
@cross_origin()
def clusterDetails():
    params = request.get_json()
    data_filtered, clusters = query(params)
    return jsonify(clusters[params['id']])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)


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