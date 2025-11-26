#!/usr/bin/env python
"""Simple examples demonstrating rtprofile usage."""

# Example 1: Headless profiling (no Qt required)
print("=" * 60)
print("Example 1: Headless Profiling")
print("=" * 60)

from rtprofile.profiler import Profile
import time


def expensive_function():
    """Simulate an expensive operation."""
    time.sleep(0.05)


def main_work():
    """Main work function."""
    expensive_function()
    time.sleep(0.02)
    expensive_function()


# Create and start profiler
prof = Profile()
prof.start()

# Run the code you want to profile
main_work()

# Stop profiling
prof.stop()

# Print the call tree
prof.print_call_tree()

print("\n" + "=" * 60)
print("✓ Headless profiling completed")
print("=" * 60)


# Example 2: GUI Profiling (requires Qt)
print("\n" + "=" * 60)
print("Example 2: GUI Profiling")
print("=" * 60)
print("Run test_profiler.py to see the GUI profiler in action.")
print("=" * 60)
