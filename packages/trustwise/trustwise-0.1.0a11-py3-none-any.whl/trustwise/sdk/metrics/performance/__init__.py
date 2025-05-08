from trustwise.sdk.metrics.performance.v1 import PerformanceMetricsV1


class PerformanceMetrics:
    """
    Namespace for Performance Metrics API versions.
    """

    def __init__(self, client) -> None:
        """
        Initialize the Performance Namespace with all supported versions.
        """
        self._current_version = PerformanceMetricsV1(client)
        self.v1 = self._current_version

        # Expose all v1 methods directly
        self.cost = self._current_version.cost
        self.carbon = self._current_version.carbon
        self.explain = self._current_version.explain
        self.batch_evaluate = self._current_version.batch_evaluate

    @property
    def version(self) -> str:
        """Get the current default version."""
        return self._current_version.version
