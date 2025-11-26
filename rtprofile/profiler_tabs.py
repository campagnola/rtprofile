from . import qt_shim as Qt
from .qt_profiler import QtEventProfiler
from .memory_profiler import MemoryProfiler
from .function_profiler import FunctionProfiler


class ProfilerTabs(Qt.QWidget):
    """Combined profiler widget with function, Qt event, and memory profilers in tabs.

    This is a QWidget that can be embedded in existing applications
    or shown standalone.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout
        layout = Qt.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Tab widget for different profiling views
        self.tab_widget = Qt.QTabWidget()
        layout.addWidget(self.tab_widget)

        # Create profiler instances
        self.function_profiler = FunctionProfiler(self)
        self.qt_profiler = QtEventProfiler(self)
        self.memory_profiler = MemoryProfiler(self)

        # Add tabs
        self.tab_widget.addTab(self.function_profiler.widget, "Function Profiler")
        self.tab_widget.addTab(self.qt_profiler.widget, "Qt Event Profile")
        self.tab_widget.addTab(self.memory_profiler.widget, "Memory Profile")

    def closeEvent(self, event):
        """Stop all Qt profiles when the widget closes."""
        # Stop all active Qt profiles
        app = Qt.QApplication.instance()
        if hasattr(app, 'stop_all_profiles'):
            app.stop_all_profiles()

        # Accept the close event
        super().closeEvent(event)
