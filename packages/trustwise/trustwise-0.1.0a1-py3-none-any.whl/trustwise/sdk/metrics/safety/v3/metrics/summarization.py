from typing import Any, Dict, List, Union

from trustwise.sdk.client import TrustwiseClient
from trustwise.sdk.types import Context, SummarizationRequest, SummarizationResponse


class SummarizationMetric:
    """Summarization metric for evaluating response summarization quality."""
    
    def __init__(self, client: TrustwiseClient) -> None:
        self.client = client
        self.base_url = client.config.get_safety_url("v3")
    
    def evaluate(
        self,
        *,
        query: str,
        response: str,
        context: Context,
        **kwargs
    ) -> SummarizationResponse:
        """
        Evaluate the quality of a summarization.

        Args:
            query: The query string (required)
            response: The response string (required)
            context: The context information (required)

        Returns:
            SummarizationResponse containing the evaluation results
        """
        req = SummarizationRequest(query=query, response=response, context=context)
        result = self.client._post(
            endpoint=f"{self.base_url}/summarization",
            data=req.model_dump() if hasattr(req, "model_dump") else req.dict()
        )
        return SummarizationResponse(**result)
    
    def batch_evaluate(
        self,
        inputs: List[Dict[str, Any]]
    ) -> List[SummarizationResponse]:
        """Evaluate multiple inputs in a single request."""
        raise NotImplementedError("Batch evaluation not yet supported")
    
    def explain(
        self,
        query: str,
        response: str,
        context: Union[List[Dict[str, str]], Dict[str, str]]
    ) -> Dict[str, Any]:
        """Get detailed explanation of the evaluation."""
        raise NotImplementedError("Explanation not yet supported") 