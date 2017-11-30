# GLAM Server
This is the Python backend for GLAM. You can find the frontend at [GlamGeoVis/GlamGeoMap](https://github.com/GlamGeoVis/GlamGeoMap).

# Docker
* This repository contains a Dockerfile that can be used to create a Docker image. The provided nginx configuration file in `config/nginx.conf.template` provides three endpoints, running on port 8000:
  * Trove backend endpoint `/trove`
  * Risse backend endpoint `/risse`
  * All other requests will be forwarded to `STATIC_FILES_URL`, this is where the files for the frontend can be found (eg. `/index.html` will forward to `{STATIC_FILES_URL}/index.html`. This setting can be found in `Dockerfile`, and is by default configured to an Amazon S3 bucket where the current build of the `GlamGeoVis/GlamGeoMap` master branch is automatically deployed.

# How to run
You can run either using Docker, or using a local python environment.
## Docker
* Make sure `STATIC_FILES_URL` in `Dockerfile` is set to the frontend files' location (your local deployment of `GlamGeoVis/GlamGeoMap` or Amazon S3).
* Build the image `docker build . -t glam_server`.
* Run and bind to a local port eg. `docker run -it -name glam_server -p 127.0.0.1:8888:8000 glam_server`.
* Server is now running at [http://localhost:8888](http://localhost:8888).

## Local python
* Use `python3`
* Make a [virtual environment](https://docs.python.org/3/library/venv.html).
* Install dependencies `pip install -r requirements.txt`.
* Set environmental variable `GLAM_DATA_FILE` to the data filename eg. `glammap-risse-dump-authors.csv` (if not set, the script will try to open `glammap-risse-dump-authors.csv` by default).
* Run using `python server.py`.
* Note that unlike the Docker setup, this will only serve a single API backend (so either Trove or Risse) on port `8000`.
