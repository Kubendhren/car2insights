
import streamlit as st


def apply_styles():
    st.markdown(
        """
        <style>
        /* Main background */
        .stApp {
            background: linear-gradient(
                135deg, #f5f7ff 0%, #eef2ff 100%
            );
            font-family: 'Segoe UI', sans-serif;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1500px;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(
                180deg, #111827 0%, #202b49 100%
            );
        }

        section[data-testid="stSidebar"] > div:first-child {
            padding: 1.5rem 1rem;
        }

        /* Sidebar text */
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label {
            color: #f8fafc;
        }

        /* Sidebar menu buttons */
        section[data-testid="stSidebar"] .stButton > button {
            width: 100%;
            min-height: 48px;
            text-align: left;
            padding: 10px 15px;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.08);
            background: rgba(255,255,255,0.045);
            color: #e2e8f0;
            font-size: 15px;
            font-weight: 600;
            transition: all 0.2s ease;
        }

        section[data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(59,130,246,0.22);
            border-color: #60a5fa;
            color: #ffffff;
            transform: translateX(3px);
        }

        /* Active menu button */
        section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
            background: linear-gradient(
                100deg, #2563eb 0%, #4f46e5 100%
            );
            color: #ffffff;
            border: 1px solid #93c5fd;
            box-shadow: 0 5px 15px rgba(37,99,235,0.25);
        }

        /* Metric cards */
        div[data-testid="stMetric"] {
            background: white;
            border: 1px solid #e3e8f5;
            padding: 20px;
            border-radius: 17px;
            box-shadow: 0 5px 18px rgba(30,41,59,0.055);
        }

        div[data-testid="stMetricValue"] {
            color: #312e81;
            font-size: 27px;
            font-weight: 800;
        }

        /* Data tables */
        div[data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
        }

        /* Dividers */
        section[data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.15);
        }

        /* Hide Streamlit automatic page navigation */
        [data-testid="stSidebarNav"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
