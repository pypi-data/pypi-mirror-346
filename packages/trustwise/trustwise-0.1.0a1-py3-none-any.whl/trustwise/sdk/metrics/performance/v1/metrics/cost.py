from typing import Any, Dict, List, Optional

from trustwise.sdk.types import CostRequest, CostResponse


class CostMetric:
    """Cost metrics evaluator."""
    def __init__(self, client) -> None:
        self.client = client
        self.base_url = client.config.get_performance_url("v1")

    def evaluate(
        self,
        request: object = None,
        *,
        model_name: Optional[str] = None,
        model_type: Optional[str] = None,
        model_provider: Optional[str] = None,
        number_of_queries: Optional[int] = None,
        total_prompt_tokens: Optional[int] = None,
        total_completion_tokens: Optional[int] = None,
        total_tokens: Optional[int] = None,
        instance_type: Optional[str] = None,
        average_latency: Optional[float] = None,
        cost_map_name: str = "sys",
        **kwargs
    ) -> CostResponse:
        """
        Evaluate cost metrics.
        Accepts either a CostRequest object or keyword arguments.
        """
        if isinstance(request, CostRequest):
            req = request
        elif model_name and model_type and model_provider and number_of_queries is not None:
            req = CostRequest(
                model_name=model_name,
                model_type=model_type,
                model_provider=model_provider,
                number_of_queries=number_of_queries,
                total_prompt_tokens=total_prompt_tokens,
                total_completion_tokens=total_completion_tokens,
                total_tokens=total_tokens,
                instance_type=instance_type,
                average_latency=average_latency
            )
        else:
            raise ValueError("Must provide either a CostRequest or all required keyword arguments.")

        # Validate model type
        if req.model_type not in ["LLM", "Reranker"]:
            raise ValueError("model_type must be either 'LLM' or 'Reranker'")

        # Validate and prepare data based on provider
        if req.model_type == "LLM":
            if req.total_prompt_tokens is None or req.total_completion_tokens is None:
                raise ValueError("total_prompt_tokens and total_completion_tokens are required for LLM providers")
            if req.model_provider == "HuggingFace":
                if req.instance_type is None or req.average_latency is None:
                    raise ValueError("instance_type and average_latency are required for Hugging Face")
            elif req.model_provider in ["OpenAI", "Azure"]:
                if req.instance_type is not None:
                    raise ValueError(f"instance_type is not allowed for {req.model_provider}")
                if req.average_latency is not None:
                    raise ValueError(f"average_latency is not allowed for {req.model_provider}")
        else:  # Reranker
            if req.model_provider == "Together Reranker":
                if req.total_tokens is None:
                    raise ValueError("total_tokens is required for Together Reranker")
            else:  # Azure Reranker, Cohere Reranker
                if req.instance_type is not None:
                    raise ValueError(f"instance_type is not allowed for {req.model_provider}")
                if req.average_latency is not None:
                    raise ValueError(f"average_latency is not allowed for {req.model_provider}")

        result = self.client._post(
            endpoint=f"{self.base_url}/cost",
            data=req.model_dump() if hasattr(req, "model_dump") else req.dict()
        )
        return CostResponse(**result)

    def batch_evaluate(
        self,
        inputs: List[CostRequest]
    ) -> List[CostResponse]:
        """Evaluate multiple inputs for cost."""
        raise NotImplementedError("Batch evaluation not yet supported")

    def explain(
        self,
        request: CostRequest
    ) -> Dict[str, Any]:
        """Get detailed explanation of the cost evaluation."""
        raise NotImplementedError("Explanation not yet supported") 