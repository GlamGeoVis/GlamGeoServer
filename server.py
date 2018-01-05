import os
from flask import Flask

from GlamGeoServer.data import loadData
from GlamGeoServer.routes import routes

loadData(os.environ.get('GLAM_DATA_FILE') or 'data/glammap-risse-dump-authors.csv')
# loadData(os.environ.get('GLAM_DATA_FILE') or 'data/trove-dump-uniq-cleaned.tsv-authors.csv')

app = application = Flask(__name__, static_url_path='/')
app.register_blueprint(routes)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True, use_reloader = True)
    # app.run(host='0.0.0.0', port=8000, debug=False, use_reloader = False)
