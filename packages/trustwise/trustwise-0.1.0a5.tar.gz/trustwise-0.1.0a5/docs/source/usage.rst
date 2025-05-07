Usage
=================

This section provides comprehensive documentation on how to use the Trustwise SDK, including basic setup, configuration, and detailed examples.

Basic Setup
-----------

Here's a quick example of how to set up and use the Trustwise SDK:

.. code-block:: python

    import os
    from trustwise.sdk import TrustwiseSDK
    from trustwise.sdk.config import TrustwiseConfig

    # Initialize the SDK
    config = TrustwiseConfig(api_key=os.environ["TW_API_KEY"])
    trustwise = TrustwiseSDK(config)

Configuration
-------------

The SDK can be configured using environment variables or directly:

.. code-block:: python

    # Using environment variables
    os.environ["TW_API_KEY"] = "your-api-key"
    os.environ["TW_BASE_URL"] = "https://api.trustwise.ai"
    config = TrustwiseConfig()

    # Or directly
    config = TrustwiseConfig(
        api_key="your-api-key",
        base_url="https://api.trustwise.ai"
    )

Examples
--------

Safety Metrics
~~~~~~~~~~~~~~

.. code-block:: python

    # Example context
    context = [{
        "node_text": "Paris is the capital of France.",
        "node_score": 0.95,
        "node_id": "doc:idx:1"
    }]

    # Evaluate faithfulness
    result = trustwise.safety.v3.faithfulness.evaluate(
        query="What is the capital of France?",
        response="The capital of France is Paris.",
        context=[{"node_id": "doc:idx:1", "node_score": 0.95, "node_text": "Paris is the capital of France."}]
    )
    print(f"Faithfulness score: {result.score}")
    # Example result object:
    # {
    #     "score": 95.5,
    #     "facts": [
    #         {
    #             "statement": "Paris is the capital of France",
    #             "label": "VERIFIED",
    #             "prob": 0.98,
    #             "sentence_span": [0, 28]
    #         }
    #     ]
    # }

    # Evaluate PII detection
    pii_result = trustwise.safety.v3.pii.evaluate(
        text="Contact me at john@example.com.",
        allowlist=["EMAIL"],
        blocklist=["PHONE"]
    )
    print(f"PII detection result: {pii_result}")
    # Example result object:
    # {
    #     "identified_pii": [
    #         {
    #             "interval": [0, 5],
    #             "string": "Hello",
    #             "category": "blocklist"
    #         },
    #         {
    #             "interval": [94, 111],
    #             "string": "www.wikipedia.org",
    #             "category": "organization"
    #         }
    #     ]
    # }

Alignment Metrics
~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Evaluate clarity
    result = trustwise.alignment.v1.clarity.evaluate(
        query="What is the capital of France?",
        response="The capital of France is Paris."
    )
    print(f"Clarity score: {result.score}")
    # Example result object:
    # {
    #     "score": 92.5
    # }

    # Evaluate toxicity
    toxicity_result = trustwise.alignment.v1.toxicity.evaluate(
        query="What is the capital of France?",
        response="That's a stupid question."
    )
    print(f"Toxicity scores: {toxicity_result.scores}")
    # Example result object:
    # {
    #     "labels": ["hate", "harassment"],
    #     "scores": [0.10, 0.05]
    # }

Guardrails
~~~~~~~~~~

.. code-block:: python

    # Create a multi-metric guardrail
    guardrail = trustwise.guardrails(
        thresholds={
            "faithfulness": 0.8,
            "answer_relevancy": 0.7,
            "clarity": 0.7
        },
        block_on_failure=True
    )

    # Evaluate with multiple metrics
    evaluation = guardrail.evaluate_response(
        query="What is the capital of France?",
        response="The capital of France is Paris.",
        context=context
    )

    print("Guardrail Evaluation:")
    print(f"Passed all checks: {evaluation['passed']}")
    print(f"Response blocked: {evaluation['blocked']}")
    for metric, result in evaluation['results'].items():
        print(f" - {metric}: {result['passed']} (score: {result['result'].get('score')})")

Versioning
~~~~~~~~~~

.. code-block:: python

    # Get current versions
    versions = trustwise.get_versions()
    print(f"Default versions: {versions}")

    # Using different version access methods
    result1 = trustwise.safety.v3.faithfulness.evaluate(...)
    result2 = trustwise.safety.v3.faithfulness.evaluate(...)  # Uses default v3
    print(f"Scores identical: {result1['score'] == result2['score']}")

Performance Metrics
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Evaluate cost
    cost_result = trustwise.performance.v1.cost.evaluate(
        total_prompt_tokens=950,
        total_completion_tokens=50,
        model_name="gpt-3.5-turbo",
        model_provider="OpenAI",
        average_latency=653,
        number_of_queries=5,
        instance_type="a1.large"
    )
    print(f"Total cost: {cost_result.total_project_cost_estimate}")
    print(f"Cost per query: {cost_result.cost_estimate_per_run}")
    # Example result object:
    # {
    #     "cost_estimate_per_run": 0.0025,
    #     "total_project_cost_estimate": 0.0125
    # }

    # Evaluate carbon emissions
    carbon_result = trustwise.performance.v1.carbon.evaluate(
        processor_name="RTX 3080",
        provider_name="aws",
        provider_region="us-east-1",
        instance_type="a1.metal",
        average_latency=653
    )
    print(f"Total emissions: {carbon_result.carbon_emitted}")
    print(f"SCI per API call: {carbon_result.sci_per_api_call}")
    print(f"SCI per 10k calls: {carbon_result.sci_per_10k_calls}")
    # Example result object:
    # {
    #     "carbon_emitted": 0.00015,
    #     "sci_per_api_call": 0.00003,
    #     "sci_per_10k_calls": 0.3
    # } 