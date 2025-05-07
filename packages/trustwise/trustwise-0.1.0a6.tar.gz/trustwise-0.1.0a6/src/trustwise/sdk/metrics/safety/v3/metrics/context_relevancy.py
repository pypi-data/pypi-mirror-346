from typing import List

from trustwise.sdk.types import (
    Context,
    ContextRelevancyRequest,
    ContextRelevancyResponse,
)


class ContextRelevancyMetric:
    """Context relevancy metric for evaluating context relevance to query."""
    
    def __init__(self, client) -> None:
        self.client = client
        self.base_url = client.config.get_safety_url("v3")
    
    def evaluate(
        self,
        *,
        query: str,
        context: Context,
        response: str,
        **kwargs
    ) -> ContextRelevancyResponse:
        """
        Evaluate the relevancy of context to the query.

        Args:
            query: The query string (required)
            context: The context information (required)
            response: The response string (required)

        Returns:
            ContextRelevancyResponse containing the evaluation results
        """
        req = ContextRelevancyRequest(query=query, context=context, response=response, **kwargs)
        result = self.client._post(
            endpoint=f"{self.base_url}/context_relevancy",
            data=req.to_dict()
        )
        return ContextRelevancyResponse(**result)
    
    def batch_evaluate(
        self,
        inputs: List[ContextRelevancyRequest]
    ) -> List[ContextRelevancyResponse]:
        """Evaluate multiple inputs in a single request."""
        raise NotImplementedError("Batch evaluation not yet supported")
    
    def explain(
        self,
        *,
        query: str,
        context: Context,
        response: str,
        **kwargs
    ) -> dict:
        """Get detailed explanation of the evaluation."""
        # req = ContextRelevancyRequest(query=query, context=context, response=response)
        raise NotImplementedError("Explanation not yet supported") 