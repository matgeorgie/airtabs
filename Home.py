import mysql.connector
from time import sleep
import streamlit as st

db = mysql.connector.connect(**st.secrets.db_credentials)

mycursor = db.cursor()

UID = None

st.set_page_config(page_title='AirTabs', page_icon='https://cdn-icons-png.flaticon.com/512/2786/2786398.png', layout='wide', initial_sidebar_state='collapsed')

st.title('Welcome to AirTabs 🌎')
st.markdown('👉 AirTabs is a simple, secure platform for booking rooms in the cloud')

with st.container():
    with st.form("sign in"):
        st.header('🔓 Sign in')
        email = st.text_input('Email', placeholder='Enter your email')
        passwd = st.text_input('Password', placeholder='Enter your Password', type = 'password')
        signin_submit = st.form_submit_button("Sign in")
        
        if signin_submit:
            if email and passwd:
                mycursor.execute(f"SELECT * FROM Users WHERE email = '{email}' AND passwd = md5('{passwd}')")
                myresult = mycursor.fetchall()
                if myresult:
                    UID = myresult[0][0]
                    st.success(f'✅ Sign in Successful!')
                    st.info(f'👋 Welcome {myresult[0][1]}')
                    st.session_state['UID'] = UID
                    st.session_state['name'] = myresult[0][1]
                else:
                    st.error(f'🔴 Invalid credentials')
                    st.info(f'🟢 Sign up for an account')
            else:
                st.error(f'🔴 Please fill in all fields')

with st.container():
    with st.form("create account"):
        st.header('📝 Create Account')
        name = st.text_input('Name', placeholder='Enter your name')
        email_c = st.text_input('Email ID', placeholder='Enter your email')
        passwd_c = st.text_input('Password', placeholder='Enter your password', type = 'password')
        country = st.text_input('Country', placeholder='Enter your country Code')

        signup_submit = st.form_submit_button("Sign up")

        if signup_submit:
            if email_c and passwd_c and name and country:
                if len(country) > 3:
                    mycursor.execute(f"SELECT * FROM Users WHERE email = '{email_c}'")
                    myresult = mycursor.fetchall()
                    if myresult == []:
                        mycursor.execute(f"INSERT INTO Users (name, email, passwd, country) VALUES ('{name}', '{email_c}', md5('{passwd_c}'), '{country}')")
                        db.commit()
                        mycursor.execute(f"SELECT * FROM Users WHERE email = '{email_c}'")
                        myresult = mycursor.fetchall()
                        with st.spinner('Creating account...'):
                            sleep(3)
                        st.success(f'🟢 Signup Successful. Welcome {myresult[0][1]}')
                        UID = myresult[0][0]
                        st.info(f'🔴 Login to access your account')
                    else:
                        st.error(f'🔴 Email already exists')
                else:
                    st.error(f'🔴 Invalid country code')
            else:
                st.error(f'🔴 Please fill in all fields')

with st.container():
    with st.form("logout"):
        st.header("🔐 Logout")
        logout_submit = st.form_submit_button("Logout")
        if logout_submit:
            if st.session_state.get('UID', None):
                del st.session_state['UID']
                del st.session_state['name']
                st.success(f'🟢 Logout Successful')
            else:
                st.error(f'🔴 You are not logged in')