from typing import Any, Dict, List

from trustwise.sdk.types import ClarityRequest, ClarityResponse


class ClarityMetric:
    """Clarity metric for evaluating response clarity."""
    def __init__(self, client) -> None:
        self.client = client
        self.base_url = client.config.get_alignment_url("v1")

    def evaluate(
        self,
        *,
        query: str,
        response: str,
        **kwargs
    ) -> ClarityResponse:
        """
        Evaluate the clarity of a response to the query.

        Args:
            query: The query string (required)
            response: The response string (required)

        Returns:
            ClarityResponse containing the evaluation results
        """
        req = ClarityRequest(query=query, response=response)
        result = self.client._post(
            endpoint=f"{self.base_url}/clarity",
            data=req.model_dump() if hasattr(req, "model_dump") else req.dict()
        )
        return ClarityResponse(**result)

    def batch_evaluate(
        self,
        inputs: List[ClarityRequest]
    ) -> List[ClarityResponse]:
        """Evaluate multiple inputs for clarity."""
        raise NotImplementedError("Batch evaluation not yet supported")

    def explain(
        self,
        request: ClarityRequest
    ) -> Dict[str, Any]:
        """Get detailed explanation of the clarity evaluation."""
        raise NotImplementedError("Explanation not yet supported") 