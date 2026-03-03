"""Tests for the function profiler core functionality (no Qt required)."""

import queue
import threading
import time
import pytest
from rtprofile.profiler import Profile


def dummy_function_a():
    """A simple function that calls another function."""
    time.sleep(0.01)  # 10ms
    dummy_function_b()


def dummy_function_b():
    """A simple function that takes some time."""
    time.sleep(0.01)  # 10ms


def dummy_recursive_function(n):
    """A recursive function for testing call depth."""
    if n <= 0:
        return
    time.sleep(0.001)  # 1ms
    dummy_recursive_function(n - 1)


def find_call(root_call, funcname):
    """Helper function to find a call record by function name."""
    if root_call.funcname == funcname:
        return root_call
    for child in root_call.children:
        result = find_call(child, funcname)
        if result is not None:
            return result
    return None


def test_basic_profiling():
    """Test basic profiling functionality: start, run function, stop, verify results."""
    prof = Profile()

    # Test that profile starts correctly
    prof.start()
    assert prof.start_time is not None
    assert prof.stop_time is None

    # Run our test function
    dummy_function_a()

    # Stop profiling
    prof.stop()
    assert prof.stop_time is not None
    assert prof.stop_time > prof.start_time

    # Get events and verify structure
    events = prof.get_events()
    assert isinstance(events, dict)

    tid = threading.current_thread().ident
    assert tid in events

    call_root = events[tid][0]
    call_a = find_call(call_root, 'dummy_function_a')
    assert call_a is not None
    assert call_a.parent.funcname == 'test_basic_profiling'
    call_b = [rec for rec in call_a.children if rec.funcname == 'dummy_function_b'][0]
    assert call_b.event_type == 'call'
    assert call_b.children[0].display_name == 'sleep'
    assert call_b.children[0].event_type == 'c_call'


def test_threaded_profiling():
    """Test that profiling works on threads created after profiling starts."""

    # start one thread before starting the profiler
    run_queue = queue.Queue()
    def run_from_queue():
        func = run_queue.get()
        func()
    thread1 = threading.Thread(target=run_from_queue)
    thread1.start()

    # start the profiler
    prof = Profile()
    prof.start()

    run_queue.put(dummy_function_a)

    # start another thread after the profiler
    thread2 = threading.Thread(target=dummy_function_a)
    thread2.start()

    thread1.join()
    thread2.join()

    prof.stop()

    # verify that the profiler caught events from both threads
    events = prof.get_events()
    
    call1 = find_call(events[thread1.ident][0], 'dummy_function_a')
    assert call1 is not None
    assert call1.parent.funcname.endswith('run_from_queue')

    call2 = find_call(events[thread2.ident][0], 'dummy_function_a')
    assert call2 is not None
    assert call2.parent.funcname == 'Thread.run'

