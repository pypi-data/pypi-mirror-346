from typing import List, Optional

from trustwise.sdk.types import CarbonRequest, CarbonResponse


class CarbonMetric:
    """Carbon emissions metrics evaluator."""
    def __init__(self, client) -> None:
        self.client = client
        self.base_url = client.config.get_performance_url("v1")

    def evaluate(
        self,
        *,
        processor_name: str,
        provider_name: str,
        provider_region: str,
        instance_type: str,
        average_latency: int,
        **kwargs
    ) -> CarbonResponse:
        """
        Evaluate carbon metrics.
        All arguments are required except those marked optional.
        """
        req = CarbonRequest(
            processor_name=processor_name,
            provider_name=provider_name,
            provider_region=provider_region,
            instance_type=instance_type,
            average_latency=average_latency,
            **kwargs
        )

        result = self.client._post(
            endpoint=f"{self.base_url}/carbon",
            data=req.to_dict()
        )
        # Only validate and return CarbonResponse for 200 responses. # TODO: Create custom TrustwiseException and raise that instead
        if isinstance(result, dict) and "detail" in result:
            # API error, raise as is
            raise Exception(f"API error: {result['detail']}")
        return CarbonResponse(**result)

    def batch_evaluate(
        self,
        inputs: List[CarbonRequest]
    ) -> List[CarbonResponse]:
        """Evaluate multiple inputs for carbon."""
        raise NotImplementedError("Batch evaluation not yet supported")

    def explain(
        self,
        *,
        processor_name: Optional[str] = None,
        provider_name: Optional[str] = None,
        provider_region: Optional[str] = None,
        instance_type: Optional[str] = None,
        average_latency: Optional[int] = None,
        **kwargs
    ) -> dict:
        """Get detailed explanation of the carbon evaluation."""
        # req = CarbonRequest(
        #     processor_name=processor_name,
        #     provider_name=provider_name,
        #     provider_region=provider_region,
        #     instance_type=instance_type,
        #     average_latency=average_latency
        # )
        raise NotImplementedError("Explanation not yet supported") 