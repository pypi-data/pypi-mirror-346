from typing import Any, Dict, List

from trustwise.sdk.types import (
    Context,
    FaithfulnessRequest,
    FaithfulnessResponse,
)


class FaithfulnessMetric:
    """Faithfulness metric for evaluating response accuracy against context."""
    
    def __init__(self, client) -> None:
        self.client = client
        self.base_url = client.config.get_safety_url("v3")
    
    def evaluate(
        self,
        *,
        query: str,
        response: str,
        context: Context,
        **kwargs
    ) -> FaithfulnessResponse:
        """
        Evaluate the faithfulness of a response against its context.

        Args:
            query: The query string (required)
            response: The response string (required)
            context: The context information (required)

        Returns:
            FaithfulnessResponse containing the evaluation results

        Raises:
            ValueError: If not all of query, response, and context are provided
        """
        req = FaithfulnessRequest(query=query, response=response, context=context)
        result = self.client._post(
            endpoint=f"{self.base_url}/faithfulness",
            data=req.model_dump() if hasattr(req, "model_dump") else req.dict()
        )
        return FaithfulnessResponse(**result)
    
    def batch_evaluate(
        self,
        inputs: List[FaithfulnessRequest]
    ) -> List[FaithfulnessResponse]:
        """Evaluate multiple inputs in a single request."""
        raise NotImplementedError("Batch evaluation not yet supported")
    
    def explain(
        self,
        query: str,
        response: str,
        context: Context
    ) -> Dict[str, Any]:
        """Get detailed explanation of the evaluation. Context is required."""
        raise NotImplementedError("Explanation not yet supported") 