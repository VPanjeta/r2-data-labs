import time
import streamlit as st
import openai
import os
from utils.maps import MapsManager
import streamlit_authenticator as stauth
from utils.base_messages import *


openai.api_key = os.getenv("OPENAI_API_KEY")
maps_manager = MapsManager()


base_messages = GPT_BASE_MESSAGES

st.set_page_config(page_title="GridGuru!", page_icon=":earth_americas:", initial_sidebar_state="auto", menu_items=None, layout="wide")

hide_streamlit_style = """<style>
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.sidebar.title("Location Analyser Options")
st.sidebar.markdown('---')


st.title("GridGuru: Mastering the Art of Power Analysis!")
st.markdown('---')

location_name = st.text_input("Location", "Bangalore")

power_grid = st.sidebar.checkbox("Evaluate location for new power grid", value=True)
nearby_locations = st.sidebar.checkbox("Find better nearby locations for power grid placement", value=True)
heat_waves = st.sidebar.checkbox("Evaluate heat wave related power issues in the given location", value=True)
natural_disasters = st.sidebar.checkbox("Details of disasters that have affected power usage and delivery in the past", value=True)
untapped_renewable_energy_sites = st.sidebar.checkbox("Details of untapped renewable energy sites near the given location", value=True)


def get_total_message(inp):
    return [
        { 'message': base_messages['power_grid'] + [{"role": "user", "content": f"{inp}"}] if power_grid else [], 'type': 'power_grid' },
        { 'message': base_messages['nearby_locations'] + [{"role": "user", "content": f"{inp}"}] if nearby_locations else [], 'type': 'nearby_locations' },
        { 'message': base_messages['heat_waves'] + [{"role": "user", "content": f"{inp}"}] if heat_waves else [], 'type': 'heat_waves' },
        { 'message': base_messages['natural_disasters'] + [{"role": "user", "content": f"{inp}"}] if natural_disasters else [], 'type': 'natural_disasters' },
        { 'message': base_messages['untapped_renewable_energy_sites'] + [{"role": "user", "content": f"{inp}"}] if untapped_renewable_energy_sites else [], 'type': 'untapped_renewable_energy_sites' }
    ]

def predict(inp, res_box):
    input_messages = get_total_message(inp)
    response = ""

    for input_message in input_messages:
        if input_message['message'] == []:
            continue

        for completion in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=input_message['message'],
            stream=True
        ):
            if 'content' in completion.choices[0].delta:
                response += completion.choices[0].delta.content
                res_box.markdown(response, unsafe_allow_html=True)

    return response


col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    assess_button = st.button("Analyze Location", type="primary", use_container_width=True)

with col2:
    reset_button = st.button("Reset Data", use_container_width=True)
    if reset_button:
        st.experimental_rerun()

if assess_button:

    if not (power_grid or nearby_locations or heat_waves or natural_disasters or untapped_renewable_energy_sites):
        st.error("Please select at least one option from the sidebar")

    else:

        st.markdown('---')
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Location Image")
            with st.spinner("Analysing map terrain.."):
                st.image(maps_manager.get_location_image(location_name, zoom=10), use_column_width=True)
                time.sleep(2)
            st.markdown('----')
            st.markdown("#### Satellite Image")
            with st.spinner("Analysing satellite image.."):
                st.image(maps_manager.get_location_image(location_name, zoom=10, type='hybrid'), use_column_width=True)
                time.sleep(2)
            st.markdown("#### Nearby locations' Terrain")
            with st.spinner("Analysing Nearby Terrain.."):
                st.image(maps_manager.get_location_image(location_name, zoom=8), use_column_width=True)
                time.sleep(2)
            st.success("Analysis complete! Results and details available in the right column. "
                        "Scroll up to see the results.")
            st.markdown('----')

        with col2:
            res_box = st.empty()
            response = predict(location_name, res_box)

            if response.strip() == "":
                st.error("Something went wrong while analysing data.")

            location_name = st.empty()
            assess_button = st.empty()
            reset_button = st.button("Check another location", type="primary")

if reset_button:
    st.experimental_rerun()


