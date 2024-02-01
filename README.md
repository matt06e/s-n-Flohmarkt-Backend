# API-Dokumentation

Die API ist standardmäßig unter `http://127.0.0.1:5000/` erreichbar.

## API-Endpunkte

### 1. Alle Produkte abrufen

#### Endpunkt


GET /products


#### Beschreibung

Eine Liste aller Produkte abrufen.

#### Antwort

- Statuscode: 200 OK
- Body: JSON-Array mit Produktinformationen.

### 2. Produkt nach ID abrufen

#### Endpunkt


GET /product=<int:id>


#### Parameter

- `id`: Die eindeutige Kennung des Produkts.

#### Beschreibung

Detaillierte Informationen zu einem bestimmten Produkt abrufen.

#### Antwort

- Statuscode: 200 OK
- Body: JSON-Objekt mit Produktdetails.

### 3. Artikel auflisten

#### Endpunkt


POST /ListItem


#### Parameter

- `title`: Titel des Artikels.
- `price`: Preis des Artikels.
- `description`: Beschreibung des Artikels.
- `location`: Ort des Artikels.
- `image`: Bilddatei des Artikels (multipart/form-data).
- `get_typ`: Art des Erhalts des Artikels.
- `category`: Kategorie des Artikels.
- `payment_type`: Zahlungstyp für den Artikel.
- `account_id`: Mit dem Artikel verknüpfte Kontonummer.

#### Beschreibung

Einen neuen Artikel mit den bereitgestellten Informationen auflisten.

#### Antwort

- Statuscode: 201 Created
- Body: JSON-Objekt, das Erfolg oder Fehler angibt.

### 4. Produkte suchen

#### Endpunkt


GET /search=<string:search_query>


#### Parameter

- `search_query`: Die Suchanfrage für Produkte.

#### Beschreibung

Nach Produkten basierend auf der bereitgestellten Suchanfrage suchen.

#### Antwort

- Statuscode: 200 OK
- Body: JSON-Array mit übereinstimmenden Produkten.

### 5. Produktbild abrufen

#### Endpunkt


GET /product=<int:id>/image


#### Parameter

- `id`: Die eindeutige Kennung des Produkts.

#### Beschreibung

Das Bild eines bestimmten Produkts abrufen.

#### Antwort

- Statuscode: 200 OK
- Body: Bilddatei (JPEG-Format).

### 6. Kommentare abrufen

#### Endpunkt


GET /comment=<int:item_id>


#### Parameter

- `item_id`: Die eindeutige Kennung des Artikels.

#### Beschreibung

Kommentare zu einem bestimmten Artikel abrufen.

#### Antwort

- Statuscode: 200 OK
- Body: JSON-Array mit Kommentaren.

### 7. Kommentar posten

#### Endpunkt


POST /comments


#### Body

- JSON-Objekt mit den Schlüsseln:
  - `item_id`: Die eindeutige Kennung des Artikels.
  - `account_id`: Mit dem Kommentar verknüpfte Kontonummer.
  - `comment`: Text des Kommentars.

#### Beschreibung

Einen neuen Kommentar zu einem bestimmten Artikel hinzufügen.

#### Antwort

- Statuscode: 201 Created
- Body: JSON-Objekt, das Erfolg oder Fehler angibt.

### 8. Konto nach ID abrufen

#### Endpunkt


GET /account=<int:account_id>


#### Parameter

- `account_id`: Die eindeutige Kennung des Kontos.

#### Beschreibung

Detaillierte Informationen zu einem bestimmten Benutzerkonto abrufen.

#### Antwort

- Statuscode: 200 OK
- Body: JSON-Objekt mit Kontodetails.

### 9. Konto erstellen

#### Endpunkt


POST /accounts


#### Body

- Formulardaten mit den Schlüsseln:
  - `name`: Name des Benutzers.
  - `location`: Standort des Benutzers.
  - `image`: Bilddatei des Benutzers (multipart/form-data).

#### Beschreibung

Ein neues Benutzerkonto erstellen.

#### Antwort

- Statuscode: 201 Created
- Body: JSON-Objekt, das Erfolg oder Fehler angibt.
