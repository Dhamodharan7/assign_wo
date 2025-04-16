import streamlit as st
from create_wo import create_wo_ui
from generate_eval import generate_eval_ui
from delete_wo import delete_wo_ui
from update_wo import update_wo_ui

# Set page configuration with a custom favicon (emoji or file)
st.set_page_config(
    page_title="FTA Workorder Management",
    page_icon="🛠️",  # You can also use: "favicon.png"
    layout="wide"
)

# App title
st.markdown("<h1 style='text-align: center; color: steelblue;'>FTA Workorder Management</h1>", unsafe_allow_html=True)
st.markdown("---")

# Top menu tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "✅ Create Work Order", 
    "🔄 Update Work Order", 
    "❌ Delete Work Order", 
    "🖼️ Generate Evaluation Images"
])

# Tab 1: Create Work Order
with tab1:
    # Generate UI
    create_wo_ui()

# Tab 2: Update Work Order
with tab2:
    update_wo_ui()

# Tab 3: Delete Work Order
with tab3:
    # Delete Work order UI
    delete_wo_ui()

# Tab 4: Generate Evaluation Images
with tab4:
    
    generate_eval_ui()
