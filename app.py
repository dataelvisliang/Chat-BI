import streamlit as st
import pandas as pd
import os
import warnings
from tabs import render_pygwalker_tab, render_plotly_tab, render_echarts_tab

# Suppress deprecation warnings from dependencies
warnings.filterwarnings('ignore', category=DeprecationWarning)

# Page configuration
st.set_page_config(
    page_title="Chat BI - Data Analysis",
    layout="wide"
)

# Title
st.title("💬 Chat BI - Data Analysis with AI")

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 PygWalker", "📈 Plotly", "📊 ECharts"])

# File uploader for CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

# Load data
@st.cache_data
def load_data(file):
    if file is not None:
        df = pd.read_csv(file)
        return df
    return None

# Load the dataset
df = load_data(uploaded_file)

if df is None:
    st.info("👆 Please upload a CSV file to get started")
    st.stop()

# API Configuration in Sidebar
st.sidebar.header("🤖 AI Configuration")
api_key_input = st.sidebar.text_input(
    "OpenRouter API Key",
    type="password",
    value=os.getenv("OPENROUTER_API_KEY", ""),
    help="Enter your OpenRouter API key to enable chat BI"
)

model_choice = st.sidebar.text_input(
    "Model",
    value="amazon/nova-2-lite-v1:free",
    help="Enter the model name (e.g., amazon/nova-2-lite-v1:free, anthropic/claude-3.5-sonnet, openai/gpt-4o)"
)

st.sidebar.markdown("---")

# Display basic info
st.sidebar.header("📊 Dataset Info")
st.sidebar.write(f"**Total Records:** {len(df):,}")
st.sidebar.write(f"**Total Columns:** {len(df.columns)}")

# Show columns
with st.sidebar.expander("View Columns"):
    for col in df.columns:
        st.write(f"• {col} ({df[col].dtype})")

st.sidebar.markdown("---")

# Show raw data option
if st.sidebar.checkbox("Show Raw Data"):
    st.subheader("Raw Data")
    st.dataframe(df)

# Initialize session state for chat history and spec
if "messages" not in st.session_state:
    st.session_state.messages = []
if "messages_plotly" not in st.session_state:
    st.session_state.messages_plotly = []
if "messages_echarts" not in st.session_state:
    st.session_state.messages_echarts = []
if "current_spec" not in st.session_state:
    st.session_state.current_spec = None
if "current_plotly_spec" not in st.session_state:
    st.session_state.current_plotly_spec = None
if "current_echarts_spec" not in st.session_state:
    st.session_state.current_echarts_spec = None
if "spec_version" not in st.session_state:
    st.session_state.spec_version = 0

# Render tabs
with tab1:
    render_pygwalker_tab(df, api_key_input, model_choice)

with tab2:
    render_plotly_tab(df, api_key_input, model_choice)

with tab3:
    render_echarts_tab(df, api_key_input, model_choice)
