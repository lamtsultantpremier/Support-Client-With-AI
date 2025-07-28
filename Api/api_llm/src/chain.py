from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser,JsonOutputParser
import configs
from src.prompts import RESPONSE_TEMPLATE , CLASSIFICATION_TEMPLATE
model = ChatOpenAI(model = "gpt-4o" , api_key = configs.OPENAI_API_KEY , temperature = 0.3)

def create_response_chain():
    return RESPONSE_TEMPLATE|model|StrOutputParser()

def create_classification_chain():
    return CLASSIFICATION_TEMPLATE|model|JsonOutputParser()