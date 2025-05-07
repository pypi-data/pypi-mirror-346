API Reference
=============

This section provides detailed technical documentation for the Trustwise SDK. For conceptual information and best practices, see the individual metric sections.

SDK
---

.. automodule:: trustwise.sdk
   :members:
   :undoc-members:
   :show-inheritance:

Configuration
-------------

.. automodule:: trustwise.sdk.config
   :members:
   :undoc-members:
   :show-inheritance:

Types
-----

.. automodule:: trustwise.sdk.types
   :members:
   :undoc-members:
   :show-inheritance:

Safety Metrics
--------------

For detailed explanations and best practices, see :doc:`safety_metrics`.

The SDK provides access to safety metrics through the `safety` namespace. Each metric provides an `evaluate()` function with the following parameters:

faithfulness
~~~~~~~~~~~~
.. function:: safety.faithfulness.evaluate(query: str, response: str, context: :py:data:`~trustwise.sdk.types.Context`) -> FaithfulnessResponse

   Evaluate the faithfulness of a response against its context.

   Parameters:
   - query (str): The input query
   - response (str): The response to evaluate
   - context (:py:data:`~trustwise.sdk.types.Context`): Context information (list of :class:`~trustwise.sdk.types.ContextNode`)

   Returns:
   - FaithfulnessResponse: Example response:

     .. code-block:: json

        {
            "score": 95.5,
            "facts": [
                {
                    "text": "Paris is the capital of France",
                    "label": "VERIFIED",
                    "probability": 0.98
                }
            ]
        }

answer_relevancy
~~~~~~~~~~~~~~~~
.. function:: safety.answer_relevancy.evaluate(query: str, response: str, context: :py:data:`~trustwise.sdk.types.Context`) -> AnswerRelevancyResponse

   Evaluate the relevancy of a response to the query.

   Parameters:
   - query (str): The input query
   - response (str): The response to evaluate
   - context (:py:data:`~trustwise.sdk.types.Context`): Context information (list of :class:`~trustwise.sdk.types.ContextNode`)

   Returns:
   - AnswerRelevancyResponse: Example response:

     .. code-block:: json

        {
            "score": 92.0,
            "generated_question": "What is the capital city of France?",
            "relevance_score": 0.95
        }

context_relevancy
~~~~~~~~~~~~~~~~~
.. function:: safety.context_relevancy.evaluate(query: str, context: :py:data:`~trustwise.sdk.types.Context`, response: str) -> ContextRelevancyResponse

   Evaluate the relevancy of the context to the query.

   Parameters:
   - query (str): The input query
   - context (:py:data:`~trustwise.sdk.types.Context`): Context information (list of :class:`~trustwise.sdk.types.ContextNode`)
   - response (str): The response to evaluate

   Returns:
   - ContextRelevancyResponse: Example response:

     .. code-block:: json

        {
            "score": 88.5,
            "topics": ["geography", "capitals", "France"],
            "scores": [0.92, 0.85, 0.88],
            "context_relevance": 0.89
        }

summarization
~~~~~~~~~~~~~
.. function:: safety.summarization.evaluate(query: str, response: str, context: :py:data:`~trustwise.sdk.types.Context`) -> SummarizationResponse

   Evaluate the quality of a summary.

   Parameters:
   - query (str): The input query
   - response (str): The response to evaluate
   - context (:py:data:`~trustwise.sdk.types.Context`): Context information (list of :class:`~trustwise.sdk.types.ContextNode`)

   Returns:
   - SummarizationResponse: Example response:

     .. code-block:: json

        {
            "score": 90.0,
            "coverage": 0.95,
            "accuracy": 0.92,
            "conciseness": 0.88
        }

