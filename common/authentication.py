import streamlit as st
import streamlit_authenticator as stauth
import yaml


# login authentication
def authenticate():
    with open('config_auth.yml') as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    name, authentication_status, user_name = authenticator.login('Login', 'main')

    # Authentication status
    b_authentication_ok = False
    if authentication_status:
        authenticator.logout('Logout', 'main')
        try:
            st.write(f'Welcome {name}')
            b_authentication_ok = True
        except TypeError:
            st.write(f'NAME WAS MISSING. Please re-authenticate.')
    elif not authentication_status:
        st.error('user_name/password is incorrect')
    elif authentication_status is None:
        st.warning('Please enter your user_name and password')

    return name, authentication_status, user_name, authenticator, b_authentication_ok

