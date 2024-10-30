# from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama


llm = ChatOllama(model="llama3.2:1b", temperature=0)
response = llm.invoke("what is the color blue?")
print(response.content)