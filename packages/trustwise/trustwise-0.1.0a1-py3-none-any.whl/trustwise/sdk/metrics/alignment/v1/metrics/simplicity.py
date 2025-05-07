from typing import Any, Dict, List

from trustwise.sdk.types import SimplicityRequest, SimplicityResponse


class SimplicityMetric:
    """Simplicity metric for evaluating response simplicity."""
    def __init__(self, client) -> None:
        self.client = client
        self.base_url = client.config.get_alignment_url("v1")

    def evaluate(
        self,
        *,
        response: str,
        **kwargs
    ) -> SimplicityResponse:
        """
        Evaluate the simplicity of a response.

        Args:
            response: The response string (required)

        Returns:
            SimplicityResponse containing the evaluation results
        """
        req = SimplicityRequest(response=response)
        result = self.client._post(
            endpoint=f"{self.base_url}/simplicity",
            data=req.model_dump() if hasattr(req, "model_dump") else req.dict()
        )
        return SimplicityResponse(**result)

    def batch_evaluate(
        self,
        inputs: List[SimplicityRequest]
    ) -> List[SimplicityResponse]:
        """Evaluate multiple inputs for simplicity."""
        raise NotImplementedError("Batch evaluation not yet supported")

    def explain(
        self,
        request: SimplicityRequest
    ) -> Dict[str, Any]:
        """Get detailed explanation of the simplicity evaluation."""
        raise NotImplementedError("Explanation not yet supported") 