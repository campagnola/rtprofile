"""rtprofile - Real-time profiling tools for Python applications.

This package provides profiling tools designed for debugging running systems
where traditional debugging is challenging.

Main components:
- Profile: Headless function profiler (no Qt required)
- ProfileAnalyzer: Analyze profile results
- CallRecord, FunctionAnalysis, etc.: Profiling data structures

Qt-based widgets (import explicitly):
- rtprofile.function_profiler.FunctionProfiler: Function profiler widget
- rtprofile.memory_profiler.MemoryProfiler: Memory profiler widget
- rtprofile.qt_profiler.QtEventProfiler: Qt event profiler widget
- rtprofile.profiler_tabs.ProfilerTabs: Combined tabbed widget with all profilers

Usage without Qt:
    from rtprofile.profiler import Profile

    prof = Profile()
    prof.start()
    # Your code here
    prof.stop()
    prof.print_call_tree()

Usage with Qt widgets:
    from rtprofile.function_profiler import FunctionProfiler
    from rtprofile.code_editor import set_code_editor

    set_code_editor('vscode')

    profiler = FunctionProfiler(parent_widget=None)
    profiler.widget.show()

Combined tabbed widget:
    from rtprofile.profiler_tabs import ProfilerTabs

    tabs = ProfilerTabs()
    tabs.show()  # Or embed in your app
"""

__version__ = '1.0.0'
