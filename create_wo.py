import streamlit as st
import requests
from datetime import datetime, timedelta, timezone
import random

generic_api = ""

def create_wo_ui():
    st.header("✅ Create Work Order")
    generic_api = "https://fieldtechmiddlewaredemo.azurewebsites.net/api/fta_middleware_generic_api"
    device_ids = ["None"]
    available_slots = ["None"]
    operation_type = ""
    
    env = st.radio("Create work order on", ["Local", "Prod"], horizontal=True, key="env_radio1")
    if env == "Prod":
        generic_api = "https://fieldtechmiddleware.azurewebsites.net/api/fta_middleware_generic_api"
        
    # Enter Operation type
    operation_type = st.selectbox("Operation type", ["installation", "troubleshooting"])

    # Select Device Id
    if operation_type:
        device_ids = device_ids + get_all_device_details(generic_api, operation_type)
    device_id = st.selectbox("Device Id(Enter Id and Press 'Enter' key to populate)", device_ids)
    print(device_id)
    
    # Select Email Id
    email_id = st.text_input("Assign to(Email-Id)")

    # Select available time slot
    if email_id and operation_type:
        available_slots = available_slots + available_time_slots(generic_api, email_id, operation_type)
    if email_id and len(available_slots) < 2:
        st.warning(f"No available slots! Delete other work order to proceed.")
    selected_slot = st.selectbox("Available time slot(Enter email id and Press 'Enter' key to populate)", available_slots)
    if selected_slot != "None":
        order_start_time = selected_slot.split("-")[0].strip()
        order_due_time = selected_slot.split("-")[1].strip()
    
    
    # Check if all fields are filled
    all_filled = all([
        email_id.strip(),
        operation_type.strip(),
        device_id.strip(),
        selected_slot.strip()
    ])
    
    create_button = st.button("Create", disabled=not all_filled)
    
    if create_button:
        print(selected_slot)
        if selected_slot == "None":
            st.warning(f"Please select valid time slot")
        elif device_id == "None":
            st.warning(f"Please select valid device id")
        else:
            device_id = device_id.split("-")[0].strip()
            response = create_work_order(generic_api, email_id, device_id, operation_type, order_start_time, order_due_time)
            print(response)
            if "uccess" in response:
                st.success(f"Work Order for '{email_id}' created successfully!")
            else:
                st.error(f"Work Order for '{email_id}' can't be created at this moment. Try again later!")


        
