from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class SDKBaseModel(BaseModel):
    def to_json(self, **kwargs) -> str:
        """
        Return a JSON string representation of the model.
        Ensures valid JSON output regardless of Pydantic version.
        """
        return self.model_dump_json(**kwargs)

class Fact(SDKBaseModel):
    """
    A fact extracted from a response with its verification status.
    :param statement: The fact statement text.
    :param label: The label for the fact.
    :param prob: The probability/confidence for the fact.
    :param sentence_span: The character span of the statement in the response.
    """
    statement: str
    label: str
    prob: float
    sentence_span: List[int]

Facts = List[Fact]

class FaithfulnessResponse(SDKBaseModel):
    """
    Response type for faithfulness evaluation.
    :param score: The faithfulness score.
    :param facts: List of facts extracted from the response.
    """
    score: float
    facts: Facts

class AnswerRelevancyResponse(SDKBaseModel):
    """
    Response type for answer relevancy evaluation.

    :param score: The answer relevancy score.
    :param generated_question: The generated question for evaluation.
    """
    score: float
    generated_question: str

class ContextNode(SDKBaseModel):
    """
    A single context node with its metadata.

    :param node_id: The unique identifier for the context node.
    :param node_score: The score associated with the node.
    :param node_text: The text content of the node.
    """
    node_id: str
    node_score: float
    node_text: str

# Define Context as a list of ContextNode (Pydantic model)
Context = List[ContextNode]
"""A list of ContextNode objects representing the context for evaluation."""

class ContextRelevancyRequest(SDKBaseModel):
    """
    Request type for context relevancy evaluation.
    :param query: The input query string.
    :param context: The context information (required).
    :param response: The response to evaluate.
    """
    query: str
    context: Context
    response: str

class ContextRelevancyResponse(SDKBaseModel):
    """
    Response type for context relevancy evaluation.
    :param score: The context relevancy score.
    :param topics: List of topics identified.
    :param scores: List of scores for each topic.
    """
    score: float
    topics: List[str]
    scores: List[float]

class SummarizationRequest(SDKBaseModel):
    """
    Request type for summarization evaluation.
    :param query: The input query string.
    :param response: The response to evaluate.
    :param context: The context information (required).
    """
    query: str
    response: str
    context: Context

class SummarizationResponse(SDKBaseModel):
    """
    Response type for summarization quality evaluation.
    :param score: The summarization score.
    """
    score: float

class PIIEntity(SDKBaseModel):
    """
    A detected piece of personally identifiable information.
    :param interval: The [start, end] indices of the PII in the text.
    :param string: The detected PII string.
    :param category: The PII category.
    """
    interval: List[int]
    string: str
    category: str

class PIIRequest(SDKBaseModel):
    """
    Request type for PII detection.
    :param text: The text to evaluate.
    :param allowlist: List of allowed PII categories.
    :param blocklist: List of blocked PII categories.
    """
    text: str
    allowlist: List[str]
    blocklist: List[str]

class PIIResponse(SDKBaseModel):
    """
    Response type for PII detection.
    :param identified_pii: List of detected PII entities.
    """
    identified_pii: List[PIIEntity]

class PromptInjectionRequest(SDKBaseModel):
    """
    Request type for prompt injection detection.
    :param query: The input query string.
    :param response: The response to evaluate.
    :param context: The context information (required).
    """
    query: str
    response: str
    context: Context = Field(..., min_items=1, description="A non-empty list of ContextNode objects.")

class PromptInjectionResponse(SDKBaseModel):
    """
    Response type for prompt injection detection.
    :param score: The prompt injection score.
    """
    score: float

class ClarityRequest(SDKBaseModel):
    """
    Request type for clarity evaluation.
    :param query: The input query string.
    :param response: The response to evaluate.
    """
    query: str
    response: str

class ClarityResponse(SDKBaseModel):
    """
    Response type for clarity evaluation.
    :param score: The overall clarity score.
    """
    score: float

class HelpfulnessRequest(SDKBaseModel):
    """
    Request type for helpfulness evaluation.
    :param query: The input query string.
    :param response: The response to evaluate.
    """
    query: str
    response: str

class HelpfulnessResponse(SDKBaseModel):
    """
    Response type for helpfulness evaluation.
    :param score: The overall helpfulness score.
    """
    score: float

class FormalityRequest(SDKBaseModel):
    """
    Request type for formality evaluation.
    :param response: The response to evaluate.
    """
    response: str

class FormalityResponse(SDKBaseModel):
    """
    Response type for formality evaluation.
    :param score: The overall formality score.
    :param sentences: List of sentences analyzed.
    :param scores: List of scores for each sentence.
    """
    score: float
    sentences: List[str]
    scores: List[float]

class SimplicityResponse(SDKBaseModel):
    """
    Response type for simplicity evaluation.
    :param score: The overall simplicity score (percentage).
    """
    score: float

class SensitivityResponse(SDKBaseModel):
    """
    Response type for sensitivity evaluation.
    :param scores: Mapping of topic to sensitivity score.
    """
    scores: Dict[str, float]

