from typing import List, Optional

from trustwise.sdk.types import PIIRequest, PIIResponse


class PIIMetric:
    """PII detection metric for identifying personally identifiable information."""
    
    def __init__(self, client) -> None:
        self.client = client
        self.base_url = client.config.get_safety_url("v3")
    
    def evaluate(
        self,
        *,
        text: str,
        allowlist: List[str],
        blocklist: List[str],
        **kwargs
    ) -> PIIResponse:
        """
        Evaluate the PII detection in a response.

        Args:
            text: The text to evaluate (required)
            allowlist: List of allowed PII categories (required)
            blocklist: List of blocked PII categories (required)

        Returns:
            PIIResponse containing the evaluation results
        """
        req = PIIRequest(text=text, allowlist=allowlist, blocklist=blocklist)
        result = self.client._post(
            endpoint=f"{self.base_url}/pii",
            data=req.model_dump() if hasattr(req, "model_dump") else req.dict()
        )
        return PIIResponse(**result)
    
    def batch_evaluate(
        self,
        texts: List[str],
        allowlist: Optional[List[str]] = None,
        blocklist: Optional[List[str]] = None
    ) -> List[PIIResponse]:
        """Evaluate multiple texts for PII content."""
        raise NotImplementedError("Batch evaluation not yet supported")
    
    def explain(
        self,
        *,
        text: str,
        allowlist: List[str],
        blocklist: List[str],
        **kwargs
    ) -> dict:
        """Get detailed explanation of the PII detection."""
        # req = PIIRequest(text=text, allowlist=allowlist, blocklist=blocklist)
        raise NotImplementedError("Explanation not yet supported") 