#importing the necessary libraries and modules for the application
import streamlit as st
import os
import pandas as pd
import requests
import aisuite as ai
import sqlite3
import json
from Agentic_AI_functions_file import Agentic_AI_orchestrator

#loads sections of the secrets.toml file into environment variables for secure access to API keys and database paths
db_path = st.secrets["connections"]["sales_database"]["path"]
os.environ["WEATHER_API_KEY"] = st.secrets["WEATHER_API_KEY"]
client = ai.Client() #instantiating the AI client to interact with the AI suite

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["WEATHER_API_KEY"] = st.secrets["WEATHER_API_KEY"]

# configures the app page 
st.set_page_config(page_title="Agentic Assistant", page_icon="🤖", layout="centered")
theme_selection= st.sidebar.selectbox("Select Theme", options=sorted(["Aquamarine","Lightgreen","Lightblue","Dark","Maroon","Gray"]),index=1,help="Choose a theme for the app", key="Theme_selector")

# styles the app to the user preferences.
st.markdown(f"""
            <style>
    [data-testid="stSidebar"] .stButton>button {{
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
        border: 2px solid white;
        font-weight: bold;
    }}
        
    [data-testid="stSidebarCollapseButton"] svg {{
        fill: Black !important; 
        color: Black !important;
    }}

    [data-testid="stSidebarCollapseButton"]:hover svg {{
        fill: yellow !important;
        color: yellow !important;
    }}

    [data-testid="stSidebar"] .stButton>button:hover {{
        background-color: white;
        color: #4CAF50;
        border: 2px solid #4CAF50;
    }}
    [data-testid="stAppViewContainer"]  {{ background-color: {theme_selection.lower()}; }}
    [data-testid="stHeader"] {{ background-color: Black; }}
    .stButton>button{{width:100%;
            border-radius:15px;
            height:3em;
            background-color:yellow;
            color:white;}}
    .stTextInput>div>div>input {{ 
        border-radius: 15px;
        background-color: skyblue ; 
    }}

    div[data-testid="stForm"] {{
        border: 2px solid black; 
        border-radius: 15px; 
        padding: 20px; 
        background-color: grey ; 
    }}
    .stStatus>div{{ border: 2px solid black; 
        border-radius: 15px; 
        padding: 20px; 
        background-color: lightgrey;
    }}
    </style>
    """, unsafe_allow_html=True)

#db_path = st.secrets["connections"]["sales_database"]["path"]
#client = ai.Client()

# this sets the title of the app pages and give a small description on the agent capabilities.
if theme_selection == "Dark":
    st.markdown("<h1 style='text-align: center;color:white;'>🤖 AI Agentic Orchestrator</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center;color:black;'>🤖 AI Agentic Orchestrator</h1>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: white;'>Seamlessly querying Weather, SQL Databases, and General Knowledge bases.</p>", unsafe_allow_html=True)
st.divider()

# 
# creates a container for the user input form.
with st.container(border=True):
    with st.form("agent_input", clear_on_submit=True):
        user_query = st.text_input(
            "What can I help you with today?", 
            placeholder="e.g. List the top 10 customers or what is the weather in NYC?",
            help="Type your request and our agents will route it to the correct tool."
        )
        
        # Using columns inside the form for a compact button
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            submitted = st.form_submit_button("🚀 Ask Agent")

# checks for the user submission, validates the input and hands the query to agent for processing.
if submitted:
    if not user_query:
        st.warning("Please enter a question.")
    else:
        # Create a dedicated "Response" container
        with st.status("🔍 Agents are collaborating...", expanded=True) as status:
            try:
                st.write("Routing query...")
                result = Agentic_AI_orchestrator(
                    user_prompt=user_query,
                    db_path=db_path,
                    model="openai:gpt-5"
                )
                status.update(label="✅ Task Completed!", state="complete", expanded=True)

                # cretes result cintainer for visual separation for the answer
                st.subheader("Results")
                if isinstance(result, pd.DataFrame):
                    st.dataframe(result, use_container_width=True)
                    st.balloons()
                else:
                    st.markdown(f"""
                                <div style="background-color: #f0f0f0; 
                                padding: 15px; 
                                border-radius: 10px;
                                border-left: 5px solid #4CAF50;
                                color: #333333;
                                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                                ">
                                <span style="font-size: 16px;">{result}</span>
                                </div>
                                """, unsafe_allow_html=True
                    
                    )
                    st.snow()
            #handles any exceptions that may occur during the agent processing and displays an error message to the user
            except Exception as e:
                st.error(f'Error: {e}')