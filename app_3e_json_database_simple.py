"""
🗄️ SIMPLE JSON DATABASE
Add, view, and delete records in a JSON file
"""

import streamlit as st
import json
import os

st.set_page_config(page_title="🗄️ Simple JSON Database", page_icon="🗄️")
st.title("🗄️ Simple JSON Database")

DB_FILE = "my_db.json"

# Load database
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            db = json.load(f)
        except Exception:
            db = []
else:
    db = []

name = st.text_input("Name")
age = st.number_input("Age", min_value=0, max_value=120, step=1)
email = st.text_input("Email")

if st.button("Add Record"):
    db.append({"name": name, "age": age, "email": email})
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)
    st.success(f"Added record for {name}")
    st.rerun()

st.header("Records")
if db:
    for i, record in enumerate(db):
        st.write(f"{record}")
        if st.button(f"Delete {record['name']}", key=f"del_{i}"):
            db.pop(i)
            with open(DB_FILE, "w", encoding="utf-8") as f:
                json.dump(db, f, indent=2)
            st.warning(f"Deleted record {record['name']}")
            st.rerun()
else:
    st.info("No records yet.")
