import requests

url = "http://127.0.0.1:5000/ListItem"

# Product information
data = {
    "title": "auto mit leicht gebrauchsspuren",
    "price": 1.99,
    "description": "Verkaufe hier mein auto mit leichten gebrauchs spuren",
    "location": "Bielefeld",
}

# Load the image file
files = {'image': open('auto.jpg', 'rb')}

# Send the POST request
response = requests.post(url, data=data, files=files)

# Print the response
print(response.status_code)
print(response.json())
