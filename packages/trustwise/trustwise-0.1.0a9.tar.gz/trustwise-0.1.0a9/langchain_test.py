"""
Simple example of using Trustwise SDK with LangChain.

This example demonstrates a basic integration with LangChain
using the document about tire maintenance.
"""

import os
import traceback
from typing import Any, Dict, List

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser

# Import LangChain components
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Import Trustwise SDK - Fix the import path based on your structure
from trustwise import Trustwise

# Set your OpenAI API key
# os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# Set your Trustwise API key
# os.environ["TRUSTWISE_API_KEY"] = "your-trustwise-api-key"


def run_trustwise_langchain_example():
    """Run the Trustwise LangChain example"""

    print("Trustwise SDK with LangChain Example")
    print("------------------------------------")

    # Load the tire maintenance document
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
    document_path = os.path.join(current_dir, "tire_maintenance.txt")

    # Create sample document if it doesn't exist
    if not os.path.exists(document_path):
        sample_text = """
        # Tire Maintenance Guide
        
        ## Checking Tire Pressure
        
        To check tire pressure, you need a tire pressure gauge. These can be purchased at auto parts stores for $1-7.
        
        Follow these steps:
        1. Remove the valve cap
        2. Press the gauge onto the valve firmly
        3. Read the pressure measurement
        4. Add air if needed and recheck
        
        Proper tire pressure improves fuel efficiency and extends tire life.
        
        The recommended tire pressure for your vehicle can be found:
        - On a sticker in the driver's door jamb
        - In the vehicle owner's manual
        - Sometimes on the inside of the fuel filler door
        
        Most passenger vehicles have a recommended pressure between 32-35 PSI.
        """
        with open(document_path, "w") as f:
            f.write(sample_text)
        print(f"Created sample document at {document_path}")

    with open(document_path, "r") as f:
        document_content = f.read()

    # Create Document object
    document = Document(page_content=document_content)

    # Initialize Trustwise
    trustwise_api_key = os.environ.get("TRUSTWISE_API_KEY")
    if not trustwise_api_key:
        print(
            "Warning: TRUSTWISE_API_KEY environment variable not set. Using placeholder."
        )
        trustwise_api_key = (
            "your-trustwise-api-key"  # This won't work with actual API calls
        )

    trustwise = Trustwise(api_key=trustwise_api_key)

    # Get the Trustwise callback handler for LangChain - using the correct path
    try:
        # Try three different import paths based on your structure
        try:
            from trustwise.integrations import get_langchain_callback_handler
        except ImportError:
            try:
                from trustwise import integrations

                get_langchain_callback_handler = (
                    integrations.get_langchain_callback_handler
                )
            except (ImportError, AttributeError):
                from trustwise import get_langchain_callback_handler

        TrustwiseCallbackHandler = get_langchain_callback_handler()

        if TrustwiseCallbackHandler is None:
            raise ImportError(
                "TrustwiseCallbackHandler is None - LangChain may not be installed correctly"
            )

        print("Successfully imported TrustwiseCallbackHandler")
    except Exception as e:
        print(f"Error importing callback handler: {str(e)}")
        traceback.print_exc()
        return

    # Create thresholds for metrics
    thresholds = {"clarity": 70.0, "helpfulness": 70.0}

    # Create callback function for threshold failures
    def on_threshold_failure(metric, result):
        print(
            f"⚠️ Warning: {metric} score {result['score']:.2f} is below threshold {thresholds[metric]}"
        )

    # Create debug wrapper for the callback handler
    class DebugTrustwiseCallbackHandler(TrustwiseCallbackHandler):
        def on_chain_start(
            self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs
        ):
            print(f"[Debug] Chain Start triggered with inputs: {list(inputs.keys())}")
            super().on_chain_start(serialized, inputs, **kwargs)
            print(f"[Debug] Current query: {getattr(self, '_current_query', None)}")
            print(
                f"[Debug] Current context: {getattr(self, '_current_context', None) is not None}"
            )

        def on_chain_end(self, outputs: Dict[str, Any], **kwargs):
            print(f"[Debug] Chain End triggered with outputs: {list(outputs.keys())}")
            if "output" in outputs:
                print(f"[Debug] Output type: {type(outputs['output'])}")
                print(f"[Debug] Output preview: {str(outputs['output'])[:50]}...")

            super().on_chain_end(outputs, **kwargs)
            print(f"[Debug] Latest results: {getattr(self, 'latest_results', None)}")

    # Initialize callback handler
    trustwise_handler = DebugTrustwiseCallbackHandler(
        trustwise_client=trustwise,
        metrics=["clarity", "helpfulness"],
        threshold_config=thresholds,
        on_threshold_failure=on_threshold_failure,
    )

    # Create a simple retrieval function that returns our document
    def retrieve_docs(query: str) -> List[Document]:
        return [document]

    # Create LLM
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        print("Warning: OPENAI_API_KEY environment variable not set.")
        print("Example will run in simulated mode without making real API calls.")

        # Create a mock chain for testing without API keys
        def mock_chain(input_text, config=None):
            query = input_text
            if query.lower().startswith("how do i check"):
                return "To check tire pressure, you need a pressure gauge. Remove the valve cap, press the gauge onto the valve firmly, and read the pressure."
            elif query.lower().startswith("what tools"):
                return "The main tool you need is a tire pressure gauge, which can be purchased at auto parts stores for $1-7."
            elif query.lower().startswith("where can i find"):
                return "You can find the recommended tire pressure on a sticker in the driver's door jamb, in the vehicle owner's manual, or sometimes on the inside of the fuel filler door."
            else:
                return "I don't have specific information about that question."

        chain = mock_chain
    else:
        llm = ChatOpenAI(temperature=0.2)

        # Create prompt template
        prompt = PromptTemplate.from_template(
            "Answer the following question based on the context:\n\n"
            "Context: {context}\n\n"
            "Question: {input}\n\n"
            "Answer:"
        )

        # Create simple chain - fixed to work with current LangChain
        chain = (
            {
                "context": lambda x: "\n".join(
                    [doc.page_content for doc in retrieve_docs(x)]
                ),
                "input": RunnablePassthrough(),
            }
            | prompt
            | llm
            | StrOutputParser()
        )

    # Ask some questions
    questions = [
        "How do I check tire pressure?",
        "What tools do I need to check tire pressure?",
        "Where can I find the recommended tire pressure for my car?",
    ]

    for i, question in enumerate(questions, 1):
        print(f"\n[Question {i}] {question}")
        try:
            # Run chain with Trustwise evaluation
            if callable(getattr(chain, "invoke", None)):
                # For LangChain's Runnable protocol
                response = chain.invoke(
                    question, config={"callbacks": [trustwise_handler]}
                )
            else:
                # For the mock chain
                response = chain(question, config={"callbacks": [trustwise_handler]})

                # Manually trigger callbacks since we're using a mock
                if hasattr(trustwise_handler, "on_chain_start"):
                    trustwise_handler.on_chain_start(
                        serialized={}, inputs={"input": question}
                    )

                if hasattr(trustwise_handler, "on_chain_end"):
                    trustwise_handler.on_chain_end(outputs={"output": response})

            print(f"[Response] {response}")

            # Print evaluation results with more detailed logging
            print("[Evaluation Results]")
            if hasattr(trustwise_handler, "latest_results"):
                if not trustwise_handler.latest_results:
                    print("No evaluation results available")
                else:
                    for metric, result in trustwise_handler.latest_results.items():
                        if isinstance(result, dict) and "score" in result:
                            print(f"- {metric.capitalize()}: {result['score']:.2f}")
                        else:
                            print(
                                f"- {metric.capitalize()}: Result format unexpected - {result}"
                            )
            else:
                print("No latest_results attribute found in handler")

        except Exception as e:
            print(f"Error during evaluation: {str(e)}")
            traceback.print_exc()

        print("-" * 40)


if __name__ == "__main__":
    run_trustwise_langchain_example()
