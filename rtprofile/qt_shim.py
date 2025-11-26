"""Thin Qt shim to replace acq4.util.Qt

This module provides a unified Qt namespace similar to acq4.util.Qt,
using pyqtgraph's Qt compatibility layer.
"""
import pyqtgraph as pg

# Create one large namespace containing everything; pyqtgraph handles translation
# between different Qt versions
for mod in [pg.Qt, pg.Qt.QtGui, pg.Qt.QtCore, pg.Qt.QtTest, pg.Qt.QtWidgets]:
    ns = mod.__dict__.copy()
    # don't copy special variables like __name__, __file__, etc.
    for k in list(ns.keys()):
        if k.startswith('__'):
            ns.pop(k)
    globals().update(ns)

# signal disconnect with exception handling
# allows calling disconnect even if no connection currently exists
disconnect = pg.disconnect
