Guardrails
==========

The Trustwise SDK provides a guardrail system to automatically validate responses against multiple metrics.

Creating Guardrails
-------------------

Create a guardrail with specific thresholds for different metrics:

.. code-block:: python

    guardrail = trustwise.guardrails(
        thresholds={
            "faithfulness": 90.0,    # Minimum faithfulness score
            "answer_relevancy": 85.0, # Minimum answer relevancy score
            "clarity": 70.0          # Minimum clarity score
        },
        block_on_failure=True        # Whether to block responses that fail
    )

Using Guardrails
----------------

Evaluate a response with the guardrail:

.. code-block:: python

    evaluation = guardrail.evaluate_response(
        query="What is the capital of France?",
        response="The capital of France is Paris.",
        context=context
    )

The evaluation returns a :class:`GuardrailResponse` object, which provides convenient access to results as Python objects and supports serialization to dict or JSON.

Pythonic Access Example
----------------------

.. code-block:: python

    print("Guardrail Evaluation:")
    print(f"Passed all checks: {evaluation.passed}")
    print(f"Response blocked: {evaluation.blocked}")
    for metric, result in evaluation.results.items():
        # result['result'] is a Pydantic model, so access .score directly
        print(f" - {metric}: {result['passed']} (score: {result['result'].score})")
        # Example for faithfulness result['result']:
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

Serialization Example
---------------------

To get a JSON-serializable dict or a JSON string, use the provided methods:

.. code-block:: python

    # As a Python dict
    evaluation_dict = evaluation.to_dict()
    print(evaluation_dict)

    # As a JSON string
    print(evaluation.to_json(indent=2))

Available Metrics
-----------------

You can use any of the following metrics in your guardrails:
- faithfulness
- answer_relevancy
- context_relevancy
- clarity
- helpfulness
- tone
- formality
- simplicity
- sensitivity 