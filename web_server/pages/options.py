import streamlit as st
from data import Options
from page_util import hide_navigation_in_iframe
from storage.dbo import store_options, fetch_options

st.set_page_config(
        page_title="LLM Settings",
        page_icon="🛠️",
        initial_sidebar_state="collapsed"
)
hide_navigation_in_iframe(st._get_query_params())


def switch_page(page_name: str):
    pages = st.source_util.get_pages("main.py")

    for page_hash, config in pages.items():
        if config["page_name"] == page_name:
            raise st._RerunException(
                    st._RerunData(
                            page_script_hash=page_hash,
                            page_name=page_name,
                    )
            )
    page_names = [config["page_name"] for config in pages.values()]
    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")


GOOGLE_MODELS = ("code-bison", "gemini-pro")
OPENAI_MODELS = ("gpt-4", "gpt-3.5-turbo")
COHERE_MODELS = ("command-light", "command")

st.sidebar.header("🛠LLM Options")
st.header('🛠 LLM Settings')
options = fetch_options()
google_model = st.selectbox(
    "🐶 Select Google Model:",
    GOOGLE_MODELS,
    GOOGLE_MODELS.index(options.google_model)
)
openai_model = st.selectbox(
    "🐱 Select OpenAI Model:",
    OPENAI_MODELS,
    OPENAI_MODELS.index(options.openai_model)
)
cohere_model = st.selectbox(
    "🐻 Select Cohere Model:",
    COHERE_MODELS,
    COHERE_MODELS.index(options.cohere_model)
)
temperature = st.slider('Temperature', 0.0, 1.0, options.temperature)
token_limit = st.slider('Token limit', 0, 2048, options.token_limit)
top_k = st.slider('Top-K', 0, 40, options.top_k)
top_p = st.slider('Top-P', 0.0, 1.0, options.top_p)

col1, col2 = st.columns(2)
with col1:
    if st.button('Reset'):
        options = Options()
        store_options(options)
        st.success('Reset options successfully!', icon="✅")
        st.rerun()
with col2:
    if st.button('Apply'):
        options = Options(
            google_model, openai_model, cohere_model, temperature, token_limit, top_k, top_p)
        store_options(options)
        st.success('Options saved successfully!', icon="✅")
