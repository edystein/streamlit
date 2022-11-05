import streamlit as st
import streamlit_authenticator as stauth
import yaml

from google.oauth2 import service_account
from google.cloud import storage

import pandas as pd
import numpy as np
from pages.TheBank import Bank
from common.authentication import authenticate


# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = storage.Client(credentials=credentials)

# authentication
name, authentication_status, user_name, authenticator, b_authentication_ok = authenticate()

st.markdown("# Main page 🎈")
st.sidebar.markdown("# Main page 🎈")

st.write("# Hello world:")
st.write("## Hello world 2")


df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})

option = st.selectbox(
    'Which number do you like best?',
    df['first column'])
st.write(f'option = {option}')

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])
    st.dataframe(chart_data)

st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))
st.table(dataframe)

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.line_chart(chart_data)

x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)
