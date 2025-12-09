from langchain_core.prompts import ChatPromptTemplate

# Template 1: Generate User Questions
QUESTION_GEN_TEMPLATE = ChatPromptTemplate.from_template(
    """
    You are a customer insights agent. Analyze this product:
    {product_json}
    
    Generate exactly 15 distinct user questions categorized into: 
    Informational, Safety, Usage, Purchase, Comparison.
    Return just the questions one per line.
    """
)

# Template 2: FAQ Answer Generator
FAQ_ANSWER_TEMPLATE = ChatPromptTemplate.from_template(
    """
    You are a customer support agent. Answer the following question based strictly on the product data.
    Product: {product_json}
    Question: {question}
    
    Keep answers concise and helpful.
    """
)

# Template 3: Product Page Generator (FIXED)
PRODUCT_PAGE_TEMPLATE = ChatPromptTemplate.from_template(
    """
    You are a marketing expert. Create a high-converting Product Page for:
    {product_json}
    
    Use the following strict structure:
    - Catchy Headline
    - Key Benefits List (persuasive copy)
    - Clear Usage Instructions
    - Safety Note
    
    IMPORTANT: Return ONLY valid JSON.
    {format_instructions}
    """
)

# Template 4: Competitor Generation
COMPETITOR_GEN_TEMPLATE = ChatPromptTemplate.from_template(
    """
    Create a fictional competitor product to compare against {product_name}.
    It should be slightly inferior or different (e.g., lower concentration or higher price).
    Provide: Name, Price, Key Ingredients.
    """
)

# Template 5: Comparison Logic (FIXED)
COMPARISON_TEMPLATE = ChatPromptTemplate.from_template(
    """
    Compare these two products row-by-row:
    Product A (Ours): {product_json}
    Product B (Competitor): {competitor_json}
    
    Focus on: Price, Ingredients, Benefits, Suitability.
    
    IMPORTANT: Return ONLY valid JSON.
    {format_instructions}
    """
)