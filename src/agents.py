import json
import logging
from langchain_groq import ChatGroq
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser, JsonOutputParser
from .config import Config
from .schemas import ProductData, FAQPage, ProductPage, ComparisonPage, FAQItem
from .templates import (
    QUESTION_GEN_TEMPLATE, FAQ_ANSWER_TEMPLATE, 
    PRODUCT_PAGE_TEMPLATE, COMPETITOR_GEN_TEMPLATE, COMPARISON_TEMPLATE
)

logger = logging.getLogger(__name__)

llm = ChatGroq(
    groq_api_key=Config.GROQ_API_KEY, 
    model_name=Config.MODEL_NAME,
    temperature=0.1
)

class AgentFactory:
    
    @staticmethod
    def generate_questions_node(state):
        """Node 1: Generates questions using JSON parsing."""
        logger.info("Generating user questions...")
        try:
            # Robust JSON parsing
            chain = QUESTION_GEN_TEMPLATE | llm | JsonOutputParser()
            questions = chain.invoke({"product_json": state["product_data"]})
            
            # Validation: Ensure we have a list
            if not isinstance(questions, list):
                logger.warning("LLM returned non-list, attempting to wrap.")
                questions = [str(questions)]
            
            
            if len(questions) < 5:
                logger.warning(f"Only generated {len(questions)} questions. Retrying might be needed in prod.")

            return {"questions": questions}
        except Exception as e:
            logger.error(f"Failed to generate questions: {e}")
            raise e

    @staticmethod
    def answer_faq_node(state):
        """Node 2: Answers questions using BATCH processing."""
        questions = state["questions"]
        product_json = state["product_data"]
        logger.info(f"Answering {len(questions)} questions in batch...")
        
        try:
            chain = FAQ_ANSWER_TEMPLATE | llm | StrOutputParser()
            
            # Batch calls the API in parallel/async
            inputs = [{"product_json": product_json, "question": q} for q in questions]
            answers = chain.batch(inputs)
            
            faqs = [
                FAQItem(question=q, answer=a, category="General") 
                for q, a in zip(questions, answers)
            ]
            return {"faq_page": FAQPage(faqs=faqs)}
        except Exception as e:
            logger.error(f"Failed to batch answer FAQs: {e}")
            raise e

    @staticmethod
    def product_page_node(state):
        """Node 3: Generates Product Page."""
        logger.info("Drafting product page...")
        try:
            parser = PydanticOutputParser(pydantic_object=ProductPage)
            chain = PRODUCT_PAGE_TEMPLATE.partial(format_instructions=parser.get_format_instructions()) | llm | parser
            result = chain.invoke({"product_json": state["product_data"]})
            return {"product_page": result}
        except Exception as e:
            logger.error(f"Failed to generate product page: {e}")
            raise e

    @staticmethod
    def comparison_node(state):
        """Node 4: Generates Comparison."""
        logger.info("Analyzing competition...")
        try:
            product_name = json.loads(state["product_data"])["name"]
            
            # Sub-step 1: Create Competitor
            comp_chain = COMPETITOR_GEN_TEMPLATE | llm | StrOutputParser()
            competitor_data = comp_chain.invoke({"product_name": product_name})
            
            # Sub-step 2: Matrix
            parser = PydanticOutputParser(pydantic_object=ComparisonPage)
            compare_chain = COMPARISON_TEMPLATE.partial(format_instructions=parser.get_format_instructions()) | llm | parser
            
            result = compare_chain.invoke({
                "product_json": state["product_data"],
                "competitor_json": competitor_data
            })
            return {"comparison_page": result}
        except Exception as e:
            logger.error(f"Failed comparison generation: {e}")
            raise e
