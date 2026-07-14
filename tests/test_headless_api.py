"""Tests for the headless collection API used by acq4-mcp to drive the profiler widgets.

Each profiler exposes public start_session/stop_session/take_snapshot methods that the UI
buttons also call, so data is collectable without simulating clicks.
"""

import time

import pyqtgraph as pg
import pytest


@pytest.fixture(scope='module')
def qapp():
    return pg.mkQApp()


def test_function_profiler_start_stop_session_returns_result(qapp):
    from rtprofile.function_profiler import FunctionProfiler, ProfileResult

    fp = FunctionProfiler(parent_widget=None)
    fp.start_session(name='unit')
    sum(range(1000))
    result = fp.stop_session()
    assert isinstance(result, ProfileResult)
    assert result in fp.profile_results
    assert result.name == 'unit'


def test_memory_profiler_take_snapshot_returns_snapshot(qapp):
    guppy = pytest.importorskip('guppy')
    from rtprofile.memory_profiler import MemoryProfiler, MemorySnapshot

    mp = MemoryProfiler(parent_widget=None)
    snap = mp.take_snapshot(name='unit')
    assert isinstance(snap, MemorySnapshot)
    assert snap in mp.snapshots


def test_qt_profiler_requires_profiled_qapp_gracefully(qapp):
    # With a plain QApplication (no start_profile), start_session should raise a clear
    # error rather than AttributeError.
    from rtprofile.qt_profiler import QtEventProfiler

    qp = QtEventProfiler(parent_widget=None)
    if not hasattr(qapp, 'start_profile'):
        with pytest.raises(RuntimeError):
            qp.start_session(name='unit')
