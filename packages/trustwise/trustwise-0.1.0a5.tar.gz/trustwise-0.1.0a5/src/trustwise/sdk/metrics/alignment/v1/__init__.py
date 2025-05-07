from trustwise.sdk.metrics.alignment.v1.metrics.clarity import ClarityMetric
from trustwise.sdk.metrics.alignment.v1.metrics.formality import FormalityMetric
from trustwise.sdk.metrics.alignment.v1.metrics.helpfulness import HelpfulnessMetric
from trustwise.sdk.metrics.alignment.v1.metrics.sensitivity import SensitivityMetric
from trustwise.sdk.metrics.alignment.v1.metrics.simplicity import SimplicityMetric
from trustwise.sdk.metrics.alignment.v1.metrics.tone import ToneMetric
from trustwise.sdk.metrics.alignment.v1.metrics.toxicity import ToxicityMetric
from trustwise.sdk.metrics.base import BaseAlignmentMetric


class AlignmentMetricsV1(BaseAlignmentMetric):
    """Alignment metrics for version 1 of the API."""
    
    def __init__(self, client) -> None:
        """Initialize the safety metrics."""
        base_url = client.config.get_safety_url("v3")
        super().__init__(client, base_url=base_url, version="v3")
        self.clarity = ClarityMetric(client)
        self.helpfulness = HelpfulnessMetric(client)
        self.formality = FormalityMetric(client)
        self.simplicity = SimplicityMetric(client)
        self.tone = ToneMetric(client)
        self.toxicity = ToxicityMetric(client)
        self.sensitivity = SensitivityMetric(client)
