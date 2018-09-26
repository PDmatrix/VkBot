#!/usr/bin/env bash
gunicorn --bind localhost:5000 --workers=3 --worker-class="meinheld.gmeinheld.MeinheldWorker" src.app:bottle