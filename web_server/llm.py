import os
from enum import Enum

import chromadb as chromadb
from langchain.chat_models import ChatOpenAI, ChatCohere
from langchain.llms import VertexAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, VertexAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import AsyncHtmlLoader
from langchain.document_transformers import Html2TextTransformer


from data import Options

os.environ["OPENAI_API_KEY"] = 'your_openai_api_key_here'
os.environ["COHERE_API_KEY"] = 'your_cohere_api_key_here'


class LlmProvider(Enum):
    GOOGLE = 1
    OPENAI = 2
    COHERE = 3


def get_memory_key(llm_provider: LlmProvider):
    return "chat_history_" + llm_provider.name


def create_llm(llm_provider: LlmProvider, options: Options):
    match llm_provider:
        case LlmProvider.OPENAI:
            return ChatOpenAI(model_name=options.openai_model,
                              temperature=options.temperature,
                              max_tokens=options.token_limit,
                              model_kwargs={
                                  "top_p": options.top_p
                              })
        case LlmProvider.COHERE:
            return ChatCohere(model=options.cohere_model,
                          temperature=options.temperature,
                          max_tokens=options.token_limit,
                          top_p=options.top_p,
                          top_k=options.top_k)
        case _:
            return VertexAI(model_name=options.google_model,
                            max_output_tokens=options.token_limit,
                            top_p=options.top_p,
                            top_k=options.top_k)


def init_llm(llm_provider: LlmProvider, options: Options, template, input_variables):
    llm = create_llm(llm_provider, options)
    prompt_llm = PromptTemplate(template=template, input_variables=input_variables)
    # memory_key=get_memory_key(llm_provider)
    # memory = ConversationBufferMemory(memory_key="chat_history")

    llm_chain = LLMChain(
        prompt=prompt_llm,
        llm=llm,
        # memory=memory,
        verbose=True
    )
    return llm_chain


def load_htmls(urls):
    loader = AsyncHtmlLoader(urls)
    documents = loader.load()
    # Split documents into chunks
    html2text = Html2TextTransformer()
    docs_transformed = html2text.transform_documents(documents)
    chunk_size = 4096
    docs_new = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
    )

    for doc in docs_transformed:
        if len(doc.page_content) < chunk_size:
            docs_new.append(doc)
        else:
            docs = text_splitter.create_documents([doc.page_content])
            docs_new.extend(docs)
    return docs_new


def init_doc_embeddings_google(docs):
    try:
        # Create vectorstore from documents for LLMs
        store_google = Chroma.from_documents(
            docs, VertexAIEmbeddings(model_name='textembedding-gecko@001'))
    except chromadb.errors.InvalidDimensionException:
        Chroma().delete_collection()
        store_google = Chroma.from_documents(
            docs, VertexAIEmbeddings(model_name='textembedding-gecko@001'))
    retriever_google = store_google.as_retriever()
    return retriever_google


def init_doc_embeddings_openai(docs):
    try:
        # Create vectorstore from documents for LLMs
        store_openai = Chroma.from_documents(docs, OpenAIEmbeddings())
    except chromadb.errors.InvalidDimensionException:
        Chroma().delete_collection()
        store_openai = Chroma.from_documents(docs, OpenAIEmbeddings())
    retriever_openai = store_openai.as_retriever()
    return retriever_openai


def ask_doc(llm, retriever, query):
    # Create QA chain
    qa = RetrievalQA.from_chain_type(
        llm=llm, chain_type='stuff', retriever=retriever)
    resp = qa.run(query)
    return resp


def local_test():
    llm_google = VertexAI(model_name='code-bison')
    llm_openai = ChatOpenAI(model_name='gpt-3.5-turbo')
    urls = ['https://developers.google.com/identity/gsi/web/guides/integrate']
    docs = load_htmls(urls)


    queries = ["Is One Tap and Sign in with Google button available in webviews?",
             "Can I use my own Sign in with Google button?"]
    for query in queries:
        print('*' * 50)
        print('Question: ' + query)
        retriever_google = init_doc_embeddings_google(docs)
        resp = ask_doc(llm_google, retriever_google, query)
        print('\n\nGoogle Answer: ' + resp)

        retriever_openai = init_doc_embeddings_openai(docs)
        resp = ask_doc(llm_openai, retriever_openai, query)
        print('\n\nOpenAI Answer: ' + resp)


if __name__ == '__main__':
    local_test()
