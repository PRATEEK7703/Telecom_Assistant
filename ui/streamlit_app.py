import streamlit as st
import os
import shutil
import streamlit as st
import os
import shutil
import sqlite3
import nest_asyncio
nest_asyncio.apply()
from orchestration.graph import app
from config.config import STREAMLIT_PAGE_TITLE, STREAMLIT_PAGE_ICON, DOCS_DIR
from utils.document_loader import load_documents

import base64
import textwrap

def mermaid(code: str):
    # Use Mermaid.ink to render the diagram as an image
    # This avoids local JS syntax errors
    graphbytes = code.encode("utf8")
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    url = "https://mermaid.ink/img/" + base64_string
    st.image(url, use_container_width=True)

def main():
    st.set_page_config(page_title=STREAMLIT_PAGE_TITLE, page_icon=STREAMLIT_PAGE_ICON, layout="wide")

    # Custom CSS for Dark Theme and Premium Look
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@500;700&display=swap');

        /* Global Styles */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #e2e8f0;
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Outfit', sans-serif;
            color: #f8fafc !important;
            font-weight: 700;
            letter-spacing: -0.02em;
        }

        /* Hide Streamlit Header & Adjust Top Padding */
        header[data-testid="stHeader"] {
            background-color: transparent;
        }
        header[data-testid="stDecoration"] {
            display: none;
        }
        .block-container {
            padding-top: 1rem !important;
        }

        /* Main Background */
        .stApp {
            background: radial-gradient(circle at top left, #0f172a, #020617);
            color: #f8fafc;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: rgba(15, 23, 42, 0.7);
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }
        
        /* Inputs */
        .stTextInput > div > div > input {
            background-color: rgba(30, 41, 59, 0.4);
            color: #f8fafc;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 12px 16px;
            transition: all 0.3s ease;
        }
        .stTextInput > div > div > input:focus {
            border-color: #818cf8;
            box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.2);
            background-color: rgba(30, 41, 59, 0.6);
        }
        
        /* Selectbox */
        .stSelectbox > div > div > div {
            background-color: rgba(30, 41, 59, 0.4);
            color: #f8fafc;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.3), 0 2px 4px -1px rgba(79, 70, 229, 0.15);
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.4), 0 4px 6px -2px rgba(79, 70, 229, 0.2);
            border-color: rgba(255, 255, 255, 0.2);
        }
        
        /* Chat Messages */
        .stChatMessage {
            background-color: rgba(30, 41, 59, 0.3);
            backdrop-filter: blur(12px);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            transition: border-color 0.3s ease;
        }
        .stChatMessage:hover {
            border-color: rgba(255, 255, 255, 0.1);
        }
        [data-testid="stChatMessageContent"] {
            color: #e2e8f0;
        }
        
        /* Markdown Text */
        .stMarkdown p, .stMarkdown li, .stMarkdown span {
            color: #cbd5e1 !important;
            line-height: 1.7;
        }
        
        /* Markdown Tables */
        .stMarkdown table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            color: #f8fafc !important;
            background-color: rgba(30, 41, 59, 0.3);
            border-radius: 16px;
            overflow: hidden;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .stMarkdown th {
            background-color: rgba(15, 23, 42, 0.6);
            color: #f8fafc !important;
            padding: 1.2rem;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            font-weight: 600;
        }
        .stMarkdown td {
            padding: 1.2rem;
            color: #cbd5e1 !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
        }
        .stMarkdown tr:last-child td {
            border-bottom: none;
        }
        
        /* Streamlit Tables (st.table, st.dataframe) */
        [data-testid="stTable"], [data-testid="stDataFrame"] {
            color: #f8fafc !important;
        }
        .stTable th, .stTable td, .stDataFrame th, .stDataFrame td {
            color: #cbd5e1 !important;
            background-color: rgba(30, 41, 59, 0.3) !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: rgba(15, 23, 42, 0.4);
            padding: 8px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: 14px;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
            color: #94a3b8;
            border: none;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        .stTabs [aria-selected="true"] {
            background-color: rgba(79, 70, 229, 0.2);
            color: #a5b4fc;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.1);
        }
        
        /* Login Card */
        .login-container {
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.8));
            backdrop-filter: blur(24px);
            padding: 4rem 3rem;
            border-radius: 32px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            position: relative;
            overflow: hidden;
        }
        .login-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        }
        
        /* Success/Error/Info Messages */
        .stAlert {
            background-color: rgba(30, 41, 59, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            color: #f8fafc;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        /* Dividers */
        hr {
            border-color: rgba(255, 255, 255, 0.08) !important;
        }
        </style>
        """, unsafe_allow_html=True)

    # Session State for Login
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_type = None
        st.session_state.username = None

    if not st.session_state.logged_in:
        # Login Page
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("<div style='height: 10vh;'></div>", unsafe_allow_html=True)
            
            # Container for the login card
            with st.container():
                st.markdown(f"""
                <div class="login-container">
                    <h1 style='text-align: center; margin-bottom: 0.5rem;'>{STREAMLIT_PAGE_ICON}</h1>
                    <h2 style='text-align: center; margin-bottom: 2rem;'>{STREAMLIT_PAGE_TITLE}</h2>
                </div>
                """, unsafe_allow_html=True)
                
                # We can't put Streamlit widgets inside HTML, so we just visually group them
                # Ideally we would put them inside the div, but Streamlit doesn't support that easily.
                # So we simulate it by styling the surrounding area or just keeping it clean.
                # For this iteration, let's just keep the widgets clean below the header.
                
                st.markdown("### Login")
                email = st.text_input("Email Address", placeholder="name@example.com")
                user_type = st.selectbox("User Type", ["Customer", "Admin"])
                
                st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
                
                if st.button("Sign In", use_container_width=True):
                    if email:
                        # Exception for admin
                        if email == "admin@example.com":
                            st.session_state.logged_in = True
                            st.session_state.user_type = "Admin"
                            st.session_state.username = email
                            st.rerun()
                            return

                        # Check if user exists in database
                        try:
                            conn = sqlite3.connect('data/telecom.db')
                            cursor = conn.cursor()
                            
                            # Check in customers table
                            cursor.execute("SELECT * FROM customers WHERE email = ?", (email,))
                            user = cursor.fetchone()
                            
                            conn.close()
                            
                            if user:
                                st.session_state.logged_in = True
                                st.session_state.user_type = user_type
                                st.session_state.username = email
                                st.rerun()
                            else:
                                st.error("Access Denied: User not found in database.")
                                
                        except Exception as e:
                            st.error(f"Database error: {e}")
                    else:
                        st.error("Please enter an email address.")
        return

    # Sidebar
    with st.sidebar:
        st.title(f"{STREAMLIT_PAGE_ICON} {STREAMLIT_PAGE_TITLE}")
        
        # Navigation
        st.header("Navigation")
        if st.session_state.user_type == "Customer":
            page = st.radio("Go to", ["Customer Support"])
        else:
            page = st.radio("Go to", ["Admin Dashboard", "Project Architecture"])

        st.divider()
        
        if st.session_state.user_type == "Customer":
            st.success("Logged in as Customer")
            if st.button("Clear Chat History"):
                st.session_state.messages = []
                st.rerun()
        else:
            st.success("Logged in as Admin")
        
        st.write(f"Email: {st.session_state.username}")
        
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.session_state.username = None
            st.rerun()

    # Main Content based on Selection
    if page == "Project Architecture":
        st.title("Project Architecture")
        st.markdown("Here is the high-level architecture of the Telecom Service Assistant, showing how different agents and frameworks interact.")
        
        graph = """
        graph TD
            User[User (Streamlit UI)] -->|Query| Graph[LangGraph Orchestrator]
            
            subgraph "The Brain (LangGraph)"
                Graph --> Classifier[Classifier Node]
                Classifier -->|Billing?| BillingNode
                Classifier -->|Network?| NetworkNode
                Classifier -->|Service?| ServiceNode
                Classifier -->|Technical?| KnowledgeNode
            end
            
            subgraph "Billing Dept (CrewAI)"
                BillingNode --> BillingSpecialist[Billing Specialist Agent]
                BillingSpecialist -->|Analysis| ServiceAdvisor[Service Advisor Agent]
                ServiceAdvisor -->|Report| BillingNode
            end
            
            subgraph "Network Dept (AutoGen)"
                NetworkNode --> GroupChat[Group Chat]
                GroupChat --> UserProxy[User Proxy]
                GroupChat --> Diag[Diagnostics Agent]
                GroupChat --> Router[Router Agent]
                GroupChat --> Connect[Connectivity Agent]
                Diag <--> Router <--> Connect
                GroupChat -->|Solution| NetworkNode
            end
            
            subgraph "Sales Dept (LangChain)"
                ServiceNode --> ReAct[ReAct Agent]
                ReAct <-->|SQL Queries| DB[(SQLite Database)]
                ReAct -->|Recommendation| ServiceNode
            end
            
            subgraph "Tech Support (LlamaIndex)"
                KnowledgeNode --> QueryEngine[Vector Query Engine]
                QueryEngine <-->|Search| VectorStore[(Vector Store)]
                QueryEngine -->|Answer| KnowledgeNode
            end
            
            BillingNode --> Response[Final Response]
            NetworkNode --> Response
            ServiceNode --> Response
            KnowledgeNode --> Response
            Response --> User
        """
        # Display the generated architecture image
        if os.path.exists("architecture_diagram.png"):
            st.image("architecture_diagram.png", caption="System Architecture", use_container_width=True)
        else:
            st.error("Architecture image not found.")
            
        st.divider()
        
        st.markdown("""
        ## The Flow (Step-by-Step)

        Here is what happens when a user types a message:

        ### Step 1: Input & State (`ui/streamlit_app.py` -> `orchestration/state.py`)
        - The user types "Why is my bill so high?" in the Streamlit UI.
        - The app packages this into a **State** object (a dictionary containing the query, chat history, and current status).
        - This State is passed to the **LangGraph** application.

        ### Step 2: Classification (`orchestration/graph.py`)
        - The first node in the graph is the **Classifier**.
        - It uses an LLM (GPT-4o) to analyze the intent of the query.
        - **Prompt**: "Is this query about billing, network, plans, or technical help?"
        - **Decision**: The Classifier determines this is a **Billing** query.

        ### Step 3: Routing (`orchestration/graph.py`)
        - Based on the classification, the graph follows a "Conditional Edge".
        - It moves the execution to the **Billing Node**.

        ### Step 4: Agent Execution (The "Specialists")

        #### Scenario A: Billing (CrewAI) - `agents/billing_agents.py`
        - **Structure**: A "Crew" of two agents working sequentially.
        - **Agent 1 (Billing Specialist)**:
            - **Goal**: Analyze the data.
            - **Action**: Uses a tool (`SQLQueryTool`) to check the `billing` and `usage` tables in the SQLite database.
            - **Output**: "User used 50GB data, limit was 20GB. Overcharge of $50."
        - **Agent 2 (Service Advisor)**:
            - **Goal**: Recommend a solution.
            - **Input**: The Specialist's analysis.
            - **Output**: "I recommend upgrading to the Unlimited Plan to save money."
        - **Result**: A structured Markdown report.

        #### Scenario B: Network (AutoGen) - `agents/network_agents.py`
        - **Structure**: A "Group Chat" of agents talking to each other.
        - **Agents**:
            - **User Proxy**: Represents the human admin (or the system trigger).
            - **Diagnostics Agent**: "I see high latency in the logs."
            - **Router Agent**: "Try changing the APN settings to 'fast.net'."
            - **Connectivity Specialist**: Synthesizes the conversation into a guide.
        - **Flow**: They chat back and forth until the User Proxy sees "TERMINATE" or the max rounds are reached.
        - **Result**: A step-by-step troubleshooting guide.

        #### Scenario C: Service Plans (LangChain) - `agents/service_agents.py`
        - **Structure**: A "ReAct" (Reasoning + Acting) Agent.
        - **Process**:
            - **Thought**: "I need to find plans for a family."
            - **Action**: `SELECT * FROM service_plans WHERE type = 'Family'`.
            - **Observation**: Gets list of plans.
            - **Thought**: "The Family Share Plan is best."
            - **Answer**: Formulates the final response.
        - **Result**: A plan recommendation with details.

        #### Scenario D: Technical Help (LlamaIndex) - `agents/knowledge_agents.py`
        - **Structure**: RAG (Retrieval-Augmented Generation).
        - **Process**:
            - **Embed**: Converts "How to enable VoLTE" into numbers (vector).
            - **Retrieve**: Searches the `storage` (Vector Store) for matching document chunks (e.g., from `network_guide.md`).
            - **Synthesize**: Feeds the retrieved text + query to the LLM to generate an answer.
        - **Result**: A technical answer based *only* on your uploaded docs.

        ### Step 5: Response (`ui/streamlit_app.py`)
        - The active agent returns its final string (formatted in Markdown).
        - LangGraph updates the **State** with this response.
        - Streamlit reads the response from the State and displays it in the chat window.

        ## 4. Key Integration Points

        - **Shared Database (`telecom.db`)**:
            - Accessed by Billing (CrewAI) and Service (LangChain) agents.
            - Ensures they see the same customer data.
        - **Shared Vector Store (`storage/`)**:
            - Managed by the Admin Dashboard (uploading docs).
            - Read by the Knowledge Agent (answering questions).
        - **Unified UI**:
            - The user doesn't know there are 4 different frameworks behind the scenes. They just see a helpful assistant.
        """)

    elif st.session_state.user_type == "Customer" and page == "Customer Support":
        # Customer Dashboard
        tab1, tab2, tab3 = st.tabs(["Chat Assistant", "My Account", "Network Status"])
        
        with tab1:
            st.header("Chat with our AI Assistant")
            st.markdown("How can I help you today?")

            # Initialize chat history
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Display chat messages
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Chat Input
            if prompt := st.chat_input("What is your query?"):
                st.chat_message("user").markdown(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})

                with st.spinner("Processing your request..."):
                    try:
                        inputs = {
                            "query": prompt,
                            "user_email": st.session_state.username
                        }
                        result = app.invoke(inputs)
                        response = result["response"]
                        
                        with st.chat_message("assistant"):
                            st.markdown(response)
                        
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
        
        with tab2:
            st.header("My Account")
            
            user_email = st.session_state.username
            if user_email:
                try:
                    conn = sqlite3.connect('data/telecom.db')
                    conn.row_factory = sqlite3.Row # Allow accessing columns by name
                    cursor = conn.cursor()
                    
                    cursor.execute("SELECT * FROM customers WHERE email = ?", (user_email,))
                    user_data = cursor.fetchone()
                    
                    conn.close()
                    
                    if user_data:
                        st.subheader("Profile Details")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**Name:** {user_data['name']}")
                            st.markdown(f"**Email:** {user_data['email']}")
                            st.markdown(f"**Phone:** {user_data['phone_number']}")
                            st.markdown(f"**Address:** {user_data['address']}")
                            
                        with col2:
                            st.markdown(f"**Customer ID:** {user_data['customer_id']}")
                            st.markdown(f"**Plan ID:** {user_data['service_plan_id']}")
                            st.markdown(f"**Status:** {user_data['account_status']}")
                            st.markdown(f"**Member Since:** {user_data['registration_date']}")
                            
                    else:
                        st.warning("Customer profile not found in database.")
                        
                except Exception as e:
                    st.error(f"Error fetching account details: {e}")
            else:
                st.error("No user logged in.")
            
        with tab3:
            st.header("Network Status")
            st.info("Network status map feature coming soon. You can ask the chat assistant for network issues in your area.")

    elif st.session_state.user_type == "Admin" and page == "Admin Dashboard":
        # Admin Dashboard
        st.title("Admin Dashboard")
        tab1, tab2, tab3 = st.tabs(["Knowledge Base Management", "Customer Support", "Network Monitoring"])
        
        with tab1:
            st.subheader("Upload Documents to Knowledge Base")
            uploaded_files = st.file_uploader("Upload PDF, Markdown, or Text files", accept_multiple_files=True, type=["txt", "md", "pdf"])

            if uploaded_files:
                if st.button("Process Documents"):
                    if not os.path.exists(DOCS_DIR):
                        os.makedirs(DOCS_DIR)
                    
                    for uploaded_file in uploaded_files:
                        file_path = os.path.join(DOCS_DIR, uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        st.success(f"Saved {uploaded_file.name}")
                    
                    with st.spinner("Updating Knowledge Base..."):
                        load_documents()
                        st.success("Knowledge Base Updated Successfully!")

            st.subheader("Existing Documents")
            if os.path.exists(DOCS_DIR):
                files = os.listdir(DOCS_DIR)
                if files:
                    # Display as a table
                    file_data = [{"Document Name": f, "Type": f.split('.')[-1].upper()} for f in files]
                    st.table(file_data)
                else:
                    st.info("No documents found.")
            else:
                st.info("Documents directory does not exist.")
        
        with tab2:
            st.header("Customer Support Tickets")
            st.info("Ticket management system coming soon.")
            
        with tab3:
            st.header("Network Monitoring")
            st.info("Real-time network monitoring dashboard coming soon.")

if __name__ == "__main__":
    main()
