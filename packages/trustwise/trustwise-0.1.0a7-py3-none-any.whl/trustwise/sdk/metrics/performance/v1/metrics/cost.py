from typing import List, Optional

from trustwise.sdk.types import CostRequest, CostResponse


class CostMetric:
    """Cost metrics evaluator."""
    def __init__(self, client) -> None:
        self.client = client
        self.base_url = client.config.get_performance_url("v1")

    def evaluate(
        self,
        *,
        model_name: str,
        model_type: str,
        model_provider: str,
        number_of_queries: int,
        total_prompt_tokens: int,
        total_completion_tokens: int,
        total_tokens: Optional[int] = None,
        instance_type: Optional[str] = None,
        average_latency: Optional[float] = None,
        **kwargs
    ) -> CostResponse:
        """
        Evaluate cost metrics.
        All arguments are required except those marked optional.
        """
        req = CostRequest(
            model_name=model_name,
            model_type=model_type,
            model_provider=model_provider,
            number_of_queries=number_of_queries,
            total_prompt_tokens=total_prompt_tokens,
            total_completion_tokens=total_completion_tokens,
            total_tokens=total_tokens,
            instance_type=instance_type,
            average_latency=average_latency,
            **kwargs
        )

        result = self.client._post(
            endpoint=f"{self.base_url}/cost",
            data=req.to_dict()
        )
        # Only validate and return CostResponse for 200 responses
        if isinstance(result, dict) and "detail" in result:
            # API error, raise as is
            raise Exception(f"API error: {result['detail']}")
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