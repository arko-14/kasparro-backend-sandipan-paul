import logging
from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from src.schemas import ProductData, FAQPage, ProductPage, ComparisonPage
from src.agents import AgentFactory

# Configure Logger
logger = logging.getLogger(__name__)

# --- 1. DEFINE GRAPH STATE ---
class GraphState(TypedDict):
    product_data: str
    questions: Optional[List[str]]
    faq_page: Optional[FAQPage]
    product_page: Optional[ProductPage]
    comparison_page: Optional[ComparisonPage]

# --- 2. INPUT DATA ---
RAW_DATA = {
    "name": "GlowBoost Vitamin C Serum",
    "concentration": "10% Vitamin C",
    "skin_type": "Oily, Combination",
    "key_ingredients": ["Vitamin C", "Hyaluronic Acid"],
    "benefits": ["Brightening", "Fades dark spots"],
    "how_to_use": "Apply 2–3 drops in the morning before sunscreen",
    "side_effects": "Mild tingling for sensitive skin",
    "price": "₹699"
}

def save_json_artifact(filename, data):
    """Reusable helper with error handling."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(data.model_dump_json(indent=2))
        logger.info(f"Artifact saved: {filename}")
    except Exception as e:
        logger.error(f"Failed to save {filename}: {e}")

def main():
    logger.info("🚀 STARTING KASPARRO AUTOMATION GRAPH")

    # 1. Initialize State
    try:
        product = ProductData(**RAW_DATA)
        initial_state = {
            "product_data": product.model_dump_json(),
            "questions": [],
            "faq_page": None,
            "product_page": None,
            "comparison_page": None
        }
    except Exception as e:
        logger.critical(f"Data Ingestion Failed: {e}")
        return

    # 2. Build Graph
    workflow = StateGraph(GraphState)

    workflow.add_node("generate_questions", AgentFactory.generate_questions_node)
    workflow.add_node("answer_faqs", AgentFactory.answer_faq_node)
    workflow.add_node("generate_product_page", AgentFactory.product_page_node)
    workflow.add_node("generate_comparison", AgentFactory.comparison_node)

    # Define Flow
    workflow.set_entry_point("generate_questions")
    workflow.add_edge("generate_questions", "answer_faqs")
    workflow.add_edge("answer_faqs", "generate_product_page")
    workflow.add_edge("generate_product_page", "generate_comparison")
    workflow.add_edge("generate_comparison", END)

    # 3. Compile & Run
    app = workflow.compile()
    
    try:
        final_state = app.invoke(initial_state)
    except Exception as e:
        logger.critical(f"Graph Execution Failed: {e}")
        return

    # 4. Save Outputs
    if final_state.get("faq_page"):
        save_json_artifact("faq.json", final_state["faq_page"])
    
    if final_state.get("product_page"):
        save_json_artifact("product_page.json", final_state["product_page"])
        
    if final_state.get("comparison_page"):
        save_json_artifact("comparison_page.json", final_state["comparison_page"])

    logger.info("🏁 PIPELINE COMPLETE")

if __name__ == "__main__":
    main()
