import warnings
from typing import Any, Callable, Dict, List, Optional, Union

import requests

from trustwise.sdk.features import is_beta_feature
from trustwise.sdk.protocols import TrustwiseClientProtocol


class Guardrail:
    """
    Guardrail system for Trustwise API responses.
    
    .. warning::
        This feature is currently in beta. The API and functionality may change in future releases.
    """

    def __init__(
        self,
        trustwise_client: TrustwiseClientProtocol,
        thresholds: Dict[str, float],
        *, # This is a marker to indicate that the following arguments are keyword-only
        block_on_failure: bool = False,
        callbacks: Optional[Dict[str, Callable]] = None
    ) -> None:
        """
        Initialize the guardrail system.

        Args:
            trustwise_client: The Trustwise client instance.
            thresholds: Dictionary of metric names and their threshold values (0-100).
            block_on_failure: Whether to block responses that fail any metric.
            callbacks: Optional callbacks for metric evaluation results.

        Raises:
            ValueError: If thresholds are invalid.
        """
        if is_beta_feature("guardrails"):
            warnings.warn(
                "The guardrails feature is currently in beta. The API and functionality may change in future releases.",
                UserWarning,
                stacklevel=2
            )
            
        # Validate thresholds
        if not thresholds:
            raise ValueError("Thresholds dictionary cannot be empty")
        
        for metric, threshold in thresholds.items():
            if not isinstance(threshold, (int, float)) or isinstance(threshold, bool):
                raise ValueError(f"Threshold for {metric} must be a number")
            if not 0 <= threshold <= 100:
                raise ValueError(f"Threshold for {metric} must be between 0 and 100")

        self.client = trustwise_client
        self.thresholds = thresholds
        self.block_on_failure = block_on_failure
        self.callbacks = callbacks or {}
        self.evaluation_results = {}

    def evaluate_response(
        self,
        query: str,
        response: str,
        context: Optional[Union[List[Dict[str, Any]], Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Evaluate a response against configured metrics."""
        if not query or not response:
            raise ValueError("Query and response are required parameters")
        
        if context is not None and not isinstance(context, (list, dict)):
            raise ValueError("Context must be a list or dictionary")
            
        results = {}
        passed = True
        blocked = False
        
        for metric, threshold in self.thresholds.items():
            try:
                if metric == "faithfulness":
                    result = self.client.safety.v3.faithfulness.evaluate(
                        query=query,
                        response=response,
                        context=context
                    )
                    score = result.score
                elif metric == "answer_relevancy":
                    result = self.client.safety.v3.answer_relevancy.evaluate(
                        query=query,
                        response=response,
                        context=context
                    )
                    score = result.score
                elif metric == "context_relevancy":
                    result = self.client.safety.v3.context_relevancy.evaluate(
                        query=query,
                        response=response,
                        context=context
                    )
                    score = result.score
                elif metric in ["clarity", "helpfulness", "formality", "simplicity"]:
                    # Alignment metrics
                    result = self.client.alignment.v1.__getattribute__(metric).evaluate(
                        query=query,
                        response=response
                    )
                    score = result.score
                elif metric == "toxicity":
                    # Toxicity metric
                    result = self.client.alignment.v1.toxicity.evaluate(
                        query=query,
                        response=response
                    )
                    score = max(result.scores)  # Use maximum toxicity score
                elif metric == "prompt_injection":
                    # Prompt injection metric
                    result = self.client.safety.v3.prompt_injection.evaluate(
                        query=query,
                        response=response,
                        context=context
                    )
                    score = result.score
                else:
                    raise ValueError(f"Unknown metric: {metric}")
                
                results[metric] = {
                    "passed": score >= threshold,
                    "result": result
                }
                
                if metric in self.callbacks:
                    self.callbacks[metric](metric, result)

                if not results[metric]["passed"]:
                    passed = False
                    if self.block_on_failure:
                        blocked = True
                        break
                        
            except (ValueError, AttributeError, KeyError, requests.exceptions.RequestException) as e:
                results[metric] = {
                    "passed": False,
                    "result": {"score": 0.0},
                    "error": str(e)
                }
                passed = False
                if self.block_on_failure:
                    blocked = True
                    break
        
        return {
            "passed": passed,
            "blocked": blocked,
            "results": results
        }

    def check_pii(
        self,
        text: str,
        allowlist: Optional[List[str]] = None,
        blocklist: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Check text for PII and determine if it should be blocked.
        
        Args:
            text: Text to check for PII
            allowlist: Optional list of allowed terms
            blocklist: Optional list of blocked terms
            
        Returns:
            Dictionary with PII detection results and pass/fail status
        """
        try:
            result = self.client.safety.v3.pii.evaluate(
                text=text,
                allowlist=allowlist,
                blocklist=blocklist
            )
            
            # Consider it passed if no PII is found or only allowlisted items are found
            has_pii = len(result.get("identified_pii", [])) > 0
            
            return {
                "passed": not has_pii,
                "result": result,
                "blocked": self.block_on_failure and has_pii
            }
        except (ValueError, AttributeError, KeyError, requests.exceptions.RequestException) as e:
            print(f"Error checking PII: {e!s}")
            return {
                "passed": not self.block_on_failure,
                "error": str(e),
                "blocked": self.block_on_failure
            } 