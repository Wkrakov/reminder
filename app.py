import streamlit as st
import json
import os
from datetime import datetime, timedelta

# 🎨 Стили под твою цветовую гамму
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
        background: linear-gradient(135deg, #CCE5FF 0%, #E8EBFF 100%);
    }
    .stButton > button {
        background: linear-gradient(45deg, #949CFF, #7A85E0);
        color: white !important;
        border-radius: 12px;
        border: none;
        height: 42px;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(148, 156, 255, 0.3);
    }
    .stButton > button:hover {
        background: linear-gradient(45deg, #7A85E0, #949CFF);
        box-shadow: 0 6px 12px rgba(148, 156, 255, 0.4);
    }
    .stTextInput > div > div > input, 
    .stSelectbox > div > div > select,
    .stDateInput > div > div > input {
        border-radius: 12px !important;
        border: 2px solid #949CFF !important;
        background-color: #E8EBFF !important;
        color: #F2749B !important;
    }
    h1, h2, h3 {
        color: #F2749B !important;
        font-family: 'sans-serif' !important;
    }
    .stMarkdown {
        c
