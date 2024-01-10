import streamlit as st
from data import Example, TemplateInstance
from page_util import hide_navigation_in_iframe
from storage.dbo import add_template, delete_template, fetch_template, list_templates
from data_formatter import format_template

st.set_page_config(
    page_title="Template Editor",
    page_icon="🛠️",
    initial_sidebar_state="collapsed"
)
hide_navigation_in_iframe(st._get_query_params())

st.sidebar.header("🛠Templates")
st.header('🛠 Add Template')

name = st.text_input('Name', label_visibility='hidden',
                     placeholder='Set an unique template name here ...')
instruction = st.text_input('Instruction', label_visibility='hidden',
                            placeholder='Give your instruction here ...')
context = st.text_area("Context", "", height=100, max_chars=800, label_visibility='hidden',
                       placeholder='Give the problem context here ...')
input1 = st.text_input('Input_1', label_visibility='hidden',
                       placeholder='The input of the first example ...')
output1 = st.text_area('Output_1', height=100, max_chars=500, label_visibility='hidden',
                       placeholder='The output of the first example ...')
input2 = st.text_input('Input_2', label_visibility='hidden',
                       placeholder='The input of the second example ...')
output2 = st.text_area('Output_2', height=100, max_chars=500, label_visibility='hidden',
                       placeholder='The output of the second example ...')
col1, col2 = st.columns(2)
with col1:
    if st.button('Reset'):
        st.rerun()
with col2:
    if st.button('Add'):
        examples = []
        if input1 and output1:
            examples.append(Example(input1, output1))
        if input2 and output2:
            examples.append(Example(input2, output2))
        template = TemplateInstance(name, instruction, context, examples)
        try:
            add_template(template)
            st.success('Template saved successfully!', icon="✅")
            st.rerun()
        except Exception as exception:
            st.exception(exception)

st.divider()
st.header('Template List')
templates = list_templates()
for tmpl_name in templates:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader(tmpl_name + ':')
    with c2:
        if st.button('Delete', key='delete_' + tmpl_name):
            delete_template(tmpl_name)
            st.rerun()
    tmpl = fetch_template(tmpl_name)
    st.text(format_template(tmpl))
