import json

from trustwise.sdk.types import (
    ClarityResponse,
    Fact,
    FaithfulnessResponse,
    PIIEntity,
    PIIResponse,
    PromptInjectionResponse,
)


def test_faithfulness_response_to_json():
    resp = FaithfulnessResponse(
        score=95.0,
        facts=[Fact(statement="Paris is the capital of France.", label="CORRECT", prob=0.99, sentence_span=[0, 30])]
    )
    # Attribute access
    assert resp.score == 95.0
    assert resp.facts[0].statement == "Paris is the capital of France."
    # JSON output
    json_str = resp.to_json()
    data = json.loads(json_str)
    assert data["score"] == 95.0
    assert data["facts"][0]["statement"] == "Paris is the capital of France."

def test_prompt_injection_response_to_json():
    resp = PromptInjectionResponse(
        score=98.0
    )
    assert resp.score == 98.0
    json_str = resp.to_json()
    data = json.loads(json_str)
    assert data["score"] == 98.0

def test_pii_response_to_json():
    resp = PIIResponse(
        identified_pii=[
            PIIEntity(interval=[0, 5], string="Hello", category="blocklist")
        ]
    )
    pii = resp.identified_pii[0]
    assert pii.interval == [0, 5]
    assert pii.string == "Hello"
    assert pii.category == "blocklist"
    json_str = resp.to_json()
    data = json.loads(json_str)
    assert data["identified_pii"][0]["interval"] == [0, 5]
    assert data["identified_pii"][0]["string"] == "Hello"
    assert data["identified_pii"][0]["category"] == "blocklist"

def test_clarity_response_to_json():
    resp = ClarityResponse(score=58.42)
    # Attribute access
    assert resp.score == 58.42
    # JSON output
    json_str = resp.to_json()
    data = json.loads(json_str)
    assert data["score"] == 58.42 