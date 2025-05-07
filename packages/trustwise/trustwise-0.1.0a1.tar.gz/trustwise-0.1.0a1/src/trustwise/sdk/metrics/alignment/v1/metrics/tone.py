from typing import Any, Dict, List

from trustwise.sdk.types import ToneRequest, ToneResponse


class ToneMetric:
    """Tone metric for evaluating response tone."""
    def __init__(self, client) -> None:
        self.client = client
        self.base_url = client.config.get_alignment_url("v1")

    def evaluate(
        self,
        *,
        response: str,
        **kwargs
    ) -> ToneResponse:
        """
        Evaluate the tone of a response.

        Args:
            response: The response string (required)

        Returns:
            ToneResponse containing the evaluation results
        """
        req = ToneRequest(response=response)
        result = self.client._post(
            endpoint=f"{self.base_url}/tone",
            data=req.model_dump() if hasattr(req, "model_dump") else req.dict()
        )
        return ToneResponse(**result)

    def batch_evaluate(
        self,
        inputs: List[ToneRequest]
    ) -> List[ToneResponse]:
        """Evaluate multiple inputs for tone."""
        raise NotImplementedError("Batch evaluation not yet supported")

    def explain(
        self,
        request: ToneRequest
    ) -> Dict[str, Any]:
        """Get detailed explanation of the tone evaluation."""
        raise NotImplementedError("Explanation not yet supported") 