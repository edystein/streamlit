import streamlit as st
import datetime
import yaml
from my_app import authenticator, config


st.markdown("# Page 2 ❄️")
st.sidebar.markdown("# Page 2 ❄️")

st.sidebar.markdown("# Register user")

try:
    if authenticator.register_user('Register user', preauthorization=False):
        with open('config_auth.yml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
        st.success('User registered successfully')
except Exception as e:
    st.error(e)



st.title('Counter Example')
if 'count' not in st.session_state:
    st.session_state.count = 0
    st.session_state.last_updated = datetime.time(0,0)

def update_counter():
    st.session_state.count += st.session_state.increment_value
    st.session_state.last_updated = datetime.datetime.now().time()

with st.form(key='my_form'):
    st.time_input(label='Enter the time', value=datetime.datetime.now().time(), key='update_time')
    st.number_input('Enter a value', value=0, step=1, key='increment_value')
    submit = st.form_submit_button(label='Update', on_click=update_counter)

st.write('Current Count = ', st.session_state.count)
st.write('Last Updated = ', st.session_state.last_updated)
