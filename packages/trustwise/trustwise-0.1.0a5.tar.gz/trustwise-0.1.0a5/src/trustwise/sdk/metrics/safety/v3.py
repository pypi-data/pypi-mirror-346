from typing import Any, Dict, List, Optional, TypeVar

from trustwise.sdk.metrics.base import BaseSafetyMetric
from trustwise.sdk.metrics.safety.v3.metrics.answer_relevancy import (
    AnswerRelevancyMetric,
)
from trustwise.sdk.metrics.safety.v3.metrics.context_relevancy import (
    ContextRelevancyMetric,
)

# Import metric classes from metrics/ submodules
from trustwise.sdk.metrics.safety.v3.metrics.faithfulness import FaithfulnessMetric
from trustwise.sdk.metrics.safety.v3.metrics.pii import PIIMetric
from trustwise.sdk.metrics.safety.v3.metrics.prompt_injection import (
    PromptInjectionMetric,
)
from trustwise.sdk.metrics.safety.v3.metrics.summarization import SummarizationMetric
from trustwise.sdk.types import (
    AnswerRelevancyRequest,
    Context,
    ContextRelevancyRequest,
    FaithfulnessRequest,
    PIIRequest,
    PromptInjectionRequest,
    SummarizationRequest,
)

# Define generic type variables for request and response
TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")

class SafetyMetricsV3(BaseSafetyMetric):
    """Safety metrics implementation for version 3."""
    
    def __init__(self, client) -> None:
        super().__init__(
            client=client,
            base_url=client.config.get_safety_url("v3"),
            version="v3"
        )
        # Initialize specific metric implementations
        self.faithfulness = FaithfulnessMetric(client)
        self.answer_relevancy = AnswerRelevancyMetric(client)
        self.context_relevancy = ContextRelevancyMetric(client)
        self.summarization = SummarizationMetric(client)
        self.pii = PIIMetric(client)
        self.prompt_injection = PromptInjectionMetric(client)
        
        # Set up the registry with handler methods
        self._initialize_registry()

    def _initialize_registry(self) -> None:
        """Initialize the registry with all available metrics."""
        self._registry.register(FaithfulnessRequest, self.faithfulness.evaluate)
        self._registry.register(AnswerRelevancyRequest, self.answer_relevancy.evaluate)
        self._registry.register(ContextRelevancyRequest, self.context_relevancy.evaluate)
        self._registry.register(SummarizationRequest, self.summarization.evaluate)
        self._registry.register(PIIRequest, self.pii.evaluate)
        self._registry.register(PromptInjectionRequest, self.prompt_injection.evaluate)

    def batch_evaluate(self, inputs: List[Any]) -> List[Any]:
        """Evaluate multiple inputs in a single request.
        
        This method should be called with a list of specific metric request types.
        All requests in the list must be of the same type.
        """
        if not inputs:
            return []
            
        request_type = type(inputs[0])
        if not all(isinstance(x, request_type) for x in inputs):
            raise ValueError("All inputs must be of the same type")
            
        # Get the appropriate handler from the registry
        handler = self._registry.get_handler(inputs[0])
        if handler and callable(handler):
            # For now, still raise NotImplementedError since batch evaluation 
            # is not yet supported for any metrics
            raise NotImplementedError("Batch evaluation not yet supported")
        else:
            raise ValueError(f"Unsupported request type: {request_type}")

    def explain(self, query: str, response: str, context: Optional[Context] = None) -> Dict[str, Any]:
        """Get detailed explanation of the evaluation.
        
        This method provides explanations for all available metrics.
        """
        # Still returns empty dictionary since all metric.explain() methods will raise NotImplementedError
        return {} 