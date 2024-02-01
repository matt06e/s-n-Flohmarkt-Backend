import requests

# Ersatzdaten für den POST-Request
data = {
    'title': 'Testprodukt',
    'price': 19.99,
    'description': 'Dies ist ein Testprodukt.',
    'location': 'Testort',
    'image': open('OIP.jpg', 'rb'),
    'category': 'Testkategorie',
    'payment_type': 'Testzahlungstyp'
}

# POST-Request an die /ListItem-Route
response = requests.post('http://localhost:5000/ListItem', files={'image': ('image.jpg', data['image'])}, data=data)

# Drucke die Antwort
print(response.status_code)
print(response.json())
