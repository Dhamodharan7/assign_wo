import streamlit as st
import requests
from datetime import datetime, timedelta, timezone

def update_wo_ui():
    st.header("🔄 Update Work Order")
    generic_api = "https://fieldtechmiddlewaredemo.azurewebsites.net/api/fta_middleware_generic_api"
    env = st.radio("Create work order on", ["Local", "Prod"], horizontal=True, key="env_radio2")
    if env == "Prod":
        generic_api = "https://fieldtechmiddleware.azurewebsites.net/api/fta_middleware_generic_api"
    
    existing_id = st.text_input("Enter Existing Work Order ID")
    assign_to = st.text_input("Re-assign Existing Work Order To")

    
    if st.button("Update"):
        response = update_wo(assign_to, generic_api, existing_id)
        print(response)
        if "updated" in response: 
            st.success(f"Work Order '{existing_id}' updated.")
        else:
            st.error(f"Please provide valid work order id")
        
def update_wo(assign_to, api_url, wo_id):
    print(f"Updating WO:{wo_id}")
    payload = {
        "method": "UPDATE",
        "operation_type": "work_order_management",
        "payload": {
            "Order_ID": wo_id,
            "Order_User": assign_to
        }    
    }
    response = requests.post(api_url, json=payload)
    response = response.json()["response"]
    return response