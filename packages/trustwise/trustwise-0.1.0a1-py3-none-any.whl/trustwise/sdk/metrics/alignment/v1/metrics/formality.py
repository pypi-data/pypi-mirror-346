from typing import Any, Dict, List

from trustwise.sdk.types import FormalityRequest, FormalityResponse


class FormalityMetric:
    """Formality metric for evaluating response formality."""
    def __init__(self, client) -> None:
        self.client = client
        self.base_url = client.config.get_alignment_url("v1")

    def evaluate(
        self,
        *,
        response: str,
        **kwargs
    ) -> FormalityResponse:
        """
        Evaluate the formality of a response.

        Args:
            response: The response string (required)

        Returns:
            FormalityResponse containing the evaluation results
        """
        req = FormalityRequest(response=response)
        result = self.client._post(
            endpoint=f"{self.base_url}/formality",
            data=req.model_dump() if hasattr(req, "model_dump") else req.dict()
        )
        return FormalityResponse(**result)

    def batch_evaluate(
        self,
        inputs: List[FormalityRequest]
    ) -> List[FormalityResponse]:
        """Evaluate multiple inputs for formality."""
        raise NotImplementedError("Batch evaluation not yet supported")

    def explain(
        self,
        request: FormalityRequest
    ) -> Dict[str, Any]:
        """Get detailed explanation of the formality evaluation."""
        raise NotImplementedError("Explanation not yet supported") 