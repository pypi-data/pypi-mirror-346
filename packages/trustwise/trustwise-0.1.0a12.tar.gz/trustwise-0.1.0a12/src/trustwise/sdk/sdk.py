from typing import Callable, Dict, List, Optional, Set

from trustwise.sdk.client import TrustwiseClient
from trustwise.sdk.config import TrustwiseConfig
from trustwise.sdk.features import get_beta_features, is_beta_feature
from trustwise.sdk.guardrails.guardrail import Guardrail
from trustwise.sdk.metrics.alignment import AlignmentMetrics
from trustwise.sdk.metrics.performance import PerformanceMetrics
from trustwise.sdk.metrics.safety import SafetyMetrics


class TrustwiseSDK:
    """
    Main SDK class for Trustwise API access.

    Provides access to safety, alignment, and performance metrics through version-specific paths.
    """

    def __init__(self, config: TrustwiseConfig) -> None:
        """
        Initialize the Trustwise SDK with path-based versioning support.

        Args:
            config: Trustwise configuration instance.
        """
        self.client = TrustwiseClient(config)
        self.safety = SafetyMetrics(self.client)
        self.alignment = AlignmentMetrics(self.client)
        self.performance = PerformanceMetrics(self.client)

    def get_versions(self) -> Dict[str, List[str]]:
        """
        Get the available API versions for each metric type.

        Returns:
            Dictionary mapping metric types to their available versions.
            Example: {"safety": ["v3"], "alignment": ["v1"], "performance": ["v1"]}
        """
        return {
            "safety": ["v3"],  # Currently only v3 is supported
            "alignment": ["v1"],  # Currently only v1 is supported
            "performance": ["v1"],  # Currently only v1 is supported
        }

    def get_beta_features(self) -> Set[str]:
        """
        Get the set of features currently in beta.

        Returns:
            Set[str]: Set of feature names that are in beta
        """
        return get_beta_features()

    def is_beta_feature(self, feature_name: str) -> bool:
        """
        Check if a feature is currently in beta.

        Args:
            feature_name: Name of the feature to check

        Returns:
            bool: True if the feature is in beta, False otherwise
        """
        return is_beta_feature(feature_name)

    def guardrails(
        self,
        thresholds: Dict[str, float],
        *,
        block_on_failure: bool = False,
        callbacks: Optional[Dict[str, Callable]] = None
    ) -> Guardrail:
        """
        Create a guardrail system for response evaluation.

        Args:
            thresholds: Dictionary mapping metrics to threshold values.
            block_on_failure: Whether to block responses that fail checks.
            callbacks: Dictionary mapping metrics to callback functions.

        Returns:
            A configured Guardrail instance.

        Raises:
            ValueError: If any metric in thresholds is not supported by the current API version.
        """
        return Guardrail(
            trustwise_client=self,
            thresholds=thresholds,
            block_on_failure=block_on_failure,
            callbacks=callbacks
        ) 