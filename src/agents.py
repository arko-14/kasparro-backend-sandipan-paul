import json
from langchain_groq import ChatGroq
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from .config import Config
from .schemas import ProductData, FAQPage, ProductPage, ComparisonPage, FAQItem
from .templates import (
    QUESTION_GEN_TEMPLATE, FAQ_ANSWER_TEMPLATE, 
    PRODUCT_PAGE_TEMPLATE, COMPETITOR_GEN_TEMPLATE, COMPARISON_TEMPLATE
)

# Initialize LLM
llm = ChatGroq(
    groq_api_key=Config.GROQ_API_KEY, 
    model_name=Config.MODEL_NAME,
    temperature=0.1  # LOWER temperature to be more precise/strict
)

class AgentOrchestrator:
    
    @staticmethod
    def generate_faqs(product: ProductData) -> FAQPage:
        """Agent 1: Generates questions, then answers them."""
        print("   -> [Agent: Insight] Generating questions...")
        q_chain = QUESTION_GEN_TEMPLATE | llm | StrOutputParser()
        questions_raw = q_chain.invoke({"product_json": product.model_dump_json()})
        
        # Robust splitting
        questions = [q.strip() for q in questions_raw.split('\n') if '?' in q][:5]
        
        print(f"   -> [Agent: Support] Answering {len(questions)} questions...")
        faqs = []
        for q in questions:
            a_chain = FAQ_ANSWER_TEMPLATE | llm | StrOutputParser()
            ans = a_chain.invoke({"product_json": product.model_dump_json(), "question": q})
            faqs.append(FAQItem(question=q, answer=ans, category="General"))
            
        return FAQPage(faqs=faqs)

    @staticmethod
    def generate_product_page(product: ProductData) -> ProductPage:
        """Agent 2: Transforms raw data into a marketing landing page."""
        print("   -> [Agent: Marketing] Drafting product page...")
        parser = PydanticOutputParser(pydantic_object=ProductPage)
        
        # --- FIX: Injecting format instructions here ---
        chain = PRODUCT_PAGE_TEMPLATE.partial(
            format_instructions=parser.get_format_instructions()
        ) | llm | parser
        
        return chain.invoke({"product_json": product.model_dump_json()})

    @staticmethod
    def generate_comparison(product: ProductData) -> ComparisonPage:
        """Agent 3: Invents a competitor and generates a comparison matrix."""
        print("   -> [Agent: Competitor Analyst] Creating fictional competitor...")
        
        comp_chain = COMPETITOR_GEN_TEMPLATE | llm | StrOutputParser()
        competitor_data = comp_chain.invoke({"product_name": product.name})
        
        print("   -> [Agent: Strategist] Building comparison matrix...")
        parser = PydanticOutputParser(pydantic_object=ComparisonPage)
        
        # --- FIX: Injecting format instructions here ---
        compare_chain = COMPARISON_TEMPLATE.partial(
            format_instructions=parser.get_format_instructions()
        ) | llm | parser
        
        return compare_chain.invoke({
            "product_json": product.model_dump_json(),
            "competitor_json": competitor_data
        })