import requests

# URL für die Kommentar-POST-Anfrage
url = 'http://localhost:5000/comments'

# Testdaten für den Kommentar
comment_data = {
    'item_id': 7,  # Ersetze dies durch die tatsächliche item_id, für die du einen Kommentar hinzufügen möchtest
    'acount_id': 123,  # Ersetze dies durch die tatsächliche account_id des Benutzers
    'comment': 'Hallo'  # Ersetze dies durch den tatsächlichen Kommentartext
}

# Führe die POST-Anfrage durch
response = requests.post(url, json=comment_data)

# Überprüfe die Antwort
if response.status_code == 201:
    print('Kommentar erfolgreich hinzugefügt!')
else:
    print(f'Fehler beim Hinzufügen des Kommentars. Statuscode: {response.status_code}')
    print(response.json())
