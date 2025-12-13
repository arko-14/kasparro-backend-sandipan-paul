import pytest
import os
import json
from src.schemas import ProductData
from src.agents import AgentFactory

# Define dummy data for testing
SAMPLE_DATA = {
    "name": "Test Serum",
    "concentration": "5%",
    "skin_type": "All",
    "key_ingredients": ["Water"],
    "benefits": ["Hydration"],
    "how_to_use": "Apply daily",
    "side_effects": "None",
    "price": "100"
}

@pytest.mark.skipif(not os.environ.get("GROQ_API_KEY"), reason="Requires API Key")
def test_agent_connectivity():
    """
    E2E Integration Test: 
    Runs the 'Generate Questions' node for real to verify LLM connectivity.
    """
    # 1. Prepare State
    product = ProductData(**SAMPLE_DATA)
    state = {"product_data": product.model_dump_json()}
    
    # 2. Run the Node (Real LLM Call)
    result = AgentFactory.generate_questions_node(state)
    
    # 3. Verify Output
    assert "questions" in result
    assert isinstance(result["questions"], list)
    assert len(result["questions"]) > 0
    print(f"✅ E2E Connectivity Test Passed: Generated {len(result['questions'])} questions.")
