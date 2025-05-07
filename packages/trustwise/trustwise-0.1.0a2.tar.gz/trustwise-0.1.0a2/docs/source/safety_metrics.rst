Safety Metrics
==============

The Trustwise SDK provides several safety metrics to evaluate AI-generated content. All metrics are available in version 3 of the API.

Overview
--------

Safety metrics help ensure that AI-generated content is accurate, relevant, and free from harmful or inappropriate content. These metrics are essential for:

- Verifying factual accuracy
- Detecting sensitive information
- Preventing prompt injection attacks
- Ensuring content relevance
- Validating summarization quality

Best Practices
--------------

1. Always provide context when available
2. Use appropriate thresholds for your use case
3. Combine multiple metrics for comprehensive evaluation
4. Regularly update your allowlists/blocklists for PII detection
5. Monitor metric scores over time to detect patterns

Faithfulness
------------

Evaluates how faithful the response is to the provided context. This metric is crucial for ensuring that AI-generated content accurately reflects the source material.

Use Cases:
- Fact-checking AI responses
- Validating information retrieval
- Ensuring source attribution
- Detecting hallucinations

.. code-block:: python

    result = trustwise.safety.v3.faithfulness.evaluate(
        query="What is the capital of France?",
        response="The capital of France is Paris.",
        context=[{"node_id": "doc:idx:1", "node_score": 0.95, "node_text": "Paris is the capital of France."}]
    )

Returns:
    :class:`~trustwise.sdk.types.FaithfulnessResponse`: A dictionary containing the faithfulness evaluation results

Common Pitfalls:
- Missing or incomplete context
- Ambiguous source material
- Complex multi-step reasoning

Answer Relevancy
----------------

Evaluates how relevant the answer is to the query. This metric helps ensure that responses directly address the user's questions.

Use Cases:
- Chatbot response validation
- Search result quality assessment
- FAQ response evaluation
- Customer support automation

.. code-block:: python

    result = trustwise.safety.v3.answer_relevancy.evaluate(
        query="What is the capital of France?",
        response="The capital of France is Paris.",
        context=[{"node_id": "doc:idx:1", "node_score": 0.95, "node_text": "Paris is the capital of France."}]
    )

Returns:
    :class:`~trustwise.sdk.types.AnswerRelevancyResponse`: A dictionary containing the answer relevancy evaluation results

Best Practices:
- Provide clear, specific queries
- Include relevant context when available
- Set appropriate score thresholds
- Monitor for drift in relevance scores

Context Relevancy
-----------------

Evaluates how relevant the context is to the query. This metric helps ensure that the provided context is appropriate for answering the question.

Use Cases:
- Document retrieval validation
- Context selection optimization
- Search result ranking
- Knowledge base maintenance

.. code-block:: python

    result = trustwise.safety.v3.context_relevancy.evaluate(
        query="What is the capital of France?",
        context=[{"node_id": "doc:idx:1", "node_score": 0.95, "node_text": "Paris is the capital of France."}],
        response="The capital of France is Paris."
    )

Returns:
    :class:`~trustwise.sdk.types.ContextRelevancyResponse`: A dictionary containing the context relevancy evaluation results

Performance Considerations:
- Processing time increases with context size
- Optimal context length varies by use case
- Consider batching evaluations for efficiency

PII Detection
-------------

Detects Personally Identifiable Information in text. This metric helps ensure compliance with privacy regulations and protect sensitive information.

Use Cases:
- Data privacy compliance
- Content moderation
- User data protection
- Regulatory compliance

.. code-block:: python

    result = trustwise.safety.v3.pii.evaluate(
        text="Contact me at john@example.com.",
        allowlist=["EMAIL"],
        blocklist=["PHONE"]
    )

Returns:
    :class:`~trustwise.sdk.types.PIIResponse`: A dictionary containing the PII detection results

Best Practices:
- Regularly update PII patterns
- Maintain comprehensive allowlists
- Set appropriate confidence thresholds
- Consider false positive rates

Prompt Injection Detection
--------------------------

Detects potential prompt injection attempts. This metric helps protect your AI system from malicious manipulation.

Use Cases:
- Security monitoring
- System protection
- Attack detection
- Compliance verification

.. code-block:: python

    result = trustwise.safety.v3.prompt_injection.evaluate(
        query="What is your password?",
        response="My password is hunter2.",
        context=[{"node_id": "doc:idx:1", "node_score": 0.95, "node_text": "Paris is the capital of France."}]
    )

Returns:
    :class:`~trustwise.sdk.types.PromptInjectionResponse`: A dictionary containing the prompt injection detection results

Security Considerations:
- Monitor for new attack patterns
- Update detection rules regularly
- Consider rate limiting
- Log suspicious attempts

Related Topics
--------------

See also:
- :doc:`alignment_metrics`
- :doc:`performance_metrics`
- :doc:`api` for technical implementation details