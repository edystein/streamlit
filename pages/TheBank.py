import copy
from io import BytesIO

import pandas as pd
import streamlit as st
import yaml
import datetime
from google.cloud import storage
from google.oauth2 import service_account

from common import gcp_storage
from common.authentication import authenticate
import plotly.express as px


class Bank:
    """
    transactions schema: id, user, date, amount, action, remark, status, reviewer_name, review_date
    action: deposit, withdraw
    status: approved, rejected, pending
    transactions_datasets: transactions, pending_trans, rejected_trans
    """
    # Todo: transactions graph
    # Todo: transactions show tail

    def __init__(self, login_user):
        self.df_transactions = None
        self.df_2_approve = None
        self.user = login_user
        self.pages = ['Account Overview', 'Transaction', 'Admin']
        self.bucket_name = "streamlit-server-0"
        self.status = {'approved': 'Approved', 'pending': 'Pending'}

        with open('config_bank.yaml') as file:
            self.cfg = yaml.load(file, Loader=yaml.SafeLoader)
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"]
        )
        self.client = storage.Client(credentials=credentials)


    def get_pages(self):
        return self.pages

    def reset_bank(self):
        # backup current account
        self.save_data(backup=True)

        df_transactions = pd.DataFrame({'user': [],
                                        'date': [],
                                        'amount': [],
                                        'action': [],
                                        'remark': [],
                                        'status': [],
                                        'reviewer_name': [],
                                        'review_date': []})
        self.df_transactions = df_transactions
        self.df_2_approve = df_transactions
        self.save_data(backup=False)
        st.write('Reset Bank passed!!!!')

    def render_page(self, page):
        # self.reset_bank()
        self.load_data()
        st.write(f'Render {page}')
        if page == 'Account Overview':
            self.page_account_overview()
        elif page == 'Transaction':
            self.page_transaction()
        elif page == 'Admin':
            self.page_admin()

    def page_account_overview(self):
        st.title('Account overview')
        selected_username = st.selectbox('Select User', c_bank.get_user_list(login_user_name=self.user))
        st.sidebar.markdown(f"{selected_username}'s Account")

        st.title('Account:')
        df_trans = c_bank.get_transactions_by_user(user=selected_username, transactions=self.df_transactions)
        st.table(df_trans)

        fig = px.line(df_trans, x="date", y="Balance", title=f'{selected_username} Account')
        # fig.show()
        st.plotly_chart(fig, use_container_width=True)

        st.title('Pending transactions:')
        st.table(c_bank.get_transactions_by_user(user=selected_username, transactions=self.df_2_approve))





    def page_transaction(self):
        st.title("Transaction")
        selected_user = st.selectbox('User', c_bank.get_user_list(login_user_name=self.user))

        trans_type = st.radio(
            "Transaction type",
            ('Withdraw', 'Deposit'))
        trans_sum = st.number_input('Insert sum', min_value=0, max_value=5000, step=100)
        trans_note = st.text_area('Note')

        if st.button("Set Transaction"):
            st.balloons()
            if self.is_admin():
                df_new_trans = pd.DataFrame({'user': [selected_user],
                                             'date': [datetime.datetime.now().strftime("%y-%m-%d")],
                                             'amount': [trans_sum],
                                             'action': [trans_type],
                                             'remark': [trans_note],
                                             'status': [self.status['approved']],
                                             'reviewer_name': [self.user],
                                             'review_date': [datetime.datetime.now().strftime("%y-%m-%d")]})

                if self.df_transactions.shape[0]:
                    self.df_transactions = pd.concat([self.df_transactions, df_new_trans])
                else:
                    self.df_transactions = copy.deepcopy(df_new_trans)
            else:
                df_new_trans = pd.DataFrame({'user': [selected_user],
                                             'date': [datetime.datetime.now().strftime("%y-%m-%d")],
                                             'amount': [trans_sum],
                                             'action': [trans_type],
                                             'remark': [trans_note],
                                             'status': [self.status['pending']],
                                             'reviewer_name': [self.status['pending']],
                                             'review_date': [self.status['pending']]})
                if self.df_2_approve.shape[0]:
                    self.df_2_approve = pd.concat([self.df_2_approve, df_new_trans])
                else:
                    self.df_2_approve = copy.deepcopy(df_new_trans)
            self.save_data()

    def page_admin(self):
        """
        Approve transactions
        manage users
        reset dataset

        """
        if not self.is_admin():
            st.write('Not an admin yet.\nCome back later\n🌼')
            return
        # approve transactions
        st.header('Transactions to Approve')
        if self.df_2_approve.shape[0]:
            st.table(self.df_2_approve[:1])
            st.button('Approve 👍', on_click=self._transaction_approve_true)
            st.button('Don\'t approve 👎', on_click=self._transaction_approve_false)
        else:
            st.write('No transactions to approve you\'re all set')

        # reset dataset
        st.title('\n\n\nReset Dataset:')
        if st.button('Reset Dataset'):
            self.reset_bank()

    def _transaction_approve_true(self):
        self._transaction_approve(b_approve=True)

    def _transaction_approve_false(self):
        self._transaction_approve(b_approve=False)

    def _transaction_approve(self, b_approve):
        st.write(f'b_approve: {b_approve}')
        # update new transaction
        if b_approve:
            df_new_trans = copy.deepcopy(self.df_2_approve[:1])
            df_new_trans['status'] = self.status['approved']
            df_new_trans['reviewer_name'] = self.user
            df_new_trans['review_date'] = datetime.datetime.now().strftime("%y-%m-%d")

            if self.df_transactions.shape[0]:
                self.df_transactions = pd.concat([self.df_transactions, df_new_trans])
            else:
                self.df_transactions = copy.deepcopy(df_new_trans)
        # update approve list
        self.df_2_approve = self.df_2_approve[1:]

        self.save_data()

    def is_admin(self):
        return self.user in self.cfg['admin']


    def get_user_list(self, login_user_name):
        if login_user_name in self.cfg['admin']:
            return [login_user_name] + [user for user in self.cfg['view'] if user != login_user_name]
        else:
            return [login_user_name]

    def load_data(self):
        with st.spinner('Loading Data...'):
            self.df_transactions = pd.read_pickle(BytesIO(
                gcp_storage.read_file(client=self.client,
                                      bucket_name=self.bucket_name,
                                      file_path=self.cfg['data']['transactions'],
                                      b_decode_as_string=False)))
            self.df_2_approve = pd.read_pickle(BytesIO(
                gcp_storage.read_file(client=self.client,
                                      bucket_name=self.bucket_name,
                                      file_path=self.cfg['data']['transactions_2_approve'],
                                      b_decode_as_string=False)))

    def save_data(self, backup=False):
        with st.spinner('Saving Data....'):
            str_date = datetime.datetime.now().strftime('%m-%d-%Y')
            if backup:
                file_path = f"{self.cfg['data']['backup_transactions']}-{str_date}.pkl"
            else:
                file_path = self.cfg['data']['transactions']
            gcp_storage.write_df(client=self.client,
                                 bucket_name=self.bucket_name,
                                 file_path=file_path,
                                 df=self.df_transactions)

            if backup:
                file_path = f"{self.cfg['data']['backup_transactions_2_approve']}-{str_date}.pkl"
            else:
                file_path = self.cfg['data']['transactions_2_approve']
            gcp_storage.write_df(client=self.client,
                                 bucket_name=self.bucket_name,
                                 file_path=file_path,
                                 df=self.df_2_approve)

    def get_transactions_by_user(self, user, transactions):
        df_trans = copy.deepcopy(transactions[transactions['user'] == user])
        df_trans['Balance'] = df_trans['amount']
        df_trans.loc[df_trans['action'] == 'Withdraw', ['Balance']] = \
            df_trans.loc[df_trans['action'] == 'Withdraw', ['Balance']] * -1
        df_trans['Balance'] = df_trans['Balance'].cumsum()
        df_trans = df_trans[['user', 'date', 'amount', 'action', 'Balance', 'remark', 'status', 'reviewer_name',
                             'review_date']]
        return df_trans


# Title
st.sidebar.markdown("# The Bank 🏦")
st.title("The Bank 🏦")

# authentication
name, authentication_status, user_name, authenticator, b_authentication_ok = authenticate()

if b_authentication_ok:
    c_bank = Bank(login_user=user_name)
    selected_page = st.sidebar.selectbox("Select a page", c_bank.get_pages())
    c_bank.render_page(page=selected_page)