pii
~~~
.. function:: safety.pii.evaluate(text: str, allowlist: List[str], blocklist: List[str]) -> PIIResponse

   Detect personally identifiable information in text.

   Parameters:
   - text (str): The text to analyze
   - allowlist (List[str]): List of allowed PII patterns
   - blocklist (List[str]): List of blocked PII patterns

   Returns:
   - PIIResponse: Example response:

     .. code-block:: json

        {
            "identified_pii": [
                {
                    "interval": [0, 5],
                    "string": "Hello",
                    "category": "blocklist"
                },
                {
                    "interval": [94, 111],
                    "string": "www.wikipedia.org",
                    "category": "organization"
                }
            ]
        }

prompt_injection
~~~~~~~~~~~~~~~~
.. function:: safety.prompt_injection.evaluate(query: str, response: str, context: :py:data:`~trustwise.sdk.types.Context`) -> PromptInjectionResponse

   Detect potential prompt injection attempts.

   Parameters:
   - query (str): The input query
   - response (str): Optional response
   - context (:py:data:`~trustwise.sdk.types.Context`): Optional context information (list of :class:`~trustwise.sdk.types.ContextNode`)

   Returns:
   - PromptInjectionResponse: Example response:

     .. code-block:: json

        {
            "score": 98.0
        }

Alignment Metrics
-----------------

For detailed explanations and best practices, see :doc:`alignment_metrics`.

The SDK provides access to alignment metrics through the `alignment` namespace. Each metric provides an `evaluate()` function with the following parameters:

clarity
~~~~~~~
.. function:: alignment.clarity.evaluate(query: str, response: str) -> ClarityResponse

   Evaluate the clarity of a response.

   Parameters:
   - query (str): The input query
   - response (str): The response to evaluate

   Returns:
   - ClarityResponse: Example response:

     .. code-block:: json

        {
            "score": 92.5,
            "clarity_score": 0.93,
            "readability_score": 0.91
        }

helpfulness
~~~~~~~~~~~
.. function:: alignment.helpfulness.evaluate(query: str, response: str) -> HelpfulnessResponse

   Evaluate the helpfulness of a response.

   Parameters:
   - query (str): The input query
   - response (str): The response to evaluate

   Returns:
   - HelpfulnessResponse: Example response:

     .. code-block:: json

        {
            "score": 88.0,
            "helpfulness_score": 0.88,
            "completeness_score": 0.90
        }

formality
~~~~~~~~~
.. function:: alignment.formality.evaluate(response: str) -> FormalityResponse

   Evaluate the formality level of a response.

   Parameters:
   - response (str): The response to evaluate

   Returns:
   - FormalityResponse: Example response:

     .. code-block:: json

        {
            "score": 75.0,
            "formality_level": "FORMAL",
            "confidence": 0.85
        }

simplicity
~~~~~~~~~~
.. function:: alignment.simplicity.evaluate(response: str) -> SimplicityResponse

   Evaluate the simplicity of a response.

   Parameters:
   - response (str): The response to evaluate

   Returns:
   - SimplicityResponse: Example response:

     .. code-block:: json

        {
            "score": 82.0,
            "simplicity_score": 0.82,
            "complexity_score": 0.18
        }

sensitivity
~~~~~~~~~~~
.. function:: alignment.sensitivity.evaluate(response: str, topics: List[str], query: str) -> SensitivityResponse

   Evaluate the sensitivity of a response regarding specific topics.

   Parameters:
   - response (str): The response to evaluate
   - topics (List[str]): List of topics to evaluate sensitivity for
   - query (str): Optional input query

   Returns:
   - SensitivityResponse: Example response:

     .. code-block:: json

        {
            "score": 65.0,
            "sensitivity_level": "MODERATE",
            "topic_scores": {
                "politics": 0.70,
                "religion": 0.60
            }
        }

toxicity
~~~~~~~~~
.. function:: alignment.toxicity.evaluate(query: str, response: str, user_id: Optional[str] = None) -> ToxicityResponse

   Evaluate the toxicity of a response.

   Parameters:
   - query (str): Optional input query
   - response (str): Optional response
   - user_id (Optional[str]): Optional user identifier

   Returns:
   - ToxicityResponse: Example response:

     .. code-block:: json

        {
            "score": 15.0,
            "toxicity_level": "LOW",
            "confidence": 0.95,
            "categories": {
                "hate": 0.10,
                "harassment": 0.05
            }
        }

