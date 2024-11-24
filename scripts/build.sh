#!/usr/bin/env sh

pip install -U pyinstaller
pip install .
pyinstaller -n organise_tv_shows ./organise_tv_shows/__main__.py --clean --onefile