class ToxicityResponse(SDKBaseModel):
    """
    Response type for toxicity evaluation.
    :param labels: List of toxicity category labels.
    :param scores: List of scores for each label.
    """
    labels: List[str]
    scores: List[float]

class ToneResponse(SDKBaseModel):
    """
    Response type for tone evaluation.
    :param labels: List of detected tone labels.
    :param scores: List of scores for each label.
    """
    labels: List[str]
    scores: List[float]

class CostResponse(SDKBaseModel):
    """
    Response type for cost evaluation.
    :param cost_estimate_per_run: Estimated cost per run.
    :param total_project_cost_estimate: Total estimated cost for the project.
    """
    cost_estimate_per_run: float
    total_project_cost_estimate: float

class CarbonResponse(SDKBaseModel):
    """
    Response type for carbon emissions evaluation.
    :param carbon_emitted: Estimated carbon emitted (kg CO2e).
    :param sci_per_api_call: SCI per API call.
    :param sci_per_10k_calls: SCI per 10,000 calls.
    """
    carbon_emitted: float
    sci_per_api_call: float
    sci_per_10k_calls: float

class FaithfulnessRequest(SDKBaseModel):
    """
    Request type for faithfulness evaluation.
    :param query: The input query string.
    :param response: The response to evaluate.
    :param context: The context information (required).
    """
    query: str
    response: str
    context: Context

class AnswerRelevancyRequest(SDKBaseModel):
    """
    Request type for answer relevancy evaluation.
    :param query: The input query string.
    :param response: The response to evaluate.
    :param context: The context information (required).
    """
    query: str
    response: str
    context: Context

class SimplicityRequest(SDKBaseModel):
    """
    Request type for simplicity evaluation.
    :param response: The response to evaluate.
    """
    response: str

class SensitivityRequest(SDKBaseModel):
    """
    Request type for sensitivity evaluation.
    :param response: The response to evaluate.
    :param topics: List of topics to check for sensitivity.
    :param query: The input query string (optional).
    """
    response: str
    topics: List[str]
    query: Optional[str] = None

class ToxicityRequest(SDKBaseModel):
    """
    Request type for toxicity evaluation.
    :param query: The input query string.
    :param response: The response to evaluate.
    """
    query: str
    response: str

class ToneRequest(SDKBaseModel):
    """
    Request type for tone evaluation.
    :param response: The response to evaluate.
    """
    response: str

class CostRequest(SDKBaseModel):
    """
    Request type for cost evaluation.
    :param model_name: Name of the model.
    :param model_type: Type of the model.
    :param model_provider: Provider of the model.
    :param number_of_queries: Number of queries to estimate cost for.
    :param total_prompt_tokens: Total prompt tokens (optional).
    :param total_completion_tokens: Total completion tokens (optional).
    :param total_tokens: Total tokens (optional).
    :param instance_type: Instance type (optional).
    :param average_latency: Average latency (optional).
    """
    model_name: str
    model_type: str
    model_provider: str
    number_of_queries: int
    total_prompt_tokens: Optional[int] = None
    total_completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    instance_type: Optional[str] = None
    average_latency: Optional[float] = None

class CarbonRequest(SDKBaseModel):
    """
    Request type for carbon evaluation.
    :param processor_name: Name of the processor.
    :param provider_name: Name of the provider.
    :param provider_region: Region of the provider.
    :param instance_type: Instance type.
    :param average_latency: Average latency (ms).
    """
    processor_name: str
    provider_name: str
    provider_region: str
    instance_type: str
    average_latency: int

class GuardrailResponse(SDKBaseModel):
    """
    Response type for guardrail evaluation.
    :param passed: Whether all metrics passed.
    :param blocked: Whether the response is blocked due to failure.
    :param results: Dictionary of metric results, each containing 'passed' and 'result'.
    """
    passed: bool
    blocked: bool
    results: dict

    def to_json(self, **kwargs) -> str:
        """
        Return a JSON string representation of the guardrail evaluation, recursively serializing all nested SDK types.
        Use this for logging, API responses, or storage.
        """
        def serialize(obj):
            if hasattr(obj, "to_json"):
                return obj.model_dump()
            elif isinstance(obj, dict):
                return {k: serialize(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [serialize(i) for i in obj]
            return obj
        data = {
            "passed": self.passed,
            "blocked": self.blocked,
            "results": serialize(self.results)
        }
        import json
        return json.dumps(data, **kwargs)

    def to_dict(self) -> dict:
        """
        Return a Python dict representation of the guardrail evaluation, recursively serializing all nested SDK types.
        Use this for programmatic access, further processing, or conversion to JSON via json.dumps().
        """
        def serialize(obj):
            if hasattr(obj, "to_json"):
                return obj.model_dump()
            elif isinstance(obj, dict):
                return {k: serialize(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [serialize(i) for i in obj]
            return obj
        return {
            "passed": self.passed,
            "blocked": self.blocked,
            "results": serialize(self.results)
        } 
