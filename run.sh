#!/usr/bin/env python
export PREFIX=/usr  # for a standard install, I also use PREFIX=$CONDA_PREFIX if I've installed into an activated conda env
export QT_QPA_PLATFORM=offscreen  # Allow QT/QGIS to run headless
export PYTHONPATH=$PREFIX/share/qgis/python/plugins/processing:$PREFIX/share/qgis/python:$PYTHONPATH
python test_qgis.py
