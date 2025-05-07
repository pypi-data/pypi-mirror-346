from trustwise.sdk.metrics.alignment.v1 import AlignmentMetricsV1


class AlignmentMetrics:
    """
    Namespace for Alignment Metrics API versions.
    """

    def __init__(self, client) -> None:
        """
        Initialize the Alignment Namespace with all supported versions.
        """
        self._current_version = AlignmentMetricsV1(client)
        self.v1 = self._current_version

        # Expose all v1 metric classes directly as attributes for the preferred style
        self.clarity = self._current_version.clarity
        self.formality = self._current_version.formality
        self.helpfulness = self._current_version.helpfulness
        self.simplicity = self._current_version.simplicity
        self.tone = self._current_version.tone
        self.toxicity = self._current_version.toxicity
        self.sensitivity = self._current_version.sensitivity

    @property
    def version(self) -> str:
        """Get the current default version."""
        return self._current_version.version
