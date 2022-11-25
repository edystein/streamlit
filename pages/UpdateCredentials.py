import streamlit as st

from common.authentication import authenticate, update_authentication_file

# Title
st.sidebar.markdown("# Manage Credentials 🔑")
st.title("Manage Credentials 🔑")

# authentication
name, authentication_status, username, authenticator, b_authentication_ok = authenticate()

if b_authentication_ok:
    # update password
    try:
        if authenticator.reset_password(username, 'Reset password'):
            print('start save credentials')
            update_authentication_file(authenticator)
            print('end save credentials')
            st.success('Password modified successfully')
    except Exception as e:
        st.error(e)

    # update username & password
    try:
        if authenticator.update_user_details(username, 'Update user details'):
            update_authentication_file(authenticator)
            st.success('Entries updated successfully')

    except Exception as e:
        st.error(e)

    # forgot username
    try:
        username_forgot_username, email_forgot_username = authenticator.forgot_username('Forgot username')
        if username_forgot_username:
            st.success('Username sent securely')
            # Username to be transferred to user securely
        elif username_forgot_username == False:
            st.error('Email not found')
    except Exception as e:
        st.error(e)

    # register user
    if 'edy' == username:
        try:
            if authenticator.register_user('Register user', preauthorization=False):
                update_authentication_file(authenticator)
                st.success('User registered successfully')
        except Exception as e:
            st.error(e)
