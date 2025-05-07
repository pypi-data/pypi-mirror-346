Welcome to Trustwise SDK's documentation!
=========================================

Trustwise SDK is a powerful tool for evaluating AI-generated content with Trustwise's Safety, Alignment, and Performance metrics.

Quickstart
----------

1. **Install the SDK:**

   .. code-block:: bash

      pip install trustwise

2. **Set up and run your first evaluation:**

   .. code-block:: python

      import os
      from trustwise.sdk import TrustwiseSDK
      from trustwise.sdk.config import TrustwiseConfig

      # Initialize the SDK
      config = TrustwiseConfig(api_key=os.environ["TW_API_KEY"])
      trustwise = TrustwiseSDK(config)

      # Evaluate faithfulness
      result = trustwise.safety.v3.faithfulness.evaluate(
          query="What is the capital of France?",
          response="The capital of France is Paris.",
          context=[{"node_id": "doc:idx:1", "node_score": 0.95, "node_text": "Paris is the capital of France."}]
      )
      print(f"Faithfulness score: {result['score']}")

Documentation Overview
----------------------

This documentation is organized to help you quickly find what you need:

- **Usage:** Get started with basic setup, configuration, and comprehensive examples (:doc:`usage`)
- **Safety Metrics:** Assess faithfulness, relevancy, and PII detection (:doc:`safety_metrics`)
- **Alignment Metrics:** Evaluate clarity, helpfulness, tone, and more (:doc:`alignment_metrics`)
- **Performance Metrics:** Evaluate cost and environmental impact (:doc:`performance_metrics`)
- **Guardrails:** Enforce multi-metric validation and block unsafe responses (:doc:`guardrails`)
- **API Versioning:** Use explicit or default API versions for flexibility (:doc:`versioning`)
- **Changelog:** Track documentation changes and feature additions (:doc:`changelog`)

.. toctree::
   :maxdepth: 2
   :caption: Contents

   installation
   usage
   api
   safety_metrics
   alignment_metrics
   performance_metrics
   guardrails
   versioning
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 