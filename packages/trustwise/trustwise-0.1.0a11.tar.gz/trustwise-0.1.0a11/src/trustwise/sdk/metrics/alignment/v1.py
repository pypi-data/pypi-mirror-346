from typing import Any, Dict, List

# ClarityMetric has been moved to metrics/clarity.py
# from trustwise.sdk.metrics.alignment.v1.metrics.clarity import ClarityMetric
from trustwise.sdk.metrics.alignment.v1.metrics.clarity import ClarityMetric
from trustwise.sdk.metrics.alignment.v1.metrics.formality import FormalityMetric
from trustwise.sdk.metrics.alignment.v1.metrics.helpfulness import HelpfulnessMetric
from trustwise.sdk.metrics.alignment.v1.metrics.sensitivity import SensitivityMetric
from trustwise.sdk.metrics.alignment.v1.metrics.simplicity import SimplicityMetric
from trustwise.sdk.metrics.alignment.v1.metrics.tone import ToneMetric
from trustwise.sdk.metrics.alignment.v1.metrics.toxicity import ToxicityMetric
from trustwise.sdk.metrics.base import BaseAlignmentMetric
from trustwise.sdk.types import (
    ClarityRequest,
    # FormalityRequest,
    # FormalityResponse,
    # HelpfulnessRequest,
    # HelpfulnessResponse,
    # SensitivityRequest,
    # SensitivityResponse,
    # SimplicityRequest,
    # SimplicityResponse,
    # ToneRequest,
    # ToneResponse,
    # ToxicityRequest,
    # ToxicityResponse,
)

# class HelpfulnessMetric(MetricEvaluator[HelpfulnessRequest, HelpfulnessResponse]):
#     """Helpfulness metric for evaluating response helpfulness."""
    
#     def _get_endpoint_name(self) -> str:
#         return "helpfulness"


# class ToxicityMetric(MetricEvaluator[ToxicityRequest, ToxicityResponse]):
#     """Toxicity metric for evaluating response toxicity."""
    
#     def _get_endpoint_name(self) -> str:
#         return "toxicity"


# class ToneMetric(MetricEvaluator[ToneRequest, ToneResponse]):
#     """Tone metric for evaluating response tone."""
    
#     def _get_endpoint_name(self) -> str:
#         return "tone"


# class FormalityMetric(MetricEvaluator[FormalityRequest, FormalityResponse]):
#     """Formality metric for evaluating response formality."""
    
#     def _get_endpoint_name(self) -> str:
#         return "formality"


# class SimplicityMetric(MetricEvaluator[SimplicityRequest, SimplicityResponse]):
#     """Simplicity metric for evaluating response simplicity."""
    
#     def _get_endpoint_name(self) -> str:
#         return "simplicity"


# class SensitivityMetric(MetricEvaluator[SensitivityRequest, SensitivityResponse]):
#     """Sensitivity metric for evaluating response sensitivity."""
    
#     def _get_endpoint_name(self) -> str:
#         return "sensitivity"


class AlignmentMetricsV1(BaseAlignmentMetric):
    """
    Client for Trustwise Alignment Metrics API v1.
    
    Provides methods to assess the quality of AI-generated content across various dimensions.
    """
    
    def __init__(self, client) -> None:
        """Initialize the Alignment Metrics client for v1 API."""
        super().__init__(
            client=client,
            base_url=client.config.get_alignment_url("v1"),
            version="v1"
        )
        # Initialize specific metric implementations as public attributes
        self.clarity = ClarityMetric(client)
        self.helpfulness = HelpfulnessMetric(client)
        self.formality = FormalityMetric(client)
        self.simplicity = SimplicityMetric(client)
        self.tone = ToneMetric(client)
        self.toxicity = ToxicityMetric(client)
        self.sensitivity = SensitivityMetric(client)
        
        # Set up the registry with handler methods
        self._initialize_registry()
    
    def _initialize_registry(self) -> None:
        """Initialize the registry with all available metrics."""
        self._registry.register(ClarityRequest, self.clarity.evaluate)
        from trustwise.sdk.types import HelpfulnessRequest
        self._registry.register(HelpfulnessRequest, self.helpfulness.evaluate)
        from trustwise.sdk.types import FormalityRequest
        self._registry.register(FormalityRequest, self.formality.evaluate)
        from trustwise.sdk.types import SimplicityRequest
        self._registry.register(SimplicityRequest, self.simplicity.evaluate)
        from trustwise.sdk.types import ToneRequest
        self._registry.register(ToneRequest, self.tone.evaluate)
        from trustwise.sdk.types import ToxicityRequest
        self._registry.register(ToxicityRequest, self.toxicity.evaluate)
        from trustwise.sdk.types import SensitivityRequest
        self._registry.register(SensitivityRequest, self.sensitivity.evaluate)

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

    def explain(self, *args, **kwargs) -> Dict[str, Any]:
        """Get detailed explanation of the evaluation.
        
        This method provides explanations for all available metrics.
        """
        # Still returns empty dictionary since all metric.explain() methods will raise NotImplementedError
        return {} 