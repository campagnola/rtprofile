"""Combined profiler window with all profilers in tabs."""
from . import qt_shim as Qt
from .qt_profiler import QtEventProfiler
from .memory_profiler import MemoryProfiler
from .function_profiler import FunctionProfiler


class ProfilerWindow(Qt.QMainWindow):
    """Performance profiling window for real-time debugging.

    Provides separate function profiling (yappi), Qt event profiling (ProfiledQApplication),
    and memory profiling (guppy/heapy) with clean separation of concerns.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Profiler')
        self.resize(1300, 800)

        # Central widget with tabs
        central_widget = Qt.QWidget()
        self.setCentralWidget(central_widget)
        layout = Qt.QVBoxLayout(central_widget)

        # Tab widget for different profiling views
        self.tab_widget = Qt.QTabWidget()
        layout.addWidget(self.tab_widget)

        # Create profiler instances
        self.qt_profiler = QtEventProfiler(self)
        self.memory_profiler = MemoryProfiler(self)
        self.function_profiler = FunctionProfiler(self)

        # Add tabs
        self.tab_widget.addTab(self.function_profiler.widget, "Function Profiler")
        self.tab_widget.addTab(self.qt_profiler.widget, "Qt Event Profile")
        self.tab_widget.addTab(self.memory_profiler.widget, "Memory Profile")

    def closeEvent(self, event):
        """Stop all Qt profiles when the profiler window closes."""
        # Stop all active Qt profiles
        app = Qt.QApplication.instance()
        if hasattr(app, 'stop_all_profiles'):
            app.stop_all_profiles()

        # Accept the close event
        super().closeEvent(event)
