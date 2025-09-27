import requests

# Test the admin API
response = requests.post('http://127.0.0.1:8000/accounts/admin/api/doctors/add/', data={
    'name': 'Test Doctor',
    'specialization': 'Test Specialization',
    'email': 'test@example.com',
    'experience_years': 10
})

print(f"Status code: {response.status_code}")
print(f"Response: {response.text}")