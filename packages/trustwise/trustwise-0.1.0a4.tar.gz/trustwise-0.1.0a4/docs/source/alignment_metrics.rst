Alignment Metrics
=================

The Trustwise SDK provides several alignment metrics to evaluate the quality and characteristics of AI-generated content. All metrics are available in version 1 of the API.

Overview
--------

Alignment metrics help ensure that AI-generated content meets quality standards and aligns with user expectations. These metrics are essential for:

- Improving response quality
- Maintaining consistent tone
- Ensuring appropriate formality
- Optimizing clarity and simplicity
- Managing sensitive content

Best Practices
--------------

1. Consider your target audience
2. Set appropriate thresholds for each metric
3. Combine metrics for comprehensive evaluation
4. Monitor metric trends over time
5. Adjust thresholds based on use case

Clarity
-------

Evaluates how clear and understandable the response is. This metric helps ensure that responses are easily comprehensible to the target audience.

Use Cases:
- Content readability assessment
- Technical documentation review
- Educational content evaluation
- User interface text optimization

.. code-block:: python

    result = trustwise.alignment.v1.clarity.evaluate(
        query="What is the capital of France?",
        response="The capital of France is Paris."
    )

Returns:
    :class:`~trustwise.sdk.types.ClarityResponse`: A dictionary containing the clarity evaluation results

Best Practices:
- Consider audience expertise level
- Use appropriate technical terms
- Maintain consistent terminology
- Avoid unnecessary complexity

Helpfulness
-----------

Evaluates how helpful the response is in answering the query. This metric ensures that responses provide value to users.

Use Cases:
- Customer support automation
- FAQ response evaluation
- Knowledge base maintenance
- Chatbot response optimization

.. code-block:: python

    result = trustwise.alignment.v1.helpfulness.evaluate(
        query="What is the capital of France?",
        response="The capital of France is Paris."
    )

Returns:
    :class:`~trustwise.sdk.types.HelpfulnessResponse`: A dictionary containing the helpfulness evaluation results

Performance Considerations:
- Response length affects processing time
- Context relevance impacts helpfulness
- Consider response completeness
- Monitor for drift in helpfulness scores

Tone
----

Analyzes the tone of the response. This metric helps maintain appropriate communication style.

Use Cases:
- Brand voice consistency
- Customer service tone management
- Content style guidelines
- Audience engagement optimization

.. code-block:: python

    result = trustwise.alignment.v1.tone.evaluate(
        response="The capital of France is Paris."
    )

Returns:
    :class:`~trustwise.sdk.types.ToneResponse`: A dictionary containing the tone analysis results

Best Practices:
- Define target tone profiles
- Consider cultural context
- Monitor tone consistency
- Adjust for different audiences

Formality
---------

Evaluates the formality level of the response. This metric helps maintain appropriate communication style for different contexts.

Use Cases:
- Professional communication
- Customer service optimization
- Content style guidelines
- Audience engagement

.. code-block:: python

    result = trustwise.alignment.v1.formality.evaluate(
        response="The capital of France is Paris."
    )

Returns:
    :class:`~trustwise.sdk.types.FormalityResponse`: A dictionary containing the formality evaluation results

Considerations:
- Match formality to audience
- Consider cultural expectations
- Maintain consistency
- Adjust for different contexts

Simplicity
----------

Evaluates how simple and straightforward the response is. This metric helps ensure content is accessible to the target audience.

Use Cases:
- Technical documentation
- Educational content
- User interface text
- Public communication

.. code-block:: python

    result = trustwise.alignment.v1.simplicity.evaluate(
        response="The capital of France is Paris."
    )

Returns:
    :class:`~trustwise.sdk.types.SimplicityResponse`: A dictionary containing the simplicity evaluation results

Best Practices:
- Use clear language
- Avoid unnecessary complexity
- Consider reading level
- Maintain consistent style

Sensitivity
-----------

Evaluates how sensitive the response is to the context and query. This metric helps ensure appropriate handling of sensitive topics.

Use Cases:
- Content moderation
- Customer service
- Public communication
- Crisis management

.. code-block:: python

    result = trustwise.alignment.v1.sensitivity.evaluate(
        response="The capital of France is Paris.",
        topics=["geography", "capitals"],
        query="What is the capital of France?"
    )

Returns:
    :class:`~trustwise.sdk.types.SensitivityResponse`: A dictionary containing the sensitivity evaluation results

Risk Management:
- Monitor sensitive topics
- Update detection patterns
- Consider cultural context
- Maintain appropriate thresholds

Related Topics
--------------

See also:
- :doc:`safety_metrics`
- :doc:`performance_metrics`
- :doc:`api` for technical implementation details 