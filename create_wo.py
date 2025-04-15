import streamlit as st
import requests
from datetime import datetime, timedelta, timezone

generic_api = ""

def create_wo_ui():
    st.header("✅ Create Work Order")
    generic_api = "https://fieldtechmiddlewaredemo.azurewebsites.net/api/fta_middleware_generic_api"
    device_ids = ["None"]
    device_ids = device_ids + get_all_key("id", generic_api)
    operation_type = ""
    
    env = st.radio("Create work order on", ["Local", "Prod"], horizontal=True)
    if env == "Prod":
        generic_api = "https://fieldtechmiddleware.azurewebsites.net/api/fta_middleware_generic_api"
    email_id = st.text_input("Assign to(Email-Id)")
    
    device_id = st.selectbox("Device Id(Enter Id and Press 'Enter' key to populate)", device_ids)
    print(device_id)
    if device_id != "None":
        device_info = get_device_info(generic_api, device_id)[0]
        operation_type = device_info["operation_type"]
    op_type = st.text_input("Operation Type", value=operation_type, disabled=True)
    description = st.text_area("Description")
    assigned_to = st.text_input("Assigned To")
    due_date = st.date_input("Available time slots")
    
    
    # Check if all fields are filled
    all_filled = all([
        email_id.strip(),
        description.strip(),
        assigned_to.strip(),
        due_date
    ])
    
    create_button = st.button("Create", disabled=not all_filled)
    
    if create_button:
        st.success(f"Work Order '{email_id}' created successfully!")
        
def get_device_info(api_url, device_id):
    print("Getting Device info")
    payload = {
        "method": "GET",
        "operation_type": "device_management",
        "payload": {
            "device_id": device_id
        }    
    }
    response = requests.post(api_url, json=payload)
    response = response.json()["response"]
    return response

def get_all_devices(api_url):
    print("Getting Device info")
    payload = {
        "method": "GET-ALL",
        "operation_type": "device_management",
        "payload": {
        }    
    }
    response = requests.post(api_url, json=payload)
    response = response.json()["response"]
    return response

def get_all_key(key, api_url):
    allData = get_all_devices(api_url)
    result = []
    for data in allData:
        if "section_info" in data.keys():
            result.append(data.get(key))
        
    return result

def get_assigned_time_and_scheduled_time():
    current_time = datetime.now(timezone.utc)
    days_later = current_time + timedelta(days=6)
    return str(current_time), str(days_later)

def available_time_slots():
    pass
    

    
    