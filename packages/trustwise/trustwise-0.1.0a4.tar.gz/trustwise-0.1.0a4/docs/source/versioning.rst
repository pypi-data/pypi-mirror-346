API Versioning
==============

The Trustwise SDK provides flexible version management through both explicit version paths and default version usage for backward compatibility.

Version Management
------------------

Available Versions
~~~~~~~~~~~~~~~~~~

Get the available API versions:

.. code-block:: python

    from trustwise.sdk import TrustwiseSDK, TrustwiseConfig

    config = TrustwiseConfig(api_key="your-api-key")
    trustwise = TrustwiseSDK(config)

    # Get available versions
    versions = trustwise.get_versions()

Current Version
~~~~~~~~~~~~~~~~~~~~~

Get and set the current default version for a specific API:

.. code-block:: python

    # Get current version
    trustwise.safety.version

    # Set default safety version
    trustwise.safety.set_version("v3")

    # Get current version
    trustwise.safety.version

Usage Patterns
--------------

The SDK supports three equivalent ways to access API versions:

Explicit Version Path
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Using explicit version path
    result = trustwise.safety.v3.faithfulness.evaluate(
        query="What is the capital of France?",
        response="The capital of France is Paris.",
        context=[{"node_id": "doc:idx:1", "node_score": 0.95, "node_text": "Paris is the capital of France."}]
    )

Default Version
~~~~~~~~~~~~~~~

.. code-block:: python

    # Using default version (backward compatible)
    result = trustwise.safety.faithfulness.evaluate(
        query="What is the capital of France?",
        response="The capital of France is Paris.",
        context=[{"node_id": "doc:idx:1", "node_score": 0.95, "node_text": "Paris is the capital of France."}]
    )

Mixed Approach
~~~~~~~~~~~~~~~

.. code-block:: python

    # Set default version and use it
    trustwise.safety.set_version("v3")
    result = trustwise.safety.faithfulness.evaluate(
        query="What is the capital of France?",
        response="The capital of France is Paris.",
        context=[{"node_id": "doc:idx:1", "node_score": 0.95, "node_text": "Paris is the capital of France."}]
    )

Supported Versions
------------------

The following API versions are currently supported:

- **Safety API**: v3
- **Alignment API**: v1
- **Performance API**: v1 