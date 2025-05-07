import streamlit as st
import requests


# def delete_wo_ui():
#     generic_api = "https://fieldtechmiddlewaredemo.azurewebsites.net/api/fta_middleware_generic_api"
#     wo_details = ["None"]
#     st.header("❌ Delete Work Order")
    
#     env = st.radio("Create work order on", ["Local", "Prod"], horizontal=True, key="env_radio3")
#     if env == "Prod":
#         generic_api = "https://fieldtechmiddleware.azurewebsites.net/api/fta_middleware_generic_api"
    
#     email_id = st.text_input("Enter your Email Id")
    
#     if email_id:
#         wo_details = get_work_orders_for_email(generic_api, email_id)
        
#     selected_wo = st.selectbox("Select Work Order to Delete(Enter email_id to populate)", wo_details)
    
#     if st.button("Delete"):
#         if selected_wo == "None":
#             # Placeholder: Add actual deletion logic here
#             st.warning(f"Select work order to delete!")
#         else:
#             delete_wo_and_chat(selected_wo, generic_api)
#             st.success(f"Work Order '{email_id}' deleted successfully!")

def delete_wo_ui():
    generic_api = "https://fieldtechmiddlewaredemo.azurewebsites.net/api/fta_middleware_generic_api"
    st.header("❌ Delete Work Order")

    # Step 1: Choose environment
    env = st.radio("Create work order on", ["Local", "Prod", "Custom"], horizontal=True, key="env_radio3")
    if env == "Prod":
        generic_api = "https://fieldtechmiddleware.azurewebsites.net/api/fta_middleware_generic_api"
    elif env == "Custom":
        generic_api = st.text_input("Enter Custom API URL", value=generic_api) # added a text input

    # Step 2: Email input
    email_id = st.text_input("Enter your Email Id")

    # Initialize session state to hold work order list
    if "wo_details" not in st.session_state:
        st.session_state.wo_details = ["None"]

    # Step 3: Fetch work orders if email is entered
    if email_id:
        st.session_state.wo_details = ["None"] + get_work_orders_for_email(generic_api, email_id)

    # Step 4: Select work order from dropdown
    selected_wo = st.selectbox(
                "Select Work Order to Delete",
                st.session_state.wo_details,
                key="selected_wo"
                )

    # Step 5: Delete button logic
    if st.button("Delete"):
        if selected_wo == "None":
            st.warning("⚠️ Select a valid work order to delete!")
        else:
            delete_wo_and_chat(selected_wo, generic_api)
            st.success(f"✅ Work Order deleted successfully!")


            
def delete_wo_and_chat(selected_wo, api_url):
    try:
        wo_id = selected_wo.split('-')[0].strip()
        delete_wo(api_url, wo_id)
        delete_chat_history(api_url, wo_id)
    except:
        return "error"
    
def delete_chat_history(api_url, wo_id):
    print(f"Deleting Chat history:{wo_id}")
    payload = {
        "method": "DELETE",
        "operation_type": "chat_history_management",
        "payload": {
            "workOrderId": wo_id,
        }    
    }
    response = requests.post(api_url, json=payload)
    response = response.json()["response"]
    return response
    
def delete_wo(api_url, wo_id):
    print(f"Deleting Work Order:{wo_id}")
    payload = {
        "method": "DELETE",
        "operation_type": "work_order_management",
        "payload": {
            "Order_ID": wo_id,
        }    
    }
    response = requests.post(api_url, json=payload)
    response = response.json()["response"]
    return response
           
def get_all_work_orders(api_url, email_id):
    print("Getting All Work Orders")
    payload = {
        "method": "GET",
        "operation_type": "work_order_management",
        "payload": {
            "Order_User": email_id
        }    
    }
    response = requests.post(api_url, json=payload)
    response = response.json()["response"]
    return response

def get_work_orders_for_email(api_url, email_id):
    work_orders = get_all_work_orders(api_url=api_url, email_id=email_id)
    details = []
    for work_order in work_orders:
        device_id = work_order["Order_ID"]
        device_name = work_order["Device_Installation_ID"]
        op_type = work_order["Order_Type"]
        order_st = work_order["Order_Start_Time"]
        order_due = work_order["Order_Due_Time"]
        details.append(f"{device_id} - {device_name} - {op_type} - Slot({order_st}-{order_due})")
        
    return details
    
if __name__ == "__main__":
    get_work_orders_for_email("https://fieldtechmiddlewaredemo.azurewebsites.net/api/fta_middleware_generic_api", "d.dhanushkodi@accenture.com")