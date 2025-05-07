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

The evaluation returns a dictionary with:
- passed: bool (whether all checks passed)
- blocked: bool (whether the response was blocked)
- results: dict (detailed results for each metric)

Example Results
---------------

.. code-block:: python

    print("Guardrail Evaluation:")
    print(f"Passed all checks: {evaluation['passed']}")
    print(f"Response blocked: {evaluation['blocked']}")
    for metric, result in evaluation['results'].items():
        print(f" - {metric}: {result['passed']} (score: {result['result'].get('score')})")

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