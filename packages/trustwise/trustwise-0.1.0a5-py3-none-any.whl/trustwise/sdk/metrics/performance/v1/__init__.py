from trustwise.sdk.metrics.base import BasePerformanceMetric
from trustwise.sdk.metrics.performance.v1.metrics.carbon import CarbonMetric
from trustwise.sdk.metrics.performance.v1.metrics.cost import CostMetric


class PerformanceMetricsV1(BasePerformanceMetric):
    """Performance metrics for version 1 of the API."""
    
    def __init__(self, client) -> None:
        """Initialize the performance metrics."""
        base_url = client.config.get_performance_url("v1")
        super().__init__(client, base_url=base_url, version="v1")
        self.cost = CostMetric(client)
        self.carbon = CarbonMetric(client)