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

st.set_page_config(page_title='Host Rooms', page_icon='https://cdn-icons-png.flaticon.com/512/2786/2786398.png', layout='wide', initial_sidebar_state='collapsed')

st.markdown(f"<h5 style='text-align: right; color: purple; font-family: Source Sans Pro; font-weight: 700'>👤{st.session_state.get('name', None)}</h5>", unsafe_allow_html=True)

st.title('🏠 Host Rooms')

with st.container():
    with st.form('host house'):
        col1, col2 = st.columns(2)

        with col1:
            room_name = st.text_input("Room Name", placeholder="Enter room name")
            bedrooms = st.number_input("Bedrooms", 1, 10)
            price = st.number_input("Price (In USD)", 1, 100000)
        with col2:
            location = st.text_input("Location", placeholder="Enter location") 
            bathrooms = st.number_input("Bathrooms", 1, 10)
            status = st.selectbox("Status", ["Available", "Booked"])

        url = st.text_area("Image URL", placeholder="Enter Image URL")

        book_submit = st.form_submit_button("Submit")
        
        if book_submit:
            if st.session_state.get('UID', None) is None:
                st.error("Please login to host rooms")
            else:
                if room_name and bedrooms and price and location and bathrooms and status and url:
                    mycursor.execute(f"INSERT INTO Rooms (owner_id, room_name, room_location, total_bedrooms, total_bathrooms, price, image_url, booking_status) VALUES ({st.session_state.get('UID', None)}, '{room_name}', '{location}', {bedrooms}, {bathrooms}, {price}, '{url}', '{status}')")
                    db.commit()
                    st.success("Room added successfully")
                else:
                    st.error("Please fill all fields")



with st.container():
    st.header("✍️ Change Room Status")
    with st.form('Change Room Status'):
        room_id = st.number_input("Room ID", 1, 100000)
        new_status = st.selectbox("Status", ["Available", "Booked"])

        book_submit = st.form_submit_button("Submit")
        
        if book_submit:
            if st.session_state.get('UID', None) is None:
                    st.error("Please login to change room status")
            else:
                mycursor.execute(f"SELECT * FROM Rooms WHERE id = {room_id} and owner_id = {st.session_state.get('UID', None)}")
                myresult = mycursor.fetchall()
                if myresult:
                    mycursor.execute(f"UPDATE Rooms SET booking_status = '{new_status}' WHERE id = {room_id} ")
                    db.commit()
                    st.success("Room status changed successfully")
                else:
                    st.error("You don't have aceess to change this room status")


with st.container():
    st.header('🔍 View Your Rooms')
    if st.button('View Rooms'):
        if st.session_state.get('UID', None) is None:
            st.error("Please login to view your rooms")
        else:
            mycursor.execute(f"SELECT * FROM Rooms WHERE owner_id = {st.session_state.get('UID', None)}")
            myresult = mycursor.fetchall()
            if myresult:
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
            else:
                st.error("You don't have any rooms")
                
                    
