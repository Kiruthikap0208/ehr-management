USE ehr_db;

-- Insert Dummy Patients
INSERT INTO patients (first_name, last_name, date_of_birth, gender, contact_number, email, address)
VALUES
    ('John', 'Doe', '1990-05-15', 'Male', '1234567890', 'john.doe@example.com', '123 Main St, City'),
    ('Jane', 'Smith', '1985-10-20', 'Female', '0987654321', 'jane.smith@example.com', '456 Elm St, Town');

-- Insert Dummy Appointments
INSERT INTO appointments (patient_id, doctor_name, appointment_date, appointment_time, status)
VALUES
    (1, 'Dr. Brown', '2023-10-25', '10:00:00', 'Scheduled'),
    (2, 'Dr. Green', '2023-10-26', '14:00:00', 'Scheduled');

-- Insert Dummy Medical Records
INSERT INTO medical_records (patient_id, diagnosis, treatment, prescription, notes)
VALUES
    (1, 'Common Cold', 'Rest and hydration', 'Paracetamol 500mg', 'Patient advised to rest for 3 days.'),
    (2, 'Migraine', 'Avoid stress and bright lights', 'Ibuprofen 400mg', 'Patient to follow up in 2 weeks.');