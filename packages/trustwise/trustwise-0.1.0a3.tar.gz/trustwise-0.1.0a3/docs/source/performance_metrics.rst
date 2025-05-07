Performance Metrics
===================

The Trustwise SDK provides performance metrics to evaluate the cost and environmental impact of AI-generated content. All metrics are available in version 1 of the API.

Overview
--------

Performance metrics help optimize AI system operations by providing insights into:
- Cost efficiency
- Environmental impact
- Resource utilization
- System scalability

Best Practices
--------------

1. Monitor costs regularly
2. Optimize for environmental impact
3. Consider total cost of ownership
4. Plan for scalability
5. Track performance trends

Cost Evaluation
---------------

The cost evaluation supports different model types and providers with specific requirements. This metric helps optimize resource allocation and budget planning.

Use Cases:
- Budget forecasting
- Resource optimization
- Cost comparison
- ROI analysis

Model Types
~~~~~~~~~~~~

The SDK supports two types of models:

- **LLM (Language Model)**: For language model providers like OpenAI, Hugging Face, and Azure
- **Reranker (Reranking Model)**: For reranking model providers like Azure Reranker, Cohere Reranker, and Together Reranker

LLM Providers
~~~~~~~~~~~~~~

OpenAI
^^^^^^^^

Required Fields:
    - ``total_prompt_tokens`` (:class:`int` or :class:`None`, positive)
    - ``total_completion_tokens`` (:class:`int` or :class:`None`, positive)
    - ``model_name`` (:class:`str`, non-empty)
    - ``model_type`` (:class:`str`, must be "LLM")
    - ``model_provider`` (:class:`str`, must be "OpenAI")
    - ``number_of_queries`` (:class:`int`, positive)
    - ``cost_map_name`` (:class:`str`, defaults to "sys")

Optional Fields:
    - ``instance_type``
    - ``average_latency``

Example:

.. code-block:: python

    result = trustwise.performance.v1.cost.evaluate(
        model_name="gpt-3.5-turbo",
        model_type="LLM",
        model_provider="OpenAI",
        number_of_queries=5,
        total_prompt_tokens=950,
        total_completion_tokens=50
    )

Best Practices:
- Monitor token usage
- Optimize prompt length
- Consider model selection
- Track cost trends

Hugging Face
^^^^^^^^^^^^

Required Fields:
    - ``total_prompt_tokens`` (:class:`int` or :class:`None`, positive)
    - ``total_completion_tokens`` (:class:`int` or :class:`None`, positive)
    - ``model_name`` (:class:`str`, non-empty)
    - ``model_type`` (:class:`str`, must be "LLM")
    - ``model_provider`` (:class:`str`, must be "HuggingFace")
    - ``number_of_queries`` (:class:`int`, positive)
    - ``instance_type`` (:class:`str` or :class:`None`, non-empty)
    - ``average_latency`` (:class:`float` or :class:`None`, positive)
    - ``cost_map_name`` (:class:`str`, defaults to "sys")

Example:

.. code-block:: python

    result = trustwise.performance.v1.cost.evaluate(
        model_name="mistral-7b",
        model_type="LLM",
        model_provider="HuggingFace",
        number_of_queries=5,
        total_prompt_tokens=950,
        total_completion_tokens=50,
        instance_type="a1.large",
        average_latency=653
    )

Performance Considerations:
- Optimize instance selection
- Monitor latency
- Consider scaling needs
- Track resource utilization

Azure
^^^^^^

Required Fields:
    - ``total_prompt_tokens`` (:class:`int` or :class:`None`, positive)
    - ``total_completion_tokens`` (:class:`int` or :class:`None`, positive)
    - ``model_name`` (:class:`str`, non-empty)
    - ``model_type`` (:class:`str`, must be "LLM")
    - ``model_provider`` (:class:`str`, must be "Azure")
    - ``number_of_queries`` (:class:`int`, positive)
    - ``cost_map_name`` (:class:`str`, defaults to "sys")

Optional Fields:
    - ``instance_type``
    - ``average_latency``

Example:

.. code-block:: python

    result = trustwise.performance.v1.cost.evaluate(
        model_name="azure-gpt-3.5-turbo",
        model_type="LLM",
        model_provider="Azure",
        number_of_queries=5,
        total_prompt_tokens=950,
        total_completion_tokens=50
    )

Best Practices:
- Monitor Azure credits
- Optimize deployment
- Consider region selection
- Track usage patterns

