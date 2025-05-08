
# Import required packages
import os
from dotenv import load_dotenv
from trustwise.sdk import TrustwiseSDK
from trustwise.sdk.config import TrustwiseConfig

# Load environment variables from .env file
load_dotenv()

config = TrustwiseConfig()  # Automatically uses TW_API_KEY from environment
trustwise = TrustwiseSDK(config)

# # Try to evaluate with invalid API key
# invalid_config = TrustwiseConfig(api_key="invalid_key")
# invalid_sdk = TrustwiseSDK(invalid_config)
# result = invalid_sdk.safety.v3.faithfulness.evaluate(
#     query="What is the capital of France?",
#     response="The capital of France is Paris.",
#     context=[]
# )

context = [{
    "node_text": "Paris is the capital of France. It is known for the Eiffel Tower and the Louvre Museum.",
    "node_score": 0.95,
    "node_id": "doc:idx:1"
}]
# # Try to evaluate with invalid input (missing required field)
# result = trustwise.safety.v3.faithfulness.evaluate(
#     query="What is the capital of France?",
#     # Missing 'response' parameter
#     context=context
# )


result = trustwise.safety.v3.faithfulness.evaluate(
    query="What is the capital of France?",
    response="",
    context=context
)