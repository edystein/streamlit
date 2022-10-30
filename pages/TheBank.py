import pandas as pd
import streamlit as st
from google.cloud import storage
from google.oauth2 import service_account

import yaml
from io import BytesIO, StringIO
from common.gcp_storage import read_file
from common.authentication import authenticate


class Bank:
    """
    transactions schema: id, user, date, amount, action, remark, status, reviewer_name, review_date
    action: deposit, withdraw
    status: approved, rejected, pending
    transactions_datasets: transactions, pending_trans, rejected_trans
    """

    def __init__(self, login_user):
        self.user = login_user
        self.pages = ['Account Overview', 'Transaction', 'Admin']
        with open('config_bank.yaml') as file:
            self.cfg = yaml.load(file, Loader=yaml.SafeLoader)
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"]
        )
        self.client = storage.Client(credentials=credentials)

        # if mode == 'view':
        #     self.transactions = pd.read_pickle(BytesIO(
        #         read_file(client=self.client, bucket_name=bucket_name, file_path=file_path, b_decode_as_string=False)))
        #     print(self.transactions)
        #     #     try to dump df
        #     bucket = self.client.bucket(bucket_name)
        #     with bucket.blob('bank/ztest_transactions.pkl').open(mode='wb') as fid:
        #         self.transactions.to_pickle(fid)
        #     print('Finished write test')

    def get_pages(self):
        return self.pages

    def render_page(self, page):
        st.write(f'Render {page}')
        if page == 'Account Overview':
            self.page_account_overview()
        elif page == 'Transaction':
            self.page_transaction()

    def page_account_overview(self):
        st.title('Account overview')
        selected_username = st.selectbox('Select User', c_bank.get_user_list(login_user_name=self.user))
        st.sidebar.markdown(f"{selected_username}'s Account")
        # load transactions
        bucket_name = "streamlit-server-0"
        file_path = 'bank/transactions.pkl'
        transactions = pd.read_pickle(BytesIO(
            read_file(client=self.client, bucket_name=bucket_name, file_path=file_path, b_decode_as_string=False)))

        st.table(c_bank.get_transactions_by_user(user=selected_username, transactions=transactions))

    def page_transaction(self):
        st.title("Transaction")
        trans_type = st.radio(
            "Transaction type",
            ('Withdraw', 'Deposit'))
        trans_sum = st.number_input('Insert sum', min_value=0, max_value=5000, step=100)
        trans_note = st.text_area('Note')
        trans_set = st.button("Set Transaction")

        if trans_set:
            st.write('set transaction')



    def get_user_list(self, login_user_name):
        if login_user_name in self.cfg['admin']:
            return [login_user_name] + [user for user in self.cfg['view'] if user != login_user_name]
        else:
            return [login_user_name]

    def load_data(self):
        # load cfg
        # load datasets
        pass

    def get_transactions_by_user(self, user, transactions):
        return transactions[transactions['user'] == user]


# Title
st.sidebar.markdown("# The Bank 🏦")
st.title("The Bank 🏦")

# authentication
name, authentication_status, user_name, authenticator, b_authentication_ok = authenticate()

if b_authentication_ok:
    c_bank = Bank(login_user=user_name)
    selected_page = st.sidebar.selectbox("Select a page", c_bank.get_pages())
    c_bank.render_page(page=selected_page)
