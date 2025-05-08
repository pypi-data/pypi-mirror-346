from typing import Any, Dict, List, Protocol


class MetricProtocol(Protocol):
    """Protocol for metric evaluation interface."""
    def evaluate(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate the metric with given parameters."""
        ...

    def batch_evaluate(self, **kwargs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Evaluate multiple inputs in a single request."""
        ...

    def explain(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed explanation of the evaluation."""
        ...


class TrustwiseClientProtocol(Protocol):
    """Protocol for Trustwise client interface."""
    safety: Any
    alignment: Any
    performance: Any
    guardrails: Any 