import mysql.connector
import streamlit as st
import streamlit.components.v1 as components

db = mysql.connector.connect(
    host='remotemysql.com',
    user='gMZazGoWlk',
    passwd='07OOXPIcI9',
    database='gMZazGoWlk',
    port = 3306
    )
    
mycursor = db.cursor()

UID = st.session_state.get('UID', None)

st.set_page_config(page_title='Bookings', page_icon='https://cdn-icons-png.flaticon.com/512/2786/2786398.png', layout='wide', initial_sidebar_state='collapsed')

st.markdown(f"<h5 style='text-align: right; color: black; font-family: Source Sans Pro; font-weight: 600'>⭕ {st.session_state.get('name', '')}</h5>", unsafe_allow_html=True)

st.title('🎟️ Check Bookings')

with st.container():
    if st.session_state.get('UID', None) is None:
        st.error("Please login to check bookings")
    else:
        mycursor.execute(f"SELECT * FROM Bookings WHERE guest_id = {st.session_state.get('UID', None)}")
        myresult = mycursor.fetchall()
        if myresult:
            for x in myresult:
                st.subheader(f"Booking ID: {x[0]}")
                components.html(f"""
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
                    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
                    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
                    <div class="card text-bg-dark mb-3">
                        <div class="card-body">
                            <ul class="list-group list-group-horizontal">
                            <li class="list-group-item">🆔 Room ID: {x[2]}</li>
                            <li class="list-group-item">👩🏻‍🤝‍👨🏻 Guests: {x[3]}</li>
                            <li class="list-group-item">📅 Check-in Date: {x[4]}</li>
                            <li class="list-group-item">📆 Checkout Date: {x[5]}</li>
                            <li class="list-group-item"><strong>✅ Booking Status: {x[6]}</strong></li>
                            </ul>
                        </div>
                    </div>
                    """, height=300)
        else:
            st.error("You have no bookings")
