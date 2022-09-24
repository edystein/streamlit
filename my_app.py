import streamlit as st
import pandas as pd

# bypass user, pwd DB
def create_usertable():
    return

def make_hashes(password):
    return password

def check_hashes(password, hashed_pswd):
    return True


def login_user(user_name, hashed_pwd):
    True

def view_all_users():
    return ''

def add_userdata(username,password):
    return True


st.title("Simple Login App")

menu = ["Home", "Login", "SignUp"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.subheader("Home")

elif choice == "Login":
    st.subheader("Login Section")

username = st.sidebar.text_input("User Name")
password = st.sidebar.text_input("Password", type='password')
if st.sidebar.checkbox("Login"):
    # if password == '12345':
    create_usertable()
    hashed_pswd = make_hashes(password)

    result = login_user(username, check_hashes(password, hashed_pswd))
    if result:

        st.success("Logged In as {}".format(username))

        task = st.selectbox("Task", ["Add Post", "Analytics", "Profiles"])
        if task == "Add Post":
            st.subheader("Add Your Post")

        elif task == "Analytics":
            st.subheader("Analytics")
        elif task == "Profiles":
            st.subheader("User Profiles")
            user_result = view_all_users()
            clean_db = pd.DataFrame(user_result, columns=["Username", "Password"])
            st.dataframe(clean_db)
    else:
        st.warning("Incorrect Username/Password")

elif choice == "SignUp":
    st.subheader("Create New Account")
    new_user = st.text_input("Username", key='1')
    new_password = st.text_input("Password", type='password', key='2')

    if st.button("Signup"):
        create_usertable()
        add_userdata(new_user, make_hashes(new_password))
        st.success("You have successfully created a valid Account")
        st.info("Go to Login Menu to login")
