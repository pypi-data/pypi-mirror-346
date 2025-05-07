from typing import Any
from unittest.mock import patch

import pytest

from trustwise.sdk import TrustwiseSDK
from trustwise.sdk.types import (
    CarbonRequest,
    CarbonResponse,
    CostRequest,
    CostResponse,
)

from .helpers import get_mock_response


class TestPerformanceMetricsV1:
    """Test suite for Performance Metrics API v1."""

    @patch("trustwise.sdk.client.TrustwiseClient._post")
    def test_cost_openai_llm(
        self,
        mock_post: Any,
        sdk: TrustwiseSDK
    ) -> None:
        """Test cost evaluation for OpenAI LLM."""
        mock_post.return_value = get_mock_response("performance/v1/cost")
        request = CostRequest(
            model_name="gpt-3.5-turbo",
            model_type="LLM",
            model_provider="OpenAI",
            number_of_queries=5,
            total_prompt_tokens=950,
            total_completion_tokens=50
        )
        result = sdk.performance.v1.cost.evaluate(request)
        
        assert isinstance(result, CostResponse)
        assert isinstance(result.cost_estimate_per_run, float)
        assert isinstance(result.total_project_cost_estimate, float)
        # Test JSON output
        json_str = result.to_json()
        import json as _json
        data = _json.loads(json_str)
        assert data["cost_estimate_per_run"] == result.cost_estimate_per_run
        assert data["total_project_cost_estimate"] == result.total_project_cost_estimate

    @patch("trustwise.sdk.client.TrustwiseClient._post")
    def test_cost_huggingface_llm(
        self,
        mock_post: Any,
        sdk: TrustwiseSDK
    ) -> None:
        """Test cost evaluation for Hugging Face LLM."""
        mock_post.return_value = get_mock_response("performance/v1/cost")
        request = CostRequest(
            model_name="mistral-7b",
            model_type="LLM",
            model_provider="HuggingFace",
            number_of_queries=5,
            total_prompt_tokens=950,
            total_completion_tokens=50,
            instance_type="a1.large",
            average_latency=653
        )
        result = sdk.performance.v1.cost.evaluate(request)
        
        assert isinstance(result, CostResponse)
        assert isinstance(result.cost_estimate_per_run, float)
        assert isinstance(result.total_project_cost_estimate, float)
        # Test JSON output
        json_str = result.to_json()
        import json as _json
        data = _json.loads(json_str)
        assert data["cost_estimate_per_run"] == result.cost_estimate_per_run
        assert data["total_project_cost_estimate"] == result.total_project_cost_estimate

    @patch("trustwise.sdk.client.TrustwiseClient._post")
    def test_cost_azure_reranker(
        self,
        mock_post: Any,
        sdk: TrustwiseSDK
    ) -> None:
        """Test cost evaluation for Azure Reranker."""
        mock_post.return_value = get_mock_response("performance/v1/cost")
        request = CostRequest(
            model_name="azure-reranker",
            model_type="Reranker",
            model_provider="Azure Reranker",
            number_of_queries=5
        )
        result = sdk.performance.v1.cost.evaluate(request)
        
        assert isinstance(result, CostResponse)
        assert isinstance(result.cost_estimate_per_run, float)
        assert isinstance(result.total_project_cost_estimate, float)
        # Test JSON output
        json_str = result.to_json()
        import json as _json
        data = _json.loads(json_str)
        assert data["cost_estimate_per_run"] == result.cost_estimate_per_run
        assert data["total_project_cost_estimate"] == result.total_project_cost_estimate

    @patch("trustwise.sdk.client.TrustwiseClient._post")
    def test_cost_together_reranker(
        self,
        mock_post: Any,
        sdk: TrustwiseSDK
    ) -> None:
        """Test cost evaluation for Together Reranker."""
        mock_post.return_value = get_mock_response("performance/v1/cost")
        request = CostRequest(
            model_name="together-reranker",
            model_type="Reranker",
            model_provider="Together Reranker",
            number_of_queries=5,
            total_tokens=1000
        )
        result = sdk.performance.v1.cost.evaluate(request)
        
        assert isinstance(result, CostResponse)
        assert isinstance(result.cost_estimate_per_run, float)
        assert isinstance(result.total_project_cost_estimate, float)
        # Test JSON output
        json_str = result.to_json()
        import json as _json
        data = _json.loads(json_str)
        assert data["cost_estimate_per_run"] == result.cost_estimate_per_run
        assert data["total_project_cost_estimate"] == result.total_project_cost_estimate

    def test_cost_invalid_model_type(
        self,
        sdk: TrustwiseSDK
    ) -> None:
        """Test cost evaluation with invalid model type."""
        request = CostRequest(
            model_name="gpt-3.5-turbo",
            model_type="Invalid",
            model_provider="OpenAI",
            number_of_queries=5,
            total_prompt_tokens=950,
            total_completion_tokens=50
        )
        with pytest.raises(ValueError, match="model_type must be either 'LLM' or 'Reranker'"):
            sdk.performance.v1.cost.evaluate(request)

    def test_cost_missing_required_fields_llm(
        self,
        sdk: TrustwiseSDK
    ) -> None:
        """Test cost evaluation with missing required fields for LLM."""
        request = CostRequest(
            model_name="gpt-3.5-turbo",
            model_type="LLM",
            model_provider="OpenAI",
            number_of_queries=5
        )
        with pytest.raises(ValueError, match="total_prompt_tokens and total_completion_tokens are required for LLM providers"):
            sdk.performance.v1.cost.evaluate(request)

    def test_cost_missing_required_fields_huggingface(
        self,
        sdk: TrustwiseSDK
    ) -> None:
        """Test cost evaluation with missing required fields for Hugging Face."""
        request = CostRequest(
            model_name="mistral-7b",
            model_type="LLM",
            model_provider="HuggingFace",
            number_of_queries=5,
            total_prompt_tokens=950,
            total_completion_tokens=50
        )
        with pytest.raises(ValueError, match="instance_type and average_latency are required for Hugging Face"):
            sdk.performance.v1.cost.evaluate(request)

    def test_cost_invalid_fields_openai(
        self,
        sdk: TrustwiseSDK
    ) -> None:
        """Test cost evaluation with invalid fields for OpenAI."""
        request = CostRequest(
            model_name="gpt-3.5-turbo",
            model_type="LLM",
            model_provider="OpenAI",
            number_of_queries=5,
            total_prompt_tokens=950,
            total_completion_tokens=50,
            instance_type="a1.large"
        )
        with pytest.raises(ValueError, match="instance_type is not allowed for OpenAI"):
            sdk.performance.v1.cost.evaluate(request)

    @patch("trustwise.sdk.client.TrustwiseClient._post")
    def test_carbon(
        self,
        mock_post: Any,
        sdk: TrustwiseSDK
    ) -> None:
        """Test carbon evaluation."""
        mock_post.return_value = get_mock_response("performance/v1/carbon")
        request = CarbonRequest(
            processor_name="RTX 3080",
            provider_name="aws",
            provider_region="us-east-1",
            instance_type="a1.metal",
            average_latency=653
        )
        result = sdk.performance.v1.carbon.evaluate(request)
        
        assert isinstance(result, CarbonResponse)
        assert isinstance(result.carbon_emitted, float)
        assert isinstance(result.sci_per_api_call, float)
        assert isinstance(result.sci_per_10k_calls, float)
        # Test JSON output
        json_str = result.to_json()
        import json as _json
        data = _json.loads(json_str)
        assert data["carbon_emitted"] == result.carbon_emitted
        assert data["sci_per_api_call"] == result.sci_per_api_call
        assert data["sci_per_10k_calls"] == result.sci_per_10k_calls

    def test_batch_evaluate_not_implemented(
        self,
        sdk: TrustwiseSDK
    ) -> None:
        """Test that batch evaluation is not implemented."""
        with pytest.raises(NotImplementedError):
            sdk.performance.v1.batch_evaluate([])

    def test_explain_not_implemented(
        self,
        sdk: TrustwiseSDK
    ) -> None:
        """Test that explanation is not implemented."""
        request = CostRequest(
            model_name="gpt-3.5-turbo",
            model_type="LLM",
            model_provider="OpenAI",
            number_of_queries=5,
            total_prompt_tokens=950,
            total_completion_tokens=50
        )
        with pytest.raises(NotImplementedError):
            sdk.performance.v1.explain(request) 