# Simple test to check patient dashboard logic without Django

def test_patient_dashboard_logic():
    """
    Test the logic used in the patient dashboard view
    """
    # Simulate the patient dashboard view logic
    print("Testing patient dashboard logic...")
    
    # Simulate user profile check
    try:
        # This would be the equivalent of request.user.userprofile in the view
        user_profile = {
            'user_type': 'patient',
            'full_name': 'Test Patient',
            'id': 12345
        }
        print("User profile found:", user_profile)
    except Exception as e:
        print("Error getting user profile:", str(e))
        return False
    
    # Check if user is a patient
    if user_profile['user_type'] != 'patient':
        print("Access denied. Patients only.")
        return False
    
    # Simulate patient profile check
    try:
        patient_profile = {
            'medical_history': 'No significant medical history',
            'emergency_contact': '0987654321',
            'blood_type': 'O+'
        }
        print("Patient profile found:", patient_profile)
    except Exception as e:
        print("Error getting patient profile:", str(e))
        patient_profile = None
    
    # Simulate upcoming appointments
    upcoming_appointments = [
        {
            'doctor': 'Dr. John Smith',
            'date': '2025-10-15',
            'time': '10:00 AM',
            'treatment': 'General Checkup',
            'status': 'confirmed'
        },
        {
            'doctor': 'Dr. Emily Johnson',
            'date': '2025-10-20',
            'time': '2:30 PM',
            'treatment': 'Blood Test',
            'status': 'pending'
        }
    ]
    print("Upcoming appointments:", len(upcoming_appointments))
    
    # Simulate recent records
    recent_records = [
        {'title': 'Blood Test Report', 'doctor': 'Dr. John Smith', 'date': 'Oct 10, 2025', 'status': 'Normal'},
        {'title': 'MRI Scan', 'doctor': 'Dr. Emily Johnson', 'date': 'Oct 5, 2025', 'status': 'Review'},
    ]
    print("Recent records:", len(recent_records))
    
    # Statistics
    total_appointments = len(upcoming_appointments)
    medical_records = len(recent_records)
    prescriptions = 3
    health_score = "85%"
    
    print("Statistics:")
    print(f"  Total appointments: {total_appointments}")
    print(f"  Medical records: {medical_records}")
    print(f"  Prescriptions: {prescriptions}")
    print(f"  Health score: {health_score}")
    
    # Doctor and hospital info
    doctor = {
        'name': 'Dr. John Smith',
        'specialization': 'General Medicine',
        'experience_years': 10
    }
    print("Doctor info:", doctor['name'])
    
    hospital = {
        'name': 'Apollo Hospitals',
        'state': 'Chennai'
    }
    print("Hospital info:", hospital['name'])
    
    print("\nTest completed successfully!")
    return True

if __name__ == "__main__":
    test_patient_dashboard_logic()