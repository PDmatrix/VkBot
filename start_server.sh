#!/usr/bin/env bash
venv/bin/python -m bottle --server bjoern --bind localhost:5000 src.app:bottle
