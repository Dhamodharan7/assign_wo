import streamlit as st
from create_wo import create_wo_ui
from generate_eval import generate_eval_ui

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
    st.header("🔄 Update Work Order")
    
    existing_id = st.text_input("Enter Existing Work Order ID")
    new_status = st.selectbox("Update Status", ["Pending", "In Progress", "Completed", "On Hold"])
    remarks = st.text_area("Remarks")
    
    if st.button("Update"):
        st.success(f"Work Order '{existing_id}' updated to '{new_status}' status.")

# Tab 3: Delete Work Order
with tab3:
    st.header("❌ Delete Work Order")
    
    delete_id = st.text_input("Enter Work Order ID to Delete")
    
    if st.button("Delete"):
        # Placeholder: Add actual deletion logic here
        st.warning(f"Work Order '{delete_id}' deleted successfully!")

# Tab 4: Generate Evaluation Images
with tab4:
    
    generate_eval_ui()
