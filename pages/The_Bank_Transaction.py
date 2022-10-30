import pandas as pd
import streamlit as st
from google.cloud import storage
from google.oauth2 import service_account

import yaml
from io import BytesIO, StringIO
from common.gcp_storage import read_file
from common.authentication import authenticate
from pages.The_Bank_Overview import Bank

# Title
st.sidebar.markdown("# The Bank 🏦 Transactions")
st.title("The Bank 🏦 Transactions")

# authentication
# login authentication
name, authentication_status, user_name, authenticator = authenticate()

b_authn_ok = False
if authentication_status:
    authenticator.logout('Logout', 'main')
    try:
        st.write(f'Welcome {name}')
        b_authn_ok = True
    except TypeError:
        st.write(f'NAME WAS MISSING. Please re-authenticate.')
elif not authentication_status:
    st.error('user_name/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your user_name and password')

if b_authn_ok:
    c_bank = Bank()

    # set transaction
    st.header("Set transaction")
    trans_type = st.radio(
        "Transaction type",
        ('Withdraw', 'Deposit'))
    trans_sum = st.number_input('Insert sum', min_value=0, max_value=5000, step=100)
    trans_note = st.text_area('Note')
    trans_set = st.button("Set Transaction")

    if trans_set:
        st.write('set transaction')
