### 🤖 Create a Simple Chatbot
import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA

from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from dotenv import load_dotenv


def get_working_dir():
    working_dir = "gngsn-llm-lab"
    root = []
    for p in os.getcwd().split("/"):
        root.append(p)
        if p == working_dir:
            break
    return "/".join(root)


load_dotenv()
root_dir = get_working_dir()

loader = PyPDFLoader(root_dir + "/data/오가노이드사이언스_증권신고서.pdf")
documents = loader.load()

chat = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
vectorstore = Chroma.from_documents(
    documents, GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
)
retriever = vectorstore.as_retriever()
qa = RetrievalQA.from_chain_type(llm=chat, retriever=retriever)


while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    response = qa.run(user_input)

    print("Bot:", response)
