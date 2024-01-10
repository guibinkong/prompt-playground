import streamlit as st
from langchain.llms import VertexAI
from langchain.chat_models import ChatOpenAI

from page_util import hide_navigation_in_iframe
from storage.dbo import fetch_options, fetch_retrieval, fetch_template, list_retrievals, list_templates
import llm
from data_formatter import format_retrieval, format_template

st.set_page_config(
        page_title="Prompt Playground",
        page_icon="💬",
        initial_sidebar_state="collapsed"
)
hide_navigation_in_iframe(st._get_query_params())


@st.cache_resource(show_spinner=False)
def init_llms(tmpl, input_vars):
    options = fetch_options()
    llm1 = llm.init_llm(llm.LlmProvider.GOOGLE, options, tmpl, input_vars)
    llm2 = llm.init_llm(llm.LlmProvider.OPENAI, options, tmpl, input_vars)
    llm3 = llm.init_llm(llm.LlmProvider.COHERE, options, tmpl, input_vars)
    return llm1, llm2, llm3


st.title('💬 Prompt Playground')
st.sidebar.header("💬 Playground")

retrievals = [''] + list(list_retrievals())
r_name = st.selectbox("🔗 Select Retrieval:", retrievals)
if r_name:
    retrieval = fetch_retrieval(r_name)
    st.text(format_retrieval(retrieval))
input_variables = ['input']
templates = [''] + list(list_templates())
tmpl_name = st.selectbox("🔗 Select Template:", templates)
if tmpl_name:
    template = format_template(fetch_template(tmpl_name))
    st.text(template)
else:
    template = 'User: {input}\n\nAI:\n'

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)

    if not r_name:
        llm_google, llm_openai, llm_cohere = init_llms(template, input_variables)
        msg_google = llm_google.predict(input=prompt)
        st.chat_message("Google", avatar="🐶").write(msg_google)

        msg_openai = llm_openai.predict(input=prompt)
        st.chat_message("OpenAI", avatar="🐱").write(msg_openai)

        msg_cohere = llm_cohere.predict(input=prompt)
        st.chat_message("Cohere", avatar="🐻").write(msg_cohere)
    else:
        # Retrieval Augmented Generation
        query = template.replace('{input}', prompt)
        docs = llm.load_htmls(retrieval.urls)

        llm_google = VertexAI(model_name='code-bison')
        retriever_google = llm.init_doc_embeddings_google(docs)
        resp_google = llm.ask_doc(llm_google, retriever_google, query)
        st.chat_message("Google", avatar="🐶").write(resp_google)

        llm_openai = ChatOpenAI(model_name='gpt-3.5-turbo')
        retriever_openai = llm.init_doc_embeddings_openai(docs)
        resp_openai = llm.ask_doc(llm_openai, retriever_openai, query)
        st.chat_message("OpenAI", avatar="🐱").write(resp_openai)
