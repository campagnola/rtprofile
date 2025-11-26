# rtprofile - Real-Time Profiling for Python

Real-time profiling tools designed for debugging running Python applications where traditional debugging is challenging.

## Features

- **Function Profiler**: Thread-aware function profiling using Python 3.12+ `setprofile_all_threads`
- **Memory Profiler**: Snapshot-based memory profiling with heap analysis (requires guppy3)
- **Qt Event Profiler**: Qt event loop profiling for PyQt/PySide applications
- **Combined Widget**: Tabbed interface with all profilers in one window

## Requirements

- Python 3.12+ (required for `threading.setprofile_all_threads()`)
- PyQtGraph (for Qt GUI support)
- Guppy3 (optional, for memory profiling)

## Installation

```bash
pip install rtprofile

# With memory profiling support
pip install rtprofile[memory]
```

## Usage

### Without Qt (headless profiling)

```python
from rtprofile import Profile

# Start profiling
prof = Profile()
prof.start()

# Your code here
...

# Stop and analyze
prof.stop()
prof.print_call_tree()
```

### With Qt GUI

```python
from PyQt5.QtWidgets import QApplication
from rtprofile import FunctionProfiler, MemoryProfiler, QtEventProfiler, ProfilerWindow

app = QApplication([])

# Individual profilers
function_profiler = FunctionProfiler()
function_profiler.widget.show()

# Or use the combined window
profiler_window = ProfilerWindow()
profiler_window.show()

app.exec()
```

### Code Editor Integration

Configure which code editor opens when double-clicking call locations:

```python
from rtprofile import set_code_editor

# Use a specific editor
set_code_editor('vscode')  # or 'pycharm', 'sublime'

# Or provide a custom command template
set_code_editor('code -g "{fileName}":{lineNum}')
```

## License

MIT
