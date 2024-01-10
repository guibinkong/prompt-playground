import streamlit as st


def hide_navigation_in_iframe(params):
    if params and ('iframed' in params) and (params.get('iframed')[0] == "1"):
        hide_streamlit_style = """
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            [data-testid="stSidebar"] {
               display: none;
            }
            [data-testid="collapsedControl"] {
               display: none;
            }
        </style>
        
        """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)
