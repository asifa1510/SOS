import streamlit as st
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.location import get_location

st.set_page_config(page_title="Emergency SOS", page_icon="🚨")
st.title("🚨 Emergency SOS")

st.markdown("Click the panic button to instantly send your live location to your emergency contact.")

if st.button("🔴 Send Panic Alert"):
    lat, lon = get_location()
    if lat and lon:
        with st.spinner("Sending SOS..."):
            res = requests.post(
                st.secrets["api_url"],
                json={"latitude": lat, "longitude": lon}
            )
            if res.status_code == 200:
                st.success("✅ SOS Sent Successfully!")
            else:
                st.error("❌ Failed to send alert.")
    else:
        st.warning("Could not fetch location.")
