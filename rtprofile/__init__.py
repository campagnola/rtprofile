"""rtprofile - Real-time profiling tools for Python applications.

This package provides profiling tools designed for debugging running systems
where traditional debugging is challenging.

Main components:
- Profile: Headless function profiler (no Qt required)
- FunctionProfiler: Qt-based function profiler with GUI
- MemoryProfiler: Qt-based memory profiler with GUI (requires guppy3)
- QtEventProfiler: Qt event loop profiler with GUI
- ProfilerWindow: Combined window with all profilers in tabs

Usage without Qt:
    from rtprofile import Profile

    prof = Profile()
    prof.start()
    # Your code here
    prof.stop()
    prof.print_call_tree()

Usage with Qt:
    from rtprofile import ProfilerWindow, set_code_editor
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    set_code_editor('vscode')  # Configure code editor

    profiler = ProfilerWindow()
    profiler.show()

    app.exec()
"""

# Core profiler (no Qt required)
from .profiler import (
    Profile,
    CallRecord,
    ProfileAnalyzer,
    FunctionAnalysis,
    TreeDisplayData,
    ThreadDisplayData,
)

# Code editor configuration
from .code_editor import (
    set_code_editor,
    get_code_editor_command,
    invoke_code_editor,
)

# Qt-based profilers (only imported if Qt is available)
try:
    from .function_profiler import FunctionProfiler
    from .memory_profiler import MemoryProfiler
    from .qt_profiler import QtEventProfiler
    from .profiler_window import ProfilerWindow

    __all__ = [
        # Core profiler
        'Profile',
        'CallRecord',
        'ProfileAnalyzer',
        'FunctionAnalysis',
        'TreeDisplayData',
        'ThreadDisplayData',
        # Code editor
        'set_code_editor',
        'get_code_editor_command',
        'invoke_code_editor',
        # Qt profilers
        'FunctionProfiler',
        'MemoryProfiler',
        'QtEventProfiler',
        'ProfilerWindow',
    ]
except ImportError:
    # Qt not available - only export core profiler
    __all__ = [
        'Profile',
        'CallRecord',
        'ProfileAnalyzer',
        'FunctionAnalysis',
        'TreeDisplayData',
        'ThreadDisplayData',
        'set_code_editor',
        'get_code_editor_command',
        'invoke_code_editor',
    ]

__version__ = '0.1.0'