def create_work_order(api_url, email_id, device_id, operation_type, order_start_time, order_due_time):
    Order_Assigned_Time, Order_Scheduled_Time = get_assigned_time_and_scheduled_time()
    address, site, map_loc = get_random_site_and_address()
    device_detail = get_device_info(api_url, device_id)[0]
    source_doc = device_detail.get("source_doc", "")
    work_order_default = {
                        "Device_ID": f"{device_id}",
                        "Device_Installation_ID": "Ericsson 6160",
                        "Order_Creation_Time": f"{Order_Assigned_Time}",
                        "Order_Type": f"{operation_type}",
                        "Order_Assigned_Time": f"{Order_Assigned_Time}",
                        "Order_Site": f"{site}",
                        "Order_Address": f"{address}",
                        "Order_Map_Name": f"{map_loc}",
                        "Order_Lat_Lon": "33.01691819998306, -96.69424252820593",
                        "Order_Scheduled_Time": f"{Order_Scheduled_Time}",
                        "Order_Categories": "Enclosure Installation",
                        "Order_Description": "The Ericsson 6160 enclosure is scheduled for installation within the allocated time slot. Ensure compliance with site access protocols and prerequisites as outlined in the MoP document. Before commencing the installation, verify the site's viability, cabinet specifications, power supply, and other necessary parameters. After installation, provide post-installation photos, including cabinet cable routing, inlet sealing, and grounding, to confirm the quality of the work. If any issues arise during the installation, promptly escalate them to the field supervisor for timely resolution.",
                        "Order_Assigned_By": "Mr Sukryool",
                        "Order_Notes": "Site Constraints: Ensure there is adequate space for Ericsson 6160 installation, with at least 1-meter clearance on all sides for ventilation and maintenance. The site must have a stable, flat surface to prevent vibration or tilt issues that may affect enclosure stability.\n\nWeather Conditions: Predicted weather for the installation day suggests moderate rainfall with gusty winds. Ensure all components are covered to avoid exposure to moisture and delay the installation if heavy rainfall is present. Use protective gear and anti-slip measures for safety.\n\nSite Access Restrictions: Coordinate with the site owner/manager at least 48 hours before arrival. Access is restricted during non-business hours, and additional identification might be required. Confirm entry clearance from the customer and follow the site’s security protocols. Make sure to carry all necessary permissions and an access key if needed.\n\nSafety Precautions: Follow all safety guidelines, including wearing PPE (Personal Protective Equipment) like gloves, helmets, and safety boots. Be cautious of any live cables and hazardous materials in the vicinity. Ensure grounding measures are implemented before energizing the equipment. ",
                        "Order_Task_Groups": "",
                        "Order_Chat_History": "",
                        "Order_Start_Time": f"{order_start_time}",
                        "Order_Due_Time": f"{order_due_time}",
                        "Order_Finish_Time": "",
                        "Order_Priority": "High",
                        "Order_Logs": "",
                        "Order_User": f"{email_id}",
                        "Order_Status": f"open",
                        "data": {}
                    }
    
    if "juniper" in source_doc.lower():
        work_order_default["Order_Categories"] = "Fan Repair"
        work_order_default["Order_Description"] = "The ALM light on Juniper EX4200 (Node-1) has turned red, indicating a fan failure issue as observed in the system log alarm. A site visit is required to physically troubleshoot and resolve the issue."
        work_order_default["Order_Notes"] = "Data Center Environment: The data center is temperature-controlled, but a fan failure could result in localized overheating. Monitor environmental sensors and ensure the surrounding temperature remains within acceptable limits during troubleshooting. Be mindful of air circulation in the vicinity; any disruption might affect other nearby equipment. Utilize portable cooling if necessary. Ensure moisture levels are below 50% relative humidity to prevent any risk of condensation affecting the switch. \n\n Cabling Map: Before proceeding, consult the latest cabling map to identify cable connections around the affected switch. Ensure cables are clearly labeled and organized to avoid accidental disconnections during fan replacement. Disconnect any cables carefully, documenting each, to facilitate reinstallation after the fan issue is resolved. \n\n Data Center Access Restrictions: Access is restricted to authorized personnel only. Coordinate with the data center admin team at least 24 hours in advance to schedule entry. Carry your access badge, government-issued ID, and ensure to adhere to the data center's security protocols. Unauthorized tools or equipment may not be permitted, so verify compliance beforehand. \n\n SLA and Timeline: The SLA for fixing the fan failure is 4 hours. Immediate action is required to prevent network downtime. Ensure the replacement fan unit is compatible with the Juniper EX4300 and is available before proceeding to the site. If the fan cannot be replaced within the SLA, contact the NOC immediately to escalate the incident and inform stakeholders about potential impact."

    elif "viavi" in source_doc.lower():
        work_order_default["Order_Categories"] = "Site Installation"
        work_order_default["Order_Description"] = "Ensure the installation of 4G and 5G cell sites meets required specifications by verifying the performance of antennas, cables, and any additional tower-mounted elements, as well as fronthaul and backhaul connectivity, before integrating the new cell site into the network. "
        work_order_default["Order_Notes"] = "Ensure acceptance requirements are met to ensure the quality of 4G and 5G transmitted signals, antenna alignments, coax and optical fiber systems. The adoption of any of the suggested tests, should include on the use of standard setup and calibration techniques to establish the necessary criteria that determine the validity of the antenna systems being tested."
    
    
    if "meta_data_json" in device_detail:
        work_order_default["Device_Installation_ID"] = device_detail["meta_data_json"][0]["device_name"] if len(device_detail["meta_data_json"]) > 0 else ""
        work_order_default["Order_Issue_Type"] = device_detail["meta_data_json"][0]["issue_type"] if len(device_detail["meta_data_json"]) > 0 else ""
            
    work_order_default["data"] = device_detail["section_info"] if "section_info" in device_detail else []
    work_order_default["validationInfo"] = device_detail["validation_info"] if "validation_info" in device_detail else []
    
    # create work order
    req_payload = {
        "operation_type": "work_order_management",
        "method": "POST",
        "payload": work_order_default
    }
    print("Created work order::")

    response = requests.post(api_url, json=req_payload)
    response = response.json()  # Parse JSON response
    return response["response"]
        
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

def get_device_info(api_url, device_id):
        #get device_info
    req_payload = {
        "operation_type": "device_management",
        "method": "GET",
        "payload": {
            "device_id": f"{device_id}",
        }
    }
    print("Getting device info")
    response = requests.post(api_url, json=req_payload)
    device_detail = response.json()  # Parse JSON response
    return device_detail["response"]

