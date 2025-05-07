from typing import List, Optional

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
    ) -> dict:
        """Get detailed explanation of the cost evaluation."""
        # req = CostRequest(
        #     model_name=model_name,
        #     model_type=model_type,
        #     model_provider=model_provider,
        #     number_of_queries=number_of_queries,
        #     total_prompt_tokens=total_prompt_tokens,
        #     total_completion_tokens=total_completion_tokens,
        #     total_tokens=total_tokens,
        #     instance_type=instance_type,
        #     average_latency=average_latency
        # )
        raise NotImplementedError("Explanation not yet supported") 