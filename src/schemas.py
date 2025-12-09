from pydantic import BaseModel, Field
from typing import List, Dict, Optional

# --- 1. THE INPUT MODEL (GlowBoost) ---
class ProductData(BaseModel):
    name: str
    concentration: str
    skin_type: str
    key_ingredients: List[str]
    benefits: List[str]
    how_to_use: str
    side_effects: str
    price: str

# --- 2. OUTPUT MODELS ---

class FAQItem(BaseModel):
    question: str
    answer: str
    category: str

class FAQPage(BaseModel):
    page_title: str = "Frequently Asked Questions"
    faqs: List[FAQItem]

class ProductPage(BaseModel):
    title: str
    headline: str
    features_section: List[str]
    usage_guide: str
    safety_warning: str
    seo_tags: List[str]

class ComparisonItem(BaseModel):
    feature: str
    our_product: str
    competitor_product: str

class ComparisonPage(BaseModel):
    title: str
    competitor_name: str
    comparison_table: List[ComparisonItem]
    verdict: str