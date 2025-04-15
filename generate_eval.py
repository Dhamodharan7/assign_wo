import streamlit as st
import glob
from update_metadata import modify_valid_metadata, modify_invalid_metadata
import os
import zipfile
import io
from datetime import date



def generate_eval_ui():
    st.header("🖼️ Generate Evaluation Images")
    
    email = st.text_input("Email ID")
    
    if st.button("Generate"):
        if "@accenture" in email.strip():
            generate_eval_images()
            zip_download_images()
            st.success(f"✅ Evaluation images will be sent to {email}")
            # Your image generation or backend API call logic here
        else:
            st.warning("⚠️ Please enter an valid email ID before generating.")
            
def zip_download_images():
    # Step 1: Define folder to zip
    folder_path = "FTA Evaluation Image"  # 👈 replace with your folder path

    # Step 2: Zip the folder in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, folder_path))

    zip_buffer.seek(0)  # reset pointer to beginning
    
    # Generate filename with today's date
    filename = f"evaluation_images_{date.today().isoformat()}.zip"

    # Step 3: Offer download
    st.download_button(
        label="📦 Download Zipped Evaluation Images",
        data=zip_buffer,
        file_name=filename,
        mime="application/zip"
    )
        
def generate_eval_images():
    parentfolder = 'FTA Evaluation Image'
    viavifoldername = parentfolder + '/' + 'Viavi Installation evaluation image'
    juniperfoldername = parentfolder + '/' + 'Troubleshooting Evaluation Image'
    ericssonfoldername = parentfolder + '/' + 'Installation Evaluation Image'

    viavi = glob.glob(viavifoldername + '/valid/*.jpeg') + glob.glob(viavifoldername + '/invalid/*.jpeg')
    juniper = glob.glob(juniperfoldername + '/valid/*.jpeg') + glob.glob(juniperfoldername + '/invalid/*.jpeg')
    ericsson = glob.glob(ericssonfoldername + '/valid/*.jpeg') + glob.glob(ericssonfoldername + '/invalid/*.jpeg')

    print('~-'*5, 'Ericsson 6160 - Installation', '~-'*5)
    for item in ericsson : 
        print(item.split('\\')[1], end = ':')
        if '_valid-meta' in item.split('\\')[1] : 
            valid_update = modify_valid_metadata(item)
            print(valid_update['status'])
        if '_invalid-meta' in item.split('\\')[1] : 
            invalid_update = modify_invalid_metadata(item)
            print(invalid_update['status'])
    print('\n'+'~-'*5, 'Juniper Ex4300 - Troubleshooting', '~-'*5)
    for item in juniper : 
        print(item.split('\\')[1], end = ':')
        if '_valid-meta' in item.split('\\')[1] : 
            valid_update = modify_valid_metadata(item)
            print(valid_update['status'])
        if '_invalid-meta' in item.split('\\')[1] : 
            invalid_update = modify_invalid_metadata(item)
            print(invalid_update['status'])
    print('\n'+'~-'*5, 'Viavi 4G & 5G - Installation', '~-'*5)
    for item in viavi : 
        print(item.split('\\')[1], end = ':')
        if '_valid-meta' in item.split('\\')[1] : 
            valid_update = modify_valid_metadata(item)
            print(valid_update['status'])
        if '_invalid-meta' in item.split('\\')[1] : 
            invalid_update = modify_invalid_metadata(item)
            print(invalid_update['status'])
    print('~-'*25)