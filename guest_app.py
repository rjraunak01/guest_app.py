import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Hotel CRM System", layout="wide")

# ---------------- DATABASE ---------------- #

conn = sqlite3.connect("hotel.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS guests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    mobile TEXT,
    category TEXT,
    visit_date TEXT,
    staff_name TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guest_name TEXT,
    mobile TEXT,
    rating INTEGER,
    service TEXT,
    food TEXT,
    behaviour TEXT,
    comment TEXT,
    date TEXT
)
""")

conn.commit()

# ---------------- PAGE CONTROL ---------------- #

page = st.query_params.get("page", "entry")

# ---------------- GUEST ENTRY ---------------- #

def guest_entry():

    st.title("📝 Guest Entry Form")

    name = st.text_input("Guest Name")
    mobile = st.text_input("Mobile Number")
    category = st.selectbox("Category", ["Room Booking", "Banquet", "Restaurant", "Other"])
    staff = st.text_input("Staff Name (Who is entering)")

    if st.button("Submit Entry"):
        if name and mobile and staff:
            c.execute("""
            INSERT INTO guests (name, mobile, category, visit_date, staff_name)
            VALUES (?, ?, ?, ?, ?)
            """, (name, mobile, category, datetime.now().date(), staff))
            conn.commit()
            st.success("Entry Saved Successfully ✅")
        else:
            st.error("Please fill all fields")

# ---------------- FEEDBACK ---------------- #

def feedback_page():

    st.title("⭐ Guest Feedback Form")

    guest_name = st.text_input("Guest Name")
    mobile = st.text_input("Mobile Number")

    rating = st.slider("Overall Rating", 1, 5)

    service = st.selectbox("Service Quality", ["Excellent", "Good", "Average", "Poor"])
    food = st.selectbox("Food Quality", ["Excellent", "Good", "Average", "Poor"])
    behaviour = st.selectbox("Staff Behaviour", ["Excellent", "Good", "Average", "Poor"])

    comment = st.text_area("Additional Comments")

    if st.button("Submit Feedback"):
        if guest_name and mobile:
            c.execute("""
            INSERT INTO feedback 
            (guest_name, mobile, rating, service, food, behaviour, comment, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (guest_name, mobile, rating, service, food, behaviour, comment, datetime.now().date()))
            conn.commit()
            st.success("Thank You For Your Feedback ❤️")
        else:
            st.error("Please fill required fields")

# ---------------- ADMIN PANEL ---------------- #

def admin_panel():

    st.title("🔐 Admin Login")

    password = st.text_input("Enter Admin Password", type="password")

    if password == "admin123":

        st.success("Login Successful ✅")

        st.subheader("📅 Today Bookings")

        today = pd.read_sql_query("""
        SELECT * FROM guests
        WHERE visit_date = date('now')
        """, conn)

        st.dataframe(today)

        st.subheader("📊 Booking Category Summary")

        cat = pd.read_sql_query("""
        SELECT category, COUNT(*) as total_bookings
        FROM guests
        GROUP BY category
        """, conn)

        st.dataframe(cat)

        st.subheader("🔁 Repeat Guests")

        repeat = pd.read_sql_query("""
        SELECT name, mobile, COUNT(*) as visits
        FROM guests
        GROUP BY mobile
        HAVING visits > 1
        """, conn)

        st.dataframe(repeat)

        st.subheader("👨‍💼 Staff Wise Entries")

        staff_data = pd.read_sql_query("""
        SELECT staff_name, COUNT(*) as total_entries
        FROM guests
        GROUP BY staff_name
        """, conn)

        st.dataframe(staff_data)

        st.subheader("⭐ All Feedback")

        feedback_data = pd.read_sql_query("""
        SELECT * FROM feedback
        """, conn)

        st.dataframe(feedback_data)

    elif password != "":
        st.error("Wrong Password ❌")

# ---------------- ROUTING ---------------- #

if page == "feedback":
    feedback_page()

elif page == "admin":
    admin_panel()

else:
    guest_entry()

# ---------------- FOOTER LINKS ---------------- #

st.markdown("---")
st.markdown("### Quick Links")
st.markdown("[Guest Entry](?page=entry)")
st.markdown("[Feedback Form](?page=feedback)")
st.markdown("[Admin Panel](?page=admin)")