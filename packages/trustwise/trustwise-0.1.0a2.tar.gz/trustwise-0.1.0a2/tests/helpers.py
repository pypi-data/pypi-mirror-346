"""Test helper functions and mock data."""
from typing import Any, Dict

# Mock API responses for safety metrics
MOCK_SAFETY_RESPONSES: Dict[str, Dict[str, Any]] = {
    "faithfulness": {
        "score": 95.5,
        "facts": [
            {
                "statement": "The capital of France is Paris",
                "label": "SUPPORTED",
                "prob": 0.95,
                "sentence_span": [0, 42]
            }
        ]
    },
    "answer_relevancy": {
        "score": 92.0,
        "generated_question": "What is the capital of France?"
    },
    "context_relevancy": {
        "score": 88.5,
        "topics": ["geography", "cities"],
        "scores": [0.9, 0.85]
    },
    "pii": {
        "identified_pii": [
            {
                "string": "john@example.com",
                "category": "EMAIL",
                "interval": [0, 15]
            }
        ]
    },
    "summarization": {
        "score": 90.0
    },
    "prompt_injection": {
        "score": 98.0
    }
}

# Mock API responses for alignment metrics
MOCK_ALIGNMENT_RESPONSES: Dict[str, Dict[str, Any]] = {
    "clarity": {
        "score": 90.0
    },
    "helpfulness": {
        "score": 85.0
    },
    "formality": {
        "score": 75.0,
        "sentences": [
            "Nuclear fusion is the process by which two or more protons and neutrons combine to form a single nucleus."
        ],
        "scores": [75.0]
    },
    "simplicity": {
        "score": 80.0,
        "simplicity_score": 0.8,
        "complexity_score": 0.2
    },
    "sensitivity": {
        "scores": {
            "health": 95.0,
            "finance": 85.0
        }
    },
    "toxicity": {
        "labels": ["identity_hate", "obscene", "threat", "insult", "toxic"],
        "scores": [0.036089644, 0.105483316, 0.027964465, 0.06207772, 0.3622106]
    },
    "tone": {
        "labels": ["professional", "friendly"],
        "scores": [90.0, 85.0],
        "primary_tone": "professional",
        "confidence": 0.95
    }
}

# Mock API responses for performance metrics
MOCK_PERFORMANCE_RESPONSES: Dict[str, Dict[str, Any]] = {
    "cost": {
        "cost_estimate_per_run": 3.722222222222222e-07,
        "total_project_cost_estimate": 0.0007444444444444445,
        "token_cost": 0.0005,
        "infrastructure_cost": 0.0002
    },
    "carbon": {
        "carbon_emitted": 0.11408193333333336,
        "sci_per_api_call": 0.0005714199095626406,
        "sci_per_10k_calls": 5.714199095626406
    }
}

def get_mock_response(endpoint: str) -> Dict[str, Any]:
    """Get mock response for a given API endpoint."""
    if "safety" in endpoint:
        metric = endpoint.split("/")[-1]
        return MOCK_SAFETY_RESPONSES.get(metric, {})
    elif "alignment" in endpoint:
        metric = endpoint.split("/")[-1]
        return MOCK_ALIGNMENT_RESPONSES.get(metric, {})
    elif "performance" in endpoint:
        metric = endpoint.split("/")[-1]
        return MOCK_PERFORMANCE_RESPONSES.get(metric, {})
    return {} 