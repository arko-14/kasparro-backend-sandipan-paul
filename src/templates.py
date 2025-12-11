from langchain_core.prompts import ChatPromptTemplate

# Optimized: Asks for a simple list, no categories, to save tokens/complexity
QUESTION_GEN_TEMPLATE = ChatPromptTemplate.from_template(
    """
    Analyze this product: {product_json}
    Generate exactly 15 distinct user questions about it.
    Return the output as a pure JSON list of strings.
    Example: ["Question 1?", "Question 2?"]
    """
)

FAQ_ANSWER_TEMPLATE = ChatPromptTemplate.from_template(
    """
    Product: {product_json}
    Question: {question}
    Answer the question concisely based on the product data.
    """
)

PRODUCT_PAGE_TEMPLATE = ChatPromptTemplate.from_template(
    """
    Create a Product Page for: {product_json}
    Structure: Headline, Benefits, Usage, Safety.
    
    IMPORTANT: Return ONLY valid JSON matching the instructions.
    {format_instructions}
    """
)

COMPETITOR_GEN_TEMPLATE = ChatPromptTemplate.from_template(
    """
    Create a fictional competitor to {product_name}.
    Return Name, Price, Ingredients.
    """
)

COMPARISON_TEMPLATE = ChatPromptTemplate.from_template(
    """
    Compare Product A: {product_json}
    vs Product B: {competitor_json}
    
    IMPORTANT: Return ONLY valid JSON matching the instructions.
    {format_instructions}
    """
)
