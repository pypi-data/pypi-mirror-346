from typing import List, Optional

from trustwise.sdk.types import SensitivityRequest, SensitivityResponse


class SensitivityMetric:
    """Sensitivity metric for evaluating response sensitivity."""
    def __init__(self, client) -> None:
        self.client = client
        self.base_url = client.config.get_alignment_url("v1")

    def evaluate(
        self,
        *,
        response: str,
        topics: List[str],
        query: Optional[str] = None,
        **kwargs
    ) -> SensitivityResponse:
        """
        Evaluate the sensitivity of a response.

        Args:
            response: The response string (required)
            topics: List of topics to check for sensitivity (required)
            query: The input query string (optional)

        Returns:
            SensitivityResponse containing the evaluation results
        """
        req = SensitivityRequest(response=response, topics=topics, query=query, **kwargs)
        result = self.client._post(
            endpoint=f"{self.base_url}/sensitivity",
            data=req.to_dict()
        )
        return SensitivityResponse(**result)

    def batch_evaluate(
        self,
        inputs: List[SensitivityRequest]
    ) -> List[SensitivityResponse]:
        """Evaluate multiple inputs for sensitivity."""
        raise NotImplementedError("Batch evaluation not yet supported")

    def explain(
        self,
        *,
        response: str,
        topics: List[str],
        query: Optional[str] = None,
        **kwargs
    ) -> dict:
        """Get detailed explanation of the sensitivity evaluation."""
        # req = SensitivityRequest(response=response, topics=topics, query=query)
        raise NotImplementedError("Explanation not yet supported") 