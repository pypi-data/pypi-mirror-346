from trustwise.sdk.metrics.safety.v3 import SafetyMetricsV3


class SafetyMetrics:
    """
    Namespace for Safety Metrics API versions.
    """

    def __init__(self, client) -> None:
        """
        Initialize the Safety Namespace with all supported versions.
        """
        self._current_version = SafetyMetricsV3(client)
        self.v3 = self._current_version

        # Expose all v3 methods directly
        self.faithfulness = self._current_version.faithfulness
        self.answer_relevancy = self._current_version.answer_relevancy
        self.context_relevancy = self._current_version.context_relevancy
        self.summarization = self._current_version.summarization
        self.pii = self._current_version.pii
        self.prompt_injection = self._current_version.prompt_injection
    
    @property
    def version(self) -> str:
        """Get the current default version."""
        return self._current_version.version
