from datetime import date
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

st.set_page_config(page_title='Book Rooms', page_icon='https://cdn-icons-png.flaticon.com/512/2786/2786398.png', layout='wide', initial_sidebar_state='collapsed')

st.markdown(f"<h5 style='text-align: right; color: purple; font-family: Source Sans Pro; font-weight: 700'>👤{st.session_state.get('name', None)}</h5>", unsafe_allow_html=True)

st.title('🔑 Book Rooms')

with st.container():
    with st.form("Book Rooms"):
        col1, col2 = st.columns(2)

        with col1:
            room_id = st.text_input("Room ID", placeholder="Enter room ID")
            check_in = st.date_input("Reservation Period", value = (date(2022,8,8), date(2022,12,12)))

        with col2:
            guests = st.number_input("Guests", 1, 10)
            
            try:
                mycursor.execute(f"SELECT * FROM Rooms WHERE id = {room_id}")
                myresult = mycursor.fetchall()
            except:
                st.write()
            else:
                st.markdown("#")
                price = st.subheader(f"💲Price: ${myresult[0][6]}")
        

        book_submit = st.form_submit_button("Book")

        if book_submit:
            if st.session_state.get('UID', None) is None:
                st.error("Please login to book rooms")
            else:
                if room_id and check_in and guests:
                    mycursor.execute(f"SELECT * FROM Rooms WHERE id = {room_id} and booking_status = 'Available'")
                    myresult = mycursor.fetchall()

                    if myresult:
                        mycursor.execute(f"INSERT INTO Bookings (guest_id, room_id, guests, check_in, checkout, booking_status) VALUES ({UID}, {room_id}, {guests}, '{check_in[0]}', '{check_in[1]}', 'Booked')")
                        db.commit()
                        mycursor.execute(f"UPDATE Rooms SET booking_status = 'Booked' WHERE id = {room_id}")
                        db.commit()
                        st.success("✅ Booking successful")
                        
                    else:
                        st.error("🔴 Room not available")
                else:
                    st.error("🔴 Please fill in all fields")


with st.container():
    st.header('🔍 View Rooms')
    mycursor.execute(f"SELECT * FROM Rooms where booking_status = 'Available'")
    myresult = mycursor.fetchall()
    for x in myresult:
        st.subheader(f"{x[2]}")
        components.html(f"""
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
            <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
            <div class="card text-bg-dark mb-3">
                <p></p>
                <p style="text-align:center;">
                    <img src="{x[7]}" class="img-fluid rounded float-start"  width = 500  alt="...">
                </p>
                <div class="card-body">
                    <h5 class="card-title">🆔 Room ID: {x[0]}</h5>
                    <ul class="list-group list-group-horizontal">
                    <li class="list-group-item">📍 Location: {x[3]}</li>
                    <li class="list-group-item">🛏️ Bedrooms: {x[4]}</li>
                    <li class="list-group-item">🚽 Bathrooms: {x[5]}</li>
                    <li class="list-group-item"><strong>💰 Price: ${x[6]}</strong></li>
                    </ul>
                </div>
            </div>
            """, height=645)


