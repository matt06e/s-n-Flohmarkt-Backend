from flask import Flask, jsonify

app = Flask(__name__)

produkte = [
  {
    "id": 1,
    "titel": "Produkt 1",
    "preis": 19.99,
    "beschreibung": "Eine kurze Beschreibung für Produkt 1.",
    "bilder": [
      "bild1.jpg",
      "bild2.jpg"
    ]
  },
  {
    "id": 2,
    "titel": "Produkt 2",
    "preis": 29.99,
    "beschreibung": "Eine kurze Beschreibung für Produkt 2.",
    "bilder": [
      "bild3.jpg",
      "bild4.jpg"
    ]
  },
  {
    "id": 3,
    "titel": "Produkt 3",
    "preis": 39.99,
    "beschreibung": "Eine kurze Beschreibung für Produkt 3.",
    "bilder": [
      "bild5.jpg",
      "bild6.jpg"
    ]
  }
]

def produkt_nach_id(id):
    for Produkt in produkte:
        if Produkt["id"] == id:
            return Produkt
    return None
@app.route('/')
def hello_world():
    return "hello world!"

@app.route('/produkte/<int:id>')
def page(id):
    gefundenes_produkt = produkt_nach_id(id)
    
    if gefundenes_produkt:
        return jsonify(gefundenes_produkt)
    else:
        return "Produkt mit ID {id} nicht gefunden.".format(id)

if __name__ == '__main__':
    app.run(debug=True)
