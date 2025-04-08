import streamlit as st
import mysql.connector
from db_connection import get_db_connection
import pandas as pd

# Page Configuration
st.set_page_config(page_title="EHR Management System", layout="wide")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose a page", ["Home", "Patients", "Appointments", "Medical Records"])

# Database Connection
connection = get_db_connection()

# Stop the app if the connection fails
if connection is None:
    st.error("Failed to connect to the database. Please check your MySQL server and credentials.")
    st.stop()

# Home Page
if page == "Home":
    st.title("Welcome to the EHR Management System")
    st.write("Manage patient records, appointments, and medical history efficiently.")

# Patients Page
elif page == "Patients":
    st.title("Patient Management")

    # Add New Patient
    with st.form("add_patient_form"):
        st.subheader("Add New Patient")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        date_of_birth = st.date_input("Date of Birth")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        contact_number = st.text_input("Contact Number")
        email = st.text_input("Email")
        address = st.text_area("Address")
        submit_button = st.form_submit_button("Add Patient")

        if submit_button:
            cursor = connection.cursor()
            query = """
                INSERT INTO patients (first_name, last_name, date_of_birth, gender, contact_number, email, address)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (first_name, last_name, date_of_birth, gender, contact_number, email, address)
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            st.success("Patient added successfully!")

    # Remove Patient
    st.subheader("Remove Patient")
    patient_id_to_remove = st.number_input("Enter Patient ID to Remove", min_value=1, step=1)
    remove_button = st.button("Remove Patient")

    if remove_button:
        cursor = connection.cursor()
        
        # Check if patient exists
        cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id_to_remove,))
        patient = cursor.fetchone()
        
        if patient:
            # First, delete associated appointments
            cursor.execute("DELETE FROM appointments WHERE patient_id = %s", (patient_id_to_remove,))
            connection.commit()
            
            # Now delete the patient
            cursor.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id_to_remove,))
            connection.commit()
            
            st.success(f"Patient ID {patient_id_to_remove} and their appointments have been removed successfully.")
        else:
            st.warning("No patient found with that ID.")
        
        cursor.close()


# Appointments Page
elif page == "Appointments":
    st.title("Appointment Management")

    # Cancel Appointment
    st.subheader("Cancel Appointment")
    appointment_id_to_cancel = st.number_input("Enter Appointment ID to Cancel", min_value=1, step=1)
    cancel_button = st.button("Cancel Appointment")

    if cancel_button:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM appointments WHERE appointment_id = %s", (appointment_id_to_cancel,))
        appointment = cursor.fetchone()
        if appointment:
            cursor.execute("UPDATE appointments SET status = 'Cancelled' WHERE appointment_id = %s", (appointment_id_to_cancel,))
            connection.commit()
            st.success(f"Appointment ID {appointment_id_to_cancel} has been cancelled.")
        else:
            st.warning("No appointment found with that ID.")
        cursor.close()

# Medical Records Page
elif page == "Medical Records":
    st.title("Medical Records Management")
    st.subheader("Add Medical Record")

    with st.form("add_medical_record_form"):
        patient_id = st.number_input("Patient ID", min_value=1)
        diagnosis = st.text_area("Diagnosis")
        treatment = st.text_area("Treatment")
        prescription = st.text_area("Prescription")
        notes = st.text_area("Additional Notes")
        submit_button = st.form_submit_button("Add Record")

        if submit_button:
            cursor = connection.cursor()
            query = """
                INSERT INTO medical_records (patient_id, diagnosis, treatment, prescription, notes)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (patient_id, diagnosis, treatment, prescription, notes)
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            st.success("Medical record added successfully!")

    # View Medical Records
    st.subheader("Medical Records List")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM medical_records")
    records = cursor.fetchall()
    cursor.close()

    if records:
        df = pd.DataFrame(records, columns=["Record ID", "Patient ID", "Diagnosis", "Treatment", "Prescription", "Notes", "Created At"])
        st.dataframe(df)
    else:
        st.info("No medical records found.")

# Close Database Connection
if connection:
    connection.close()
 