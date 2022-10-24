import streamlit as st
import streamlit_authenticator as stauth
import yaml

import pandas as pd
import numpy as np


# login authentication
with open('config_auth.yml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)


name, authentication_status, username = authenticator.login('Login', 'main')
st.write(f'authentication_status: {authentication_status}')
st.write(f'type(name): {type(name)}')
if authentication_status:
    authenticator.logout('Logout', 'main')
    try:
        st.write(f'Welcome *{name}*')
    except TypeError:
        st.write(f'NAME WAS MISSING.')
    st.title('Some content')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')





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
    st.dataframe( chart_data)


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