import sys
import os

# Add the current directory to sys.path to allow imports from root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.streamlit_app import main

if __name__ == "__main__":
    main()
