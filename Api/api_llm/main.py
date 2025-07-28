from fastapi import FastAPI,Depends,Body
from src.chain import create_response_chain,create_classification_chain
from langchain_core.runnables import RunnableParallel
from pydantic import ConfigDict
from typing import Annotated,List
from src.schema import Message,ChatRequest,MessageBase
app = FastAPI()

@app.post("/chats")
def give_response(input : Annotated[str,Body()],messages:Annotated[list[dict],Body()]):
    classification_chain = create_classification_chain()
    response_chain = create_response_chain()

    chain = RunnableParallel(chatbot_response = response_chain,classification = classification_chain)
    return chain.invoke({"input":input,"history":messages})




