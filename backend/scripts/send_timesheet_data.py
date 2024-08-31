import requests
import json

# Define the API endpoint
# url = "backend:5001/verify"
url = "http://backend:5001/verify"


# Define the data to be sent in the POST request
data = {
    "email": "abdel.nasser045@gmail.com",  # Replace with the actual email
    "tableData": [
        {"date": "2023-08-25", "hours": 8, "location": "Office", "position": "Developer"},
        {"date": "2023-08-26", "hours": 7.5, "location": "Home", "position": "Developer"}
        # Add more entries as needed
    ]
}

# Send the POST request
try:
    response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))

    # Check if the request was successful
    if response.status_code == 200:
        print("Success! Here is the response data:")
        print(response.json())
    else:
        print(f"Failed with status code: {response.status_code}")
        print(response.json())

except Exception as e:
    print(f"An error occurred: {e}")