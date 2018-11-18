#!/usr/bin/env bash
venv/bin/gunicorn --bind localhost:5001 --workers=3 -k meinheld.gmeinheld.MeinheldWorker src.app:app