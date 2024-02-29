import streamlit as st
import pickle
from PyPDF2 import PdfReader
from langchain_community.llms import OpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.callbacks import get_openai_callback
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

os.environ['OPENAI_API_KEY'] = 'sk-0inHBLDz71CfBIINuQ6969ST3BlbkFJq4IyrIojmLiC9SHcRb0v'# obiously its incorrect

def main():
    st.header('Chat with PDF')
    st.sidebar.title('LLM ChatApp')
    st.sidebar.markdown('''
    This is an LLM powered chatbot , you can upload your pdf and ask related questions.
    ''')
    # Upload a PDF File
    pdf = st.file_uploader("Upload your PDF File", type='pdf')

    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text=""
        for page in pdf_reader.pages:
            text+=page.extract_text()
        #st.write(text)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len

        )
        chunks = text_splitter.split_text(text=text)
        #st.write(chunks[0])
        store_name = pdf.name[:-4]
        st.write(store_name)
        if os.path.exists(f"{store_name}"):
            VectorStore = FAISS.load_local(f"{store_name}", OpenAIEmbeddings())
            st.write('Embeddings Loaded from the Disk')
        else:
            embeddings = OpenAIEmbeddings()
            VectorStore = FAISS.from_texts(chunks, embeddings)
            VectorStore.save_local(f"{store_name}")
            st.write('Embeddings Created')
        query = st.text_input("Ask Question from your PDF File")
        if query:
            docs = VectorStore.similarity_search(query=query, k=3)
            llm = OpenAI()
            chain = load_qa_chain(llm = llm, chain_type='stuff')
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=query)
                print(cb)
            st.write(response)




if __name__ == '__main__':
    main()