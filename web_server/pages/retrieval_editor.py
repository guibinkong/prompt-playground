import streamlit as st
from data import RetrievalConfig
from data_formatter import format_retrieval
from page_util import hide_navigation_in_iframe
from storage.dbo import add_retrieval, delete_retrieval, fetch_retrieval, list_retrievals

st.set_page_config(
    page_title="Retrieval Configurator",
    page_icon="🛠️",
    initial_sidebar_state="collapsed"
)
hide_navigation_in_iframe(st._get_query_params())

st.sidebar.header("🛠Retrievals")
st.header('🛠 Retrieval Configurator')

name = st.text_input('Name', label_visibility='hidden',
                     placeholder='Set an unique retrieval name here ...')
url1 = st.text_input('url_1', label_visibility='hidden',
                       placeholder='The URL of the first doc ...')
url2 = st.text_input('url_2', label_visibility='hidden',
                     placeholder='The URL of the second doc ...')
url3 = st.text_input('url_3', label_visibility='hidden',
                     placeholder='The URL of the third doc ...')
col1, col2 = st.columns(2)
with col1:
    if st.button('Reset'):
        st.rerun()
with col2:
    if st.button('Add'):
        if name and (url1 or url2 or url3):
            urls = []
            if url1:
                urls.append(url1)
            if url2:
                urls.append(url2)
            if url3:
                urls.append(url3)
            retrieval = RetrievalConfig(name, urls)
            try:
                add_retrieval(retrieval)
                st.success('Retrieval configuration saved successfully!', icon="✅")
                st.rerun()
            except Exception as exception:
                st.exception(exception)

st.divider()
st.header('Retrieval Configuration List')
retrievals = list_retrievals()
for retrieval_name in retrievals:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader(retrieval_name + ':')
    with c2:
        if st.button('Delete', key='delete_' + retrieval_name):
            delete_retrieval(retrieval_name)
            st.rerun()
    retrieval = fetch_retrieval(retrieval_name)
    st.text(format_retrieval(retrieval))
