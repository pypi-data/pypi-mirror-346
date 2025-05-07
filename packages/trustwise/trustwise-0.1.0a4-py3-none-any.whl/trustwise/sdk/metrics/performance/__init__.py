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

    def set_version(self, version: str) -> None:
        """
        Change the default version.

        Args:
            version: Version string (e.g., "v1")

        Raises:
            ValueError: If version is not supported. The error message will list available versions.
        """
        if version == "v1":
            self._current_version = self.v1
        else:
            raise ValueError(
                f"Performance API version {version} is not supported. "
                f"Available versions: {', '.join(['v1'])}"
            ) 