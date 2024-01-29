import requests

url = "http://127.0.0.1:5000/ListItem"

# Product information
data = {
    "title": "BMW",
    "price": 200000.99,
    "description": "Verkaufe hier mein alten BMW",
    "location": "Büren",
}

# Load the image file
files = {'image': open('OIP.jpg', 'rb')}

# Send the POST request
response = requests.post(url, data=data, files=files)

# Print the response
print(response.status_code)
print(response.json())
