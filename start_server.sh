#!/usr/bin/env bash
venv/bin/gunicorn --bind localhost:5000 --workers=3 --worker-class="meinheld.gmeinheld.MeinheldWorker" src.app:app
