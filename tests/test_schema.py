import pytest
from src.schemas import ProductData, FAQPage, FAQItem

def test_product_data_validation():
    """Test that input data is validated correctly."""
    valid_data = {
        "name": "Test Serum",
        "concentration": "5%",
        "skin_type": "All",
        "key_ingredients": ["Water"],
        "benefits": ["Hydration"],
        "how_to_use": "Apply daily",
        "side_effects": "None",
        "price": "100"
    }
    product = ProductData(**valid_data)
    assert product.name == "Test Serum"

def test_faq_structure():
    """Test output schema integrity."""
    faq = FAQItem(question="Q?", answer="A.", category="Test")
    page = FAQPage(faqs=[faq])
    assert len(page.faqs) == 1
    assert page.faqs[0].question == "Q?"