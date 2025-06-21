#!/usr/bin/env python3
"""
CareSync - AI-powered personal wellness tracker
Main entry point for the application
"""

import sys
import os

# Add the caresync directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'caresync'))

# Import and run the app
from caresync.app import st

if __name__ == "__main__":
    # This file serves as the entry point for Streamlit
    pass 