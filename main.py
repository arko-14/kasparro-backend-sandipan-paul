import json
import os
from src.schemas import ProductData
from src.agents import AgentOrchestrator

# --- 1. THE INPUT DATA (Hardcoded as per requirements) ---
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

def main():
    print("AUTOMATION SYSTEM STARTING...\n")

    # 1. Ingest Data
    product = ProductData(**RAW_DATA)
    print(f"✅ Data Ingested: {product.name}")

    # 2. Run Workflow Graph
    # Node A: FAQ Agent
    print("\n--- NODE 1: FAQ GENERATION ---")
    faq_page = AgentOrchestrator.generate_faqs(product)
    
    # FIX IS HERE: Added encoding="utf-8"
    with open("faq.json", "w", encoding="utf-8") as f:
        f.write(faq_page.model_dump_json(indent=2))
    print("✅ output saved: faq.json")

    # Node B: Product Page Agent
    print("\n--- NODE 2: PRODUCT PAGE GENERATION ---")
    prod_page = AgentOrchestrator.generate_product_page(product)
    
    # FIX IS HERE: Added encoding="utf-8"
    with open("product_page.json", "w", encoding="utf-8") as f:
        f.write(prod_page.model_dump_json(indent=2))
    print("✅ output saved: product_page.json")

    # Node C: Comparison Agent
    print("\n--- NODE 3: COMPARISON GENERATION ---")
    comp_page = AgentOrchestrator.generate_comparison(product)
    
    # FIX IS HERE: Added encoding="utf-8"
    with open("comparison_page.json", "w", encoding="utf-8") as f:
        f.write(comp_page.model_dump_json(indent=2))
    print("✅ output saved: comparison_page.json")

    

if __name__ == "__main__":
    main()    