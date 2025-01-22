import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from io import BytesIO

from dotenv import load_dotenv
load_dotenv()

# Initialize session state
if 'nutrichat_initialized' not in st.session_state:
    st.session_state.nutrichat_initialized = False
    st.session_state.vectorstore = None
    st.session_state.retriever = None
    st.session_state.llm = None
    st.session_state.chat_history = []

def initialize_nutrichat():
    with st.spinner("Initializing NutriChat..."):
        pdf_paths = [
            "/Users/abhijithutla/projects/AIMD_nutritionguard/docs/mealprep.pdf",
            "/Users/abhijithutla/projects/AIMD_nutritionguard/docs/NutritionGuide.pdf",
            "/Users/abhijithutla/projects/AIMD_nutritionguard/docs/Whole-Foods-A-to-Z.pdf"
        ]
        data = []
        for pdf_path in pdf_paths:
            loader = PyPDFLoader(pdf_path)
            current_data = loader.load()
            data.extend(current_data)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
        docs = text_splitter.split_documents(data)

        st.session_state.vectorstore = Chroma.from_documents(documents=docs, embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001"))
        st.session_state.retriever = st.session_state.vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 10})
        st.session_state.llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0, max_tokens=None, timeout=None)
        st.session_state.nutrichat_initialized = True

def nutri_chat_setup():
    st.title("🥗 NutriChat: Your Personal Nutrition Assistant", anchor=False)

    

    # Clear Chat Button
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    query = st.chat_input("Describe your nutrition concerns or ask a question")

    if query:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": query})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(query)

        with st.spinner("Generating response..."):
            system_prompt = (
                "You are a Nutrition assistant for the question answering task. "
                "Use the following pieces of retrieved context to answer "
                "the question. If you don't know the answer, say that you "
                "don't know. Use concise and informative language."
                "\n\n"
                "{context}"
            )

            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", "{input}"),
            ])

            question_answer_chain = create_stuff_documents_chain(st.session_state.llm, prompt)
            rag_chain = create_retrieval_chain(st.session_state.retriever, question_answer_chain)

            response = rag_chain.invoke({"input": query})
            
            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(response["answer"])
            
            # Add assistant response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": response["answer"]})

        # Rerun the app to update the chat history display
        st.rerun()

if __name__ == "__main__":
    nutri_chat_setup()
