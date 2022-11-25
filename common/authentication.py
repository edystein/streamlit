import json

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from google.cloud import storage
from google.oauth2 import service_account

from common import gcp_storage


# login authentication
def authenticate():
    # read cfg file from GCP
    credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
    client = storage.Client(credentials=credentials)

    with open('config_bank.yaml') as file:
        cfg = yaml.load(file, Loader=yaml.SafeLoader)

    auth_cfg = json.loads(gcp_storage.read_file(client=client,
                                                bucket_name=cfg['data']['bucket_name'],
                                                file_path=cfg['data']['authentication'],
                                                b_decode_as_string=True))
    authenticator = stauth.Authenticate(
        auth_cfg['credentials'],
        auth_cfg['cookie']['name'],
        auth_cfg['cookie']['key'],
        auth_cfg['cookie']['expiry_days'],
        auth_cfg['preauthorized']
    )
    name, authentication_status, user_name = authenticator.login('Login', 'main')

    # Authentication status
    b_authentication_ok = False
    if authentication_status:
        authenticator.logout('Logout', 'main')
        try:
            st.write(f'Hello {name}')
            b_authentication_ok = True
        except TypeError:
            st.write(f'NAME WAS MISSING. Please re-authenticate.')
    elif not authentication_status:
        st.error('user_name/password is incorrect')
    elif authentication_status is None:
        st.warning('Please enter your user_name and password')

    return name, authentication_status, user_name, authenticator, b_authentication_ok


def update_authentication_file(authenticator):
    auth_cfg = {
        'credentials': authenticator.credentials,
        'preauthorized': authenticator.preauthorized,
        'cookie': {
            'name': authenticator.cookie_name,
            'key': authenticator.key,
            'expiry_days': authenticator.cookie_expiry_days
        }
    }
    with open('config_bank.yaml') as file:
        cfg = yaml.load(file, Loader=yaml.SafeLoader)

    gcp_storage.write_txt(data=json.dumps(auth_cfg), file_path=cfg['data']['authentication'])
