from typing import List

from trustwise.sdk.types import (
    AnswerRelevancyRequest,
    AnswerRelevancyResponse,
    Context,
)


class AnswerRelevancyMetric:
    """Answer relevancy metric for evaluating response relevance to query."""
    
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
    ) -> AnswerRelevancyResponse:
        """
        Evaluate the relevancy of a response to the query.

        Args:
            query: The query string (required)
            response: The response string (required)
            context: The context information (required)

        Returns:
            AnswerRelevancyResponse containing the evaluation results
        """
        req = AnswerRelevancyRequest(query=query, response=response, context=context)
        result = self.client._post(
            endpoint=f"{self.base_url}/answer_relevancy",
            data=req.model_dump() if hasattr(req, "model_dump") else req.dict()
        )
        return AnswerRelevancyResponse(**result)
    
    def batch_evaluate(
        self,
        inputs: List[AnswerRelevancyRequest]
    ) -> List[AnswerRelevancyResponse]:
        """Evaluate multiple inputs in a single request."""
        raise NotImplementedError("Batch evaluation not yet supported")
    
    def explain(
        self,
        *,
        query: str,
        response: str,
        context: Context,
        **kwargs
    ) -> dict:
        """Get detailed explanation of the evaluation."""
        # req = AnswerRelevancyRequest(query=query, response=response, context=context)
        raise NotImplementedError("Explanation not yet supported") 