# rtprofile - Real-Time Profiling for Python

Real-time profiling tools designed for debugging running Python applications where traditional debugging is challenging.

## Features

- **Function Profiler**: Thread-aware function profiling using Python 3.12+ `setprofile_all_threads`
- **Memory Profiler**: Snapshot-based memory profiling with heap analysis (requires guppy3)
- **Qt Event Profiler**: Qt event loop profiling for PyQt/PySide applications

## Requirements

- Python 3.12+ (required for `threading.setprofile_all_threads()`)
- PyQtGraph (optional, for Qt GUI widgets)
- Guppy3 (optional, for memory profiling)

## Installation

```bash
pip install rtprofile

# With memory profiling support
pip install rtprofile[memory]
```

## Usage

### Headless Profiling (no Qt required)

```python
from rtprofile.profiler import Profile

# Start profiling
prof = Profile()
prof.start()

# Your code here
...

# Stop and analyze
prof.stop()
prof.print_call_tree()

# Or analyze programmatically
from rtprofile.profiler import ProfileAnalyzer
analyzer = ProfileAnalyzer(prof)
function_lookup = analyzer.build_function_lookup()
```

### Qt Profiler Widgets

```python
from PyQt5.QtWidgets import QApplication
from rtprofile.function_profiler import FunctionProfiler
from rtprofile.memory_profiler import MemoryProfiler
from rtprofile.qt_profiler import QtEventProfiler
from rtprofile.profiler_tabs import ProfilerTabs
from rtprofile.code_editor import set_code_editor

app = QApplication([])

# Configure code editor for source navigation
set_code_editor('vscode')  # or 'pycharm', 'sublime'

# Create and show function profiler widget
function_profiler = FunctionProfiler(parent_widget=None)
function_profiler.widget.show()

# Or use the combined tabbed widget
profiler_tabs = ProfilerTabs()
profiler_tabs.show()

app.exec()
```

### Embedding Widgets

The profiler widgets can be embedded into existing applications:

```python
from rtprofile.function_profiler import FunctionProfiler

# Embed in your existing window
profiler = FunctionProfiler(parent=my_window)
my_layout.addWidget(profiler.widget)
```

### Code Editor Integration

Configure which code editor opens when double-clicking call locations:

```python
from rtprofile.code_editor import set_code_editor

# Use a specific editor
set_code_editor('vscode')  # or 'pycharm', 'sublime'

# Or provide a custom command template
set_code_editor('myeditor "{fileName}" --line {lineNum}')
```

## License

MIT
