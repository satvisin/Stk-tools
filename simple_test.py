import requests

# Simple test with exact curl parameters
url = 'https://int.apigw.umbrella.com/reports/v2/tenants/topTenantsByCategories?from=-23hours&to=now&limit=5'
headers = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjIwMTktMDEtMDEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJ1bWJyZWxsYS1hdXRoei9hdXRoc3ZjIiwic3ViIjoib3JnLzgyNzY1MDYvdXNlci8xMjI5MjQ2NyIsImV4cCI6MTc1MjgzNjgzMSwibmJmIjoxNzUyODM2NTMxLCJpYXQiOjE3NTI4MzY1MzEsInNjb3BlIjoicm9sZTpyb290LXJlYWRvbmx5IiwiYXV0aHpfZG9uZSI6ZmFsc2V9.IVPCzp0-pbj4OrwUEtAXWQXXpjF2L7EjKBpHGhssH0yvJXRN6Gv3ZdrIWjAFThPxyPf1dEugywUWL7Iy-aobyUyGnJUi7EIn_2jlMi8G7CQKX2EamvHFWX9jui3wqrRK4eD7NmDgGFhtuPSF2DNFDH5a2gBO5QOJMeOOeDnWGMXAzybn31nBLYiZSARGtKpmE2e5vKqWOIzfJxIHdYfYGmmxibmpldnwi7kJoSRtkcHse9mkMSOOlnaZDSRr_gm5CCskqYW9v90ebav8ueyFCvZET-f4GMh6j-46Qk0NgcV854lIQ7XI7EY96S-QOkUe0Qd2F15qJ_G-c5svnK2rag'
}

print("Testing API endpoint...")
try:
    response = requests.get(url, headers=headers, timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}...")
except requests.exceptions.Timeout:
    print("Request timed out!")
except Exception as e:
    print(f"Error: {e}")
