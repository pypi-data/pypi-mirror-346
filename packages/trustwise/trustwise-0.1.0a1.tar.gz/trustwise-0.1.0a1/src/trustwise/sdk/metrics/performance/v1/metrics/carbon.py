from typing import Any, Dict, List, Optional

from trustwise.sdk.types import CarbonRequest, CarbonResponse


class CarbonMetric:
    """Carbon emissions metrics evaluator."""
    def __init__(self, client) -> None:
        self.client = client
        self.base_url = client.config.get_performance_url("v1")

    def evaluate(
        self,
        request: object = None,
        *,
        processor_name: Optional[str] = None,
        provider_name: Optional[str] = None,
        provider_region: Optional[str] = None,
        instance_type: Optional[str] = None,
        average_latency: Optional[int] = None,
        **kwargs
    ) -> CarbonResponse:
        """
        Evaluate carbon metrics.
        Accepts either a CarbonRequest object or keyword arguments.
        """
        if isinstance(request, CarbonRequest):
            req = request
        elif all([processor_name, provider_name, provider_region, instance_type, average_latency is not None]):
            req = CarbonRequest(
                processor_name=processor_name,
                provider_name=provider_name,
                provider_region=provider_region,
                instance_type=instance_type,
                average_latency=average_latency
            )
        else:
            raise ValueError("Must provide either a CarbonRequest or all required keyword arguments.")

        result = self.client._post(
            endpoint=f"{self.base_url}/carbon",
            data=req.model_dump() if hasattr(req, "model_dump") else req.dict()
        )
        return CarbonResponse(**result)

    def batch_evaluate(
        self,
        inputs: List[CarbonRequest]
    ) -> List[CarbonResponse]:
        """Evaluate multiple inputs for carbon."""
        raise NotImplementedError("Batch evaluation not yet supported")

    def explain(
        self,
        request: CarbonRequest
    ) -> Dict[str, Any]:
        """Get detailed explanation of the carbon evaluation."""
        raise NotImplementedError("Explanation not yet supported") 