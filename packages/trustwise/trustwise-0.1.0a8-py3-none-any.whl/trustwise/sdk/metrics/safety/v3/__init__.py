from trustwise.sdk.metrics.base import BaseSafetyMetric
from trustwise.sdk.metrics.safety.v3.metrics.answer_relevancy import (
    AnswerRelevancyMetric,
)
from trustwise.sdk.metrics.safety.v3.metrics.context_relevancy import (
    ContextRelevancyMetric,
)
from trustwise.sdk.metrics.safety.v3.metrics.faithfulness import FaithfulnessMetric
from trustwise.sdk.metrics.safety.v3.metrics.pii import PIIMetric
from trustwise.sdk.metrics.safety.v3.metrics.prompt_injection import (
    PromptInjectionMetric,
)
from trustwise.sdk.metrics.safety.v3.metrics.summarization import SummarizationMetric


class SafetyMetricsV3(BaseSafetyMetric):
    """Safety metrics for version 3 of the API."""
    
    def __init__(self, client) -> None:
        """Initialize the safety metrics."""
        base_url = client.config.get_safety_url("v3")
        super().__init__(client, base_url=base_url, version="v3")
        self.faithfulness = FaithfulnessMetric(client)
        self.answer_relevancy = AnswerRelevancyMetric(client)
        self.context_relevancy = ContextRelevancyMetric(client)
        self.summarization = SummarizationMetric(client)
        self.pii = PIIMetric(client)
        self.prompt_injection = PromptInjectionMetric(client) 