def get_all_devices(api_url, operation_type):
    print("Getting All Device info")
    payload = {
        "method": "GET",
        "operation_type": "device_management",
        "payload": {
            "operation_type": operation_type
        }    
    }
    response = requests.post(api_url, json=payload)
    response = response.json()["response"]
    return response

def get_all_device_details(api_url, operation_type):
    allData = get_all_devices(api_url, operation_type)
    result = []
    for data in allData:
        
        if "section_info" in data.keys():
            op_type = data.get('operation_type')
            id = data.get("device_id")
            name = data.get("device_name")
            result.append(f"{id} - {name} - {op_type}")
        
    return result

def get_assigned_time_and_scheduled_time():
    current_time = datetime.now(timezone.utc)
    days_later = current_time + timedelta(days=6)
    return str(current_time), str(days_later)

def available_time_slots(api_url, email_id, operation_type):
    order_start_time = ["8:00", "10:00", "11:30", "13:00", "14:30", "16:30"]
    order_due_time = ["9:00", "10:30", "12:00", "13:30", "15:30", "17:00"]
    av_slot = []
    
    print(f"Getting WO for :{email_id} - {operation_type}")
    payload = {
        "method": "GET",
        "operation_type": "work_order_management",
        "payload": {
            "Order_Type": operation_type,
            "Order_User": email_id
        }    
    }
    response = requests.post(api_url, json=payload)
    work_orders = response.json()["response"]
    
    for wo in work_orders:
        if wo.get("Order_Start_Time") in order_start_time:
            index = order_start_time.index(wo.get("Order_Start_Time"))
            order_start_time.pop(index)
            order_due_time.pop(index)
    for count, ele in enumerate(order_start_time):
        av_slot.append(order_start_time[count] + "-" + order_due_time[count])
    return av_slot

def get_random_site_and_address():
    Order_Address_maps = [
  {
      "address": "4823 Oak Meadow Dr, Houston, TX 77018",
      "map": "https://feldtchaspstg01.blob.core.windows.net/fta-images/maps/houston.png"
  },
  {
      "address": "7831 Sunset Trail, Austin, TX 78745",
      "map": "https://feldtchaspstg01.blob.core.windows.net/fta-images/maps/austin.png"
  },
  {
      "address": "6245 Bluebonnet Ln, Dallas, TX 75209",
      "map": "https://feldtchaspstg01.blob.core.windows.net/fta-images/maps/dallas.png"
  },
  {
      "address": "3902 Lone Star Pkwy, San Antonio, TX 78253",
      "map": "https://feldtchaspstg01.blob.core.windows.net/fta-images/maps/san-antonio.png"
  },
  {
      "address": "2184 Prairie Rose St, El Paso, TX 79938",
      "map": "https://feldtchaspstg01.blob.core.windows.net/fta-images/maps/el-paso.png"
  },
  {
      "address": "1109 Brady Ridge Dr, Round Rock, TX 78681",
      "map": "https://feldtchaspstg01.blob.core.windows.net/fta-images/maps/round-rock.png"
  },
  {
      "address": "3571 Silver Creek Dr, Arlington, TX 76016",
      "map": "https://feldtchaspstg01.blob.core.windows.net/fta-images/maps/arlington.png"
  },
  {
      "address": "9214 Pecan Grove Ln, Corpus Christi, TX 78410",
      "map": "https://feldtchaspstg01.blob.core.windows.net/fta-images/maps/corpus-christi.png"
  },
  {
      "address": "7401 Westwind Blvd, Lubbock, TX 79424",
      "map": "https://feldtchaspstg01.blob.core.windows.net/fta-images/maps/lubbock.png"
  },
  {
      "address": "4501 Tejas Trail, Austin, TX 78745",
      "map": "https://feldtchaspstg01.blob.core.windows.net/fta-images/maps/austin1.png"
  }
]
    random_address_map = random.choice(Order_Address_maps)
    random_address = random_address_map["address"]
    random_map = random_address_map["map"]
    state = random_address.split(", ")[-1].split(" ")[0]

    site_number = random.randint(1, 99)
    random_site = f"{state}{site_number}"
    return random_address, random_site, random_map

    
    
if __name__ == "__main__":
    x = get_all_device_details("https://fieldtechmiddlewaredemo.azurewebsites.net/api/fta_middleware_generic_api", "installation")
    print(x)

    
    