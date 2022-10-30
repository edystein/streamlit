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
    return name, authentication_status, user_name, authenticator
