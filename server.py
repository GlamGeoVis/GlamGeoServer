from __future__ import division

from flask import Flask, send_from_directory, jsonify, request
import numpy as np
import pandas as pd

from filters import filterData
from clustering import groupData

app = Flask(__name__, static_url_path='/')

# Load data for demo -- this will need to go at some point...
risse_data = pd.read_csv('glammap-risse-dump.csv', delimiter='\t')

def prepareDataForClustering(data_pd):
    # This will need to change depending on the columns on the .csv file
    data_tmp = data_pd[['title', 'year', 'latitude', 'longitude']]
    data_tmp = data_tmp.rename(columns={'latitude': 'latti', 'longitude': 'longi'})
    data_c = data_tmp.T.to_dict().values()
    return data_c

def buildGlyphFromPoints(points_json):
    # This will need to change depending on the columns on the .csv file
    pdf = pd.DataFrame(points_json)
    bins = np.arange(1700,1940 + 50, 50)
    counts, years = np.histogram(pdf['year'], bins=bins)
    yearCounts = { y: c for y, c in  zip(years, counts) if c > 0}
    return {
        'lat': pdf['lat'].mean(),
        'lng': pdf['lng'].mean(),
        'count': len(pdf),
        'years': yearCounts
    }

def aggregateClusters(clusters):
    summary = []
    for cluster in clusters:
        glyphData = buildGlyphFromPoints(cluster['points'])
        summary.append(glyphData)
    return summary

@app.route('/jsonData/latitude/<lat_r>/longitude/<lng_r>/')
def buildData(lat_r, lng_r):
    filters = { 'latitude': lat_r, 'longitude': lng_r }
    filters.update(request.args.to_dict())
    data_filtered = filterData(filters, risse_data)

    data_prepared = prepareDataForClustering(data_filtered)

    clusters = groupData(data_prepared, lat_r, lng_r)
    data = aggregateClusters(clusters)
    return jsonify(data)

@app.route('/<path:path>')
def send_files(path):
    return send_from_directory('', path)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