Reranker Providers
~~~~~~~~~~~~~~~~~~

Azure Reranker
^^^^^^^^^^^^^^

Required Fields:
    - ``model_name`` (:class:`str`, non-empty)
    - ``model_type`` (:class:`str`, must be "Reranker")
    - ``model_provider`` (:class:`str`, must be "Azure Reranker")
    - ``number_of_queries`` (:class:`int`, positive)
    - ``cost_map_name`` (:class:`str`, defaults to "sys")

Optional Fields:
    - ``instance_type``
    - ``average_latency``

Example:

.. code-block:: python

    result = trustwise.performance.v1.cost.evaluate(
        model_name="azure-reranker",
        model_type="Reranker",
        model_provider="Azure Reranker",
        number_of_queries=5
    )

Performance Considerations:
- Optimize query batching
- Monitor throughput
- Consider caching
- Track latency

Cohere Reranker
^^^^^^^^^^^^^^^

Required Fields:
    - ``model_name`` (:class:`str`, non-empty)
    - ``model_type`` (:class:`str`, must be "Reranker")
    - ``model_provider`` (:class:`str`, must be "Cohere Reranker")
    - ``number_of_queries`` (:class:`int`, positive)
    - ``cost_map_name`` (:class:`str`, defaults to "sys")

Optional Fields:
    - ``instance_type``
    - ``average_latency``

Example:

.. code-block:: python

    result = trustwise.performance.v1.cost.evaluate(
        model_name="cohere-reranker",
        model_type="Reranker",
        model_provider="Cohere Reranker",
        number_of_queries=5
    )

Best Practices:
- Monitor API limits
- Optimize batch size
- Consider rate limits
- Track usage patterns

Together Reranker
^^^^^^^^^^^^^^^^^

Required Fields:
    - ``model_name`` (:class:`str`, non-empty)
    - ``model_type`` (:class:`str`, must be "Reranker")
    - ``model_provider`` (:class:`str`, must be "Together Reranker")
    - ``total_tokens`` (:class:`int` or :class:`None`, positive)
    - ``cost_map_name`` (:class:`str`, defaults to "sys")

Optional Fields:
    - ``instance_type``
    - ``average_latency``

Example:

.. code-block:: python

    result = trustwise.performance.v1.cost.evaluate(
        model_name="together-reranker",
        model_type="Reranker",
        model_provider="Together Reranker",
        number_of_queries=5,
        total_tokens=1000
    )

Performance Considerations:
- Monitor token usage
- Optimize batch size
- Consider rate limits
- Track latency

Response Format
~~~~~~~~~~~~~~~

The cost evaluation returns a :class:`~trustwise.sdk.types.CostResponse` object containing:

- ``cost_estimate_per_run`` (:class:`float`): Estimated cost per API call
- ``total_project_cost_estimate`` (:class:`float`): Estimated total cost for all queries

Carbon Evaluation
-----------------

Evaluates the carbon emissions based on hardware specifications and infrastructure details. This metric helps optimize environmental impact.

Use Cases:
- Environmental impact assessment
- Sustainability reporting
- Resource optimization
- Green computing initiatives

Required Fields:
    - ``processor_name`` (string): Name of the processor (e.g., "RTX 3080")
    - ``provider_name`` (string): Name of the cloud provider (e.g., "aws")
    - ``provider_region`` (string): Region of the cloud provider (e.g., "us-east-1")
    - ``instance_type`` (string): Type of instance (e.g., "a1.metal")
    - ``average_latency`` (integer): Average latency in milliseconds

Example:

.. code-block:: python

    result = trustwise.performance.v1.carbon.evaluate(
        processor_name="RTX 3080",
        provider_name="aws",
        provider_region="us-east-1",
        instance_type="a1.metal",
        average_latency=653
    )

Response Format
~~~~~~~~~~~~~~~

The carbon evaluation returns a :class:`~trustwise.sdk.types.CarbonResponse` object containing:

- ``carbon_emitted`` (:class:`float`): Total carbon emissions in kg CO2e
- ``sci_per_api_call`` (:class:`float`): Software Carbon Intensity per API call
- ``sci_per_10k_calls`` (:class:`float`): Software Carbon Intensity per 10,000 API calls

Best Practices:
- Consider region selection
- Optimize resource utilization
- Monitor environmental impact
- Track sustainability metrics

Related Topics
--------------

See also:
- :doc:`safety_metrics`
- :doc:`alignment_metrics`
- :doc:`api` for technical implementation details 