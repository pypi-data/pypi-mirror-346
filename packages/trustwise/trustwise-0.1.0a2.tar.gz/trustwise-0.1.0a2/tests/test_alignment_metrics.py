from typing import Any
from unittest.mock import patch

import pytest

from trustwise.sdk import TrustwiseSDK
from trustwise.sdk.types import (
    ClarityResponse,
    FormalityResponse,
    HelpfulnessResponse,
    SensitivityResponse,
    SimplicityResponse,
    ToneResponse,
    ToxicityResponse,
)

from .helpers import get_mock_response


class TestAlignmentMetricsV1:
    """Test suite for Alignment Metrics API v1."""

    @patch("trustwise.sdk.client.TrustwiseClient._post")
    def test_clarity(
        self,
        mock_post: Any,
        sdk: TrustwiseSDK,
        sample_query: str,
        sample_response: str
    ) -> None:
        """Test clarity evaluation."""
        mock_post.return_value = get_mock_response("alignment/v1/clarity")
        result = sdk.alignment.v1.clarity.evaluate(
            query=sample_query,
            response=sample_response
        )
        
        assert isinstance(result, ClarityResponse)
        assert isinstance(result.score, float)
        assert 0 <= result.score <= 100  # Scores are percentages
        # Test JSON output
        json_str = result.to_json()
        import json as _json
        data = _json.loads(json_str)
        assert data["score"] == result.score

    @patch("trustwise.sdk.client.TrustwiseClient._post")
    def test_helpfulness(
        self,
        mock_post: Any,
        sdk: TrustwiseSDK,
        sample_query: str,
        sample_response: str
    ) -> None:
        """Test helpfulness evaluation."""
        mock_post.return_value = get_mock_response("alignment/v1/helpfulness")
        result = sdk.alignment.v1.helpfulness.evaluate(
            query=sample_query,
            response=sample_response
        )
        assert isinstance(result, HelpfulnessResponse)
        assert isinstance(result.score, float)
        assert 0 <= result.score <= 100  # Scores are percentages
        # Test JSON output
        json_str = result.to_json()
        import json as _json
        data = _json.loads(json_str)
        assert data["score"] == result.score

    @patch("trustwise.sdk.client.TrustwiseClient._post")
    def test_formality(
        self,
        mock_post: Any,
        sdk: TrustwiseSDK,
        sample_response: str
    ) -> None:
        """Test formality evaluation."""
        mock_post.return_value = get_mock_response("alignment/v1/formality")
        result = sdk.alignment.v1.formality.evaluate(
            response=sample_response
        )
        assert isinstance(result, FormalityResponse)
        assert isinstance(result.score, float)
        assert isinstance(result.sentences, list)
        assert isinstance(result.scores, list)
        assert 0 <= result.score <= 100  # Scores are percentages
        # Test JSON output
        json_str = result.to_json()
        import json as _json
        data = _json.loads(json_str)
        assert data["score"] == result.score
        assert data["sentences"] == result.sentences
        assert data["scores"] == result.scores

    @patch("trustwise.sdk.client.TrustwiseClient._post")
    def test_simplicity(
        self,
        mock_post: Any,
        sdk: TrustwiseSDK,
        sample_response: str
    ) -> None:
        """Test simplicity evaluation."""
        mock_post.return_value = get_mock_response("alignment/v1/simplicity")
        result = sdk.alignment.v1.simplicity.evaluate(
            response=sample_response
        )
        assert isinstance(result, SimplicityResponse)
        assert isinstance(result.score, float)
        assert 0 <= result.score <= 100  # Scores are percentages
        # Test JSON output
        json_str = result.to_json()
        import json as _json
        data = _json.loads(json_str)
        assert data["score"] == result.score

    @patch("trustwise.sdk.client.TrustwiseClient._post")
    def test_sensitivity(
        self,
        mock_post: Any,
        sdk: TrustwiseSDK,
        sample_query: str,
        sample_response: str
    ) -> None:
        """Test sensitivity evaluation."""
        mock_post.return_value = get_mock_response("alignment/v1/sensitivity")
        result = sdk.alignment.v1.sensitivity.evaluate(
            response=sample_response,
            topics=["health", "finance"],
            query=sample_query
        )
        assert isinstance(result, SensitivityResponse)
        assert isinstance(result.scores, dict)
        for topic, score in result.scores.items():
            assert isinstance(score, float)
            assert 0 <= score <= 100  # Scores are percentages
        # Test JSON output
        json_str = result.to_json()
        import json as _json
        data = _json.loads(json_str)
        assert data["scores"] == result.scores

    @patch("trustwise.sdk.client.TrustwiseClient._post")
    def test_toxicity(
        self,
        mock_post: Any,
        sdk: TrustwiseSDK,
        sample_query: str,
        sample_response: str
    ) -> None:
        """Test toxicity evaluation."""
        mock_post.return_value = get_mock_response("alignment/v1/toxicity")
        result = sdk.alignment.v1.toxicity.evaluate(
            query=sample_query,
            response=sample_response
        )
        assert isinstance(result, ToxicityResponse)
        assert isinstance(result.labels, list)
        assert isinstance(result.scores, list)
        assert len(result.labels) == len(result.scores)
        for score in result.scores:
            assert isinstance(score, float)
            assert 0 <= score <= 1  # Toxicity scores are between 0 and 1
        # Test JSON output
        json_str = result.to_json()
        import json as _json
        data = _json.loads(json_str)
        assert data["labels"] == result.labels
        assert data["scores"] == result.scores

    @patch("trustwise.sdk.client.TrustwiseClient._post")
    def test_tone(
        self,
        mock_post: Any,
        sdk: TrustwiseSDK,
        sample_response: str
    ) -> None:
        """Test tone evaluation."""
        mock_post.return_value = get_mock_response("alignment/v1/tone")
        result = sdk.alignment.v1.tone.evaluate(
            response=sample_response
        )
        assert isinstance(result, ToneResponse)
        assert isinstance(result.labels, list)
        assert isinstance(result.scores, list)
        assert len(result.labels) == len(result.scores)
        for score in result.scores:
            assert isinstance(score, float)
            assert 0 <= score <= 100  # Scores are percentages
        # Test JSON output
        json_str = result.to_json()
        import json as _json
        data = _json.loads(json_str)
        assert data["labels"] == result.labels
        assert data["scores"] == result.scores

    @patch("trustwise.sdk.client.TrustwiseClient._post")
    def test_invalid_input(
        self,
        mock_post: Any,
        sdk: TrustwiseSDK
    ) -> None:
        """Test handling of invalid input."""
        mock_post.side_effect = ValueError("Invalid input")
        with pytest.raises(ValueError):
            sdk.alignment.v1.clarity.evaluate(
                query="",
                response=""
            )

    @patch("trustwise.sdk.client.TrustwiseClient._post")
    def test_missing_parameters(
        self,
        mock_post: Any,
        sdk: TrustwiseSDK
    ) -> None:
        """Test handling of missing parameters."""
        mock_post.side_effect = ValueError("Missing parameters")
        with pytest.raises(ValueError):
            sdk.alignment.v1.clarity.evaluate(
                query="test",
                response=None
            )

    @patch("trustwise.sdk.client.TrustwiseClient._post")
    def test_clarity_missing_required_fields(self, mock_post: Any, sdk: TrustwiseSDK):
        """Test clarity evaluation with missing required fields."""
        with pytest.raises(TypeError):
            sdk.alignment.v1.clarity.evaluate(response="foo")
        with pytest.raises(TypeError):
            sdk.alignment.v1.clarity.evaluate(query="foo")
        with pytest.raises(TypeError):
            sdk.alignment.v1.clarity.evaluate()

    @patch("trustwise.sdk.client.TrustwiseClient._post")
    def test_helpfulness_missing_required_fields(self, mock_post: Any, sdk: TrustwiseSDK):
        """Test helpfulness evaluation with missing required fields."""
        with pytest.raises(TypeError):
            sdk.alignment.v1.helpfulness.evaluate(response="foo")
        with pytest.raises(TypeError):
            sdk.alignment.v1.helpfulness.evaluate(query="foo")
        with pytest.raises(TypeError):
            sdk.alignment.v1.helpfulness.evaluate()

    @patch("trustwise.sdk.client.TrustwiseClient._post")
    def test_formality_missing_required_fields(self, mock_post: Any, sdk: TrustwiseSDK):
        """Test formality evaluation with missing required fields."""
        with pytest.raises(TypeError):
            sdk.alignment.v1.formality.evaluate()

    @patch("trustwise.sdk.client.TrustwiseClient._post")
    def test_simplicity_missing_required_fields(self, mock_post: Any, sdk: TrustwiseSDK):
        """Test simplicity evaluation with missing required fields."""
        with pytest.raises(TypeError):
            sdk.alignment.v1.simplicity.evaluate()

    @patch("trustwise.sdk.client.TrustwiseClient._post")
    def test_sensitivity_missing_required_fields(self, mock_post: Any, sdk: TrustwiseSDK):
        """Test sensitivity evaluation with missing required fields."""
        with pytest.raises(TypeError):
            sdk.alignment.v1.sensitivity.evaluate(topics=["foo"])
        with pytest.raises(TypeError):
            sdk.alignment.v1.sensitivity.evaluate(response="foo")
        with pytest.raises(TypeError):
            sdk.alignment.v1.sensitivity.evaluate()

    @patch("trustwise.sdk.client.TrustwiseClient._post")
    def test_toxicity_missing_required_fields(self, mock_post: Any, sdk: TrustwiseSDK):
        """Test toxicity evaluation with missing required fields."""
        with pytest.raises(TypeError):
            sdk.alignment.v1.toxicity.evaluate(response="foo")
        with pytest.raises(TypeError):
            sdk.alignment.v1.toxicity.evaluate(query="foo")
        with pytest.raises(TypeError):
            sdk.alignment.v1.toxicity.evaluate()

    @patch("trustwise.sdk.client.TrustwiseClient._post")
    def test_tone_missing_required_fields(self, mock_post: Any, sdk: TrustwiseSDK):
        """Test tone evaluation with missing required fields."""
        with pytest.raises(TypeError):
            sdk.alignment.v1.tone.evaluate() 