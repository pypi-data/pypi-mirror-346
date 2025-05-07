from typing import Any, Dict, List

from trustwise.sdk.metrics.base import BasePerformanceMetric, MetricEvaluator
from trustwise.sdk.metrics.performance.v1.metrics.cost import CostMetric
from trustwise.sdk.types import (
    CarbonRequest,
    CarbonResponse,
    CostRequest,
)


class CarbonMetric(MetricEvaluator[CarbonRequest, CarbonResponse]):
    """Carbon emissions metrics evaluator."""
    
    def _get_endpoint_name(self) -> str:
        return "carbon"


class PerformanceMetricsV1(BasePerformanceMetric):
    """
    Client for Trustwise Performance Metrics API v1.
    
    Provides methods to assess the performance of AI-generated content across various dimensions.
    Currently supports cost and carbon emission metrics.
    
    The cost metric supports different model types and providers with specific requirements:
    
    **Model Types:**
    - ``"LLM"`` - Language Model
    - ``"Reranker"`` - Reranking Model (case sensitive)
    
    **LLM Providers and Requirements:**
    
    *OpenAI:*
    - Required Fields:
      - ``total_prompt_tokens`` (positive integer)
      - ``total_completion_tokens`` (positive integer)
      - ``model_name`` (non-empty string)
      - ``model_type`` (must be "LLM")
      - ``model_provider`` (must be "OpenAI")
      - ``number_of_queries`` (positive integer)
    - Optional Fields:
      - ``cost_map_name`` (defaults to "sys")
    - Not Allowed:
      - ``instance_type``
      - ``average_latency``
    
    *Hugging Face:*
    - Required Fields:
      - ``total_prompt_tokens`` (positive integer)
      - ``total_completion_tokens`` (positive integer)
      - ``model_name`` (non-empty string)
      - ``model_type`` (must be "LLM")
      - ``model_provider`` (must be "HuggingFace")
      - ``number_of_queries`` (positive integer)
      - ``instance_type`` (non-empty string)
      - ``average_latency`` (positive number)
    - Optional Fields:
      - ``cost_map_name`` (defaults to "sys")
    
    *Azure:*
    - Required Fields:
      - ``total_prompt_tokens`` (positive integer)
      - ``total_completion_tokens`` (positive integer)
      - ``model_name`` (non-empty string)
      - ``model_type`` (must be "LLM")
      - ``model_provider`` (must be "Azure")
      - ``number_of_queries`` (positive integer)
    - Optional Fields:
      - ``cost_map_name`` (defaults to "sys")
    - Not Allowed:
      - ``instance_type``
      - ``average_latency``
    
    **Reranker Providers and Requirements:**
    
    *Azure Reranker:*
    - Required Fields:
      - ``model_name`` (non-empty string)
      - ``model_type`` (must be "Reranker")
      - ``model_provider`` (must be "Azure Reranker")
      - ``number_of_queries`` (positive integer)
    - Optional Fields:
      - ``cost_map_name`` (defaults to "sys")
    - Not Allowed:
      - ``instance_type``
      - ``average_latency``
    
    *Cohere Reranker:*
    - Required Fields:
      - ``model_name`` (non-empty string)
      - ``model_type`` (must be "Reranker")
      - ``model_provider`` (must be "Cohere Reranker")
      - ``number_of_queries`` (positive integer)
    - Optional Fields:
      - ``cost_map_name`` (defaults to "sys")
    - Not Allowed:
      - ``instance_type``
      - ``average_latency``
    
    *Together Reranker:*
    - Required Fields:
      - ``model_name`` (non-empty string)
      - ``model_type`` (must be "Reranker")
      - ``model_provider`` (must be "Together Reranker")
      - ``total_tokens`` (positive integer)
    - Optional Fields:
      - ``cost_map_name`` (defaults to "sys")
    - Not Allowed:
      - ``instance_type``
      - ``average_latency``
    """
    
    def __init__(self, client) -> None:
        """Initialize the Performance Metrics client for v1 API."""
        super().__init__(
            client=client,
            base_url=client.config.get_performance_url("v1"),
            version="v1"
        )
        self.cost = CostMetric(client)
        self.carbon = CarbonMetric(client)
        self._initialize_registry()
    
    def _initialize_registry(self) -> None:
        """Initialize the registry with all available metrics."""
        self._registry.register(CostRequest, self.cost.evaluate)
        self._registry.register(CarbonRequest, self.carbon.evaluate)
    
    def batch_evaluate(self, inputs: List[Any]) -> List[Any]:
        """Evaluate multiple inputs in a single request."""
        raise NotImplementedError("Batch evaluation not yet supported")

    def explain(self, *args, **kwargs) -> Dict[str, Any]:
        """Get detailed explanation of the evaluation."""
        raise NotImplementedError("Explanation not yet supported") 