tone
~~~~
.. function:: alignment.tone.evaluate(response: str, query: Optional[str] = None) -> ToneResponse

   Evaluate the tone of a response.

   Parameters:
   - response (str): The response to evaluate
   - query (Optional[str]): Optional input query

   Returns:
   - ToneResponse: Example response:

     .. code-block:: json

        {
            "labels": ["PROFESSIONAL", "NEUTRAL"],
            "scores": [0.85, 0.75],
            "primary_tone": "PROFESSIONAL",
            "confidence": 0.90
        }

Performance Metrics
-------------------

For detailed explanations and best practices, see :doc:`performance_metrics`.

The SDK provides access to performance metrics through the ``performance`` namespace. These metrics help evaluate the cost and environmental impact of AI-generated content.

Cost
~~~~

Evaluates the cost of API usage based on token counts, model information, and infrastructure details.

.. py:function:: performance.cost.evaluate(model_name, model_type, model_provider, number_of_queries, total_prompt_tokens=None, total_completion_tokens=None, total_tokens=None, instance_type=None, average_latency=None, cost_map_name="sys") -> CostResponse

   Parameters:
   - model_name (str): Name of the model
   - model_type (str): Type of model (LLM or Reranker)
   - model_provider (str): Provider of the model
   - number_of_queries (int): Number of queries to evaluate
   - total_prompt_tokens (Optional[int]): Total prompt tokens
   - total_completion_tokens (Optional[int]): Total completion tokens
   - total_tokens (Optional[int]): Total tokens (for Together Reranker)
   - instance_type (Optional[str]): Instance type (for Hugging Face)
   - average_latency (Optional[float]): Average latency in milliseconds
   - cost_map_name (str): Name of the cost map to use

   Returns:
   - CostResponse: Example response:

     .. code-block:: json

        {
            "cost_estimate_per_run": 0.0025,
            "total_project_cost_estimate": 0.0125
        }

Carbon
~~~~~~

Evaluates the carbon emissions based on hardware specifications and infrastructure details.

.. py:function:: performance.carbon.evaluate(processor_name, provider_name, provider_region, instance_type, average_latency) -> CarbonResponse

   Parameters:
   - processor_name (str): Name of the processor
   - provider_name (str): Name of the cloud provider
   - provider_region (str): Region of the cloud provider
   - instance_type (str): Type of instance
   - average_latency (int): Average latency in milliseconds

   Returns:
   - CarbonResponse: Example response:

     .. code-block:: json

        {
            "carbon_emitted": 0.00015,
            "sci_per_api_call": 0.00003,
            "sci_per_10k_calls": 0.3
        }

Related Topics
--------------

See also:
- :doc:`safety_metrics` for conceptual information about safety metrics
- :doc:`alignment_metrics` for conceptual information about alignment metrics
- :doc:`performance_metrics` for conceptual information about performance metrics

Guardrails
----------

.. automodule:: trustwise.sdk.guardrails
   :members:
   :undoc-members:
   :show-inheritance:

The SDK provides a guardrail system to enforce safety and alignment metrics thresholds. The guardrail system can be used to:

- Set thresholds for multiple metrics
- Block responses that fail metric checks
- Execute callbacks when metrics are evaluated
- Check for PII content with custom allowlists and blocklists

Example usage:

.. code-block:: python

    trustwise = TrustwiseSDK(config)
    guardrail = trustwise.guardrails(
        thresholds={
            "faithfulness": 0.8,
            "answer_relevancy": 0.7,
            "clarity": 0.7
        },
        block_on_failure=True
    )

The guardrail system returns detailed results including:
- Pass/fail status for each metric
- Individual metric scores
- Blocking status if enabled
- Detailed evaluation results
