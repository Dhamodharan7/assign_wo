import streamlit as st

# App title
st.markdown("<h1 style='text-align: center; color: steelblue;'>FTA Workorder Management</h1>", unsafe_allow_html=True)
st.markdown("---")

# Top menu tabs
tab1, tab2, tab3 = st.tabs([
    "✅ Create Work Order", 
    "🔄 Update Work Order", 
    "🖼️ Generate Evaluation Images"
])

# Tab: Create Work Order
with tab1:
    st.title("✅ Create Work Order")
    
    work_order_id = st.text_input("Work Order ID")
    description = st.text_area("Description")
    assigned_to = st.text_input("Assigned To")
    due_date = st.date_input("Due Date")
    
    if st.button("Create"):
        st.success(f"Work Order '{work_order_id}' created successfully!")

# Tab: Update Work Order
with tab2:
    st.title("🔄 Update Work Order")
    
    existing_id = st.text_input("Enter Existing Work Order ID")
    new_status = st.selectbox("Update Status", ["Pending", "In Progress", "Completed", "On Hold"])
    remarks = st.text_area("Remarks")
    
    if st.button("Update"):
        st.success(f"Work Order '{existing_id}' updated to '{new_status}' status.")

# Tab: Generate Evaluation Images
with tab3:
    st.title("🖼️ Generate Evaluation Images")
    
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        if st.button("Generate Evaluation"):
            st.info("🔄 Processing...")
            # Placeholder for actual image evaluation logic
            st.success("✅ Evaluation image generated!")
