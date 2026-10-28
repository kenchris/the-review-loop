#!/usr/bin/env bash
# Builds deck.pptx and deck.pdf. Usage: ./make.sh [pptx|pdf|render 5 7 13]
python "$(dirname "$0")/make.py" "$@"
