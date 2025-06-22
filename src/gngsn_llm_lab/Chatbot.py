import chromadb
import ollama
import streamlit as st
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms.ollama import Ollama
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore

st.title("💬 Chatbot")
st.caption("🚀 Chatbot powered by OpenAI")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# vector_store = Chroma(
#     collection_name="docs",
#     embedding_function=OpenAIEmbeddings(),
# )
# vectorstore = Chroma.from_documents([uploaded_file], embeddings)


client = chromadb.Client()
collection = client.get_or_create_collection(name="docs")
embeddings = OllamaEmbeddings(model="llama3")

with st.sidebar:
    uploaded_file = st.file_uploader("Choose a file")
    print(uploaded_file)

    if uploaded_file is not None:
        st.write("You selected the file:", uploaded_file.name)

        file_string = uploaded_file.read()
        print(file_string)

        document = Document(page_content="i will be deleted :(")
        documents = [document]

        text = """내 이름은 박경선이야
                나는 98년생이야
                나는 8월 12일에 태어났어
                나는 샐러드를 좋아해
                나는 운동을 좋아해"""

        for i, d in enumerate(documents):
            response = ollama.embed(model="llama3", input=[text])
            vectorstore = InMemoryVectorStore.from_texts(
                [text],
                embedding=embeddings,
            )
            retriever = vectorstore.as_retriever()
            #
            # collection.add(
            #     ids=[str(i)],
            #     embeddings=embeddings,
            #     documents=[d]
            # )

llm = Ollama(model='gemma3:latest')
# qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # response = llm.invoke(st.session_state.messages) # 'where is Seoul?'

    # for msg in response:
    #     print(msg, flush=True, end="")

    retrieved_documents = retriever.invoke(prompt)
    results = collection.query(
        query_embeddings=[embeddings],
        n_results=1
    )
    data = results['documents'][0][0]

    output = ollama.generate(
        model="llama2",
        prompt=f"Using this data: {data}. Respond to this prompt: {input}"
    )

    # print(output['response'])
    response = output['response']

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
