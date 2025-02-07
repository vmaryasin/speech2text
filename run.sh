#!/bin/bash

# Navigate to the directory containing the Streamlit app
cd "$(dirname "$0")"

# Activate virtual environment (if applicable)
source venv/bin/activate  # Uncomment this if using a virtual environment

# Run the Streamlit app
python3 -m streamlit run whisper_streamlit.py
