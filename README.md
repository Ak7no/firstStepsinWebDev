# firstStepsinWebDev
Dieses Repository dokumentiert meine ersten Schritte in der Welt der Webentwicklung im Rahmen eines DHBW-Portfolioprojekts. Es handelt sich um eine voll funktionsfähige Hotelbuchungs-Anwendung, die mit Python und dem Flask-Framework erstellt wurde.

## Features

-   **Hotelsuche:** Suchen Sie nach Hotels, indem Sie einen Städtenamen eingeben.
-   **Detailansicht:** Sehen Sie sich detaillierte Informationen zu jedem Hotel an, einschließlich Beschreibungen, Dienstleistungen und einer interaktiven Karte (Leaflet.js).
-   **Mehrstufiger Buchungsprozess:**
    1.  **Reisedaten & Zimmer:** Wählen Sie An- und Abreisedatum, Anzahl der Gäste und den Zimmertyp.
    2.  **Gästedaten:** Geben Sie die Informationen für jeden Gast ein.
    3.  **Überprüfung & Zahlung:** Überprüfen Sie alle Details, geben Sie Zahlungsinformationen ein und schließen Sie die Buchung ab.
-   **Dynamische Preisberechnung:** Der Gesamtpreis wird in Echtzeit basierend auf Zimmertyp, Anzahl der Gäste und Aufenthaltsdauer berechnet.
-   **Buchungsbestätigung:** Nach erfolgreicher Buchung wird eine Bestätigungsseite mit allen relevanten Daten angezeigt, die gedruckt oder als PDF gespeichert werden kann.
-   **Automatisches Seeding:** Die Datenbank wird beim ersten Start der Anwendung automatisch mit einer umfangreichen Liste von Beispielhotels gefüllt.

## Technologie-Stack

| Kategorie  | Technologie                                               |
| :--------- | :-------------------------------------------------------- |
| **Backend**  | Python, Flask                                             |
| **Datenbank**| SQLite, SQLAlchemy (ORM)                                  |
| **Frontend** | HTML, CSS, JavaScript, Jinja2, Bootstrap                  |
| **JS-Bibliotheken** | Litepicker.js (Datumsauswahl), Leaflet.js (Karten) |

## Projektarchitektur

### Frontend

Das Frontend ist für die Darstellung der Weboberfläche und die Interaktion mit dem Benutzer verantwortlich.

-   **Technologien:** HTML, CSS, JavaScript, Jinja2 Template-Engine
-   **Funktion:** Darstellung der Website und dynamische Inhalte auf der Webseite, wie Preisberechnung und Date-Range-Picker.
-   **Jinja2 Template-Engine:** Jinja2 ist eine Template-Engine für Python, die es ermöglicht, HTML-Templates mit Python-Code zu kombinieren. Dadurch können in das HTML direkt Logiken wie Schleifen oder If-Abfragen eingebaut werden. Im Code ist das Jinja2-Template schnell an `{{ }}` zu erkennen. Beispielsweise wird mit `{{ hotel.description_long }}` das Attribut `description_long` aus der Datenbank geholt und direkt in der HTML-Seite eingebunden.

### Backend

Das Backend enthält die Geschäftslogik der Anwendung.

-   **Technologien:** Python, Flask Micro-Framework
-   **Funktion:** Logik der Website, Datenbankanbindung, Routing und das Verwalten von Sessions während des Buchungsprozesses.
-   **Flask:** Flask ist ein Micro-Framework für Python zum Erstellen von Webanwendungen. Es bietet eine einfache und flexible Möglichkeit, Webanwendungen zu erstellen, ohne die Komplexität eines großen Frameworks.
-   **Site Routing:** Das URL-Management wird durch Flask Blueprints modular gestaltet. In `views.py` sind alle Routen (z.B. `/`, `/booking/<hotel_id>/step1`) definiert. Dieser Blueprint wird in `__init__.py` registriert, um die Anwendungsstruktur zusammenzusetzen.

### Datenbank

Die Datenpersistenz wird durch eine SQLite-Datenbank realisiert, die über SQLAlchemy angesprochen wird.

-   **Technologien:** SQLAlchemy, SQLite
-   **SQLAlchemy:** SQLAlchemy ist eine Python-Bibliothek, die als Object-Relational Mapper (ORM) fungiert. Sie ermöglicht die Interaktion mit der relationalen Datenbank über Python-Objekte, ohne rohes SQL schreiben zu müssen.
-   **SQLite:** Eine dateibasierte, serverlose Datenbank, die sich gut für kleinere bis mittelgroße Anwendungen eignet.

**Datenbank-Schema:**

-   `Hotel`: Speichert alle Informationen über die Hotels.
    -   (id, name, city, description, price_per_night, description_long, service_details, latitude, longtitude, etc.)
-   `Booking`: Enthält alle Details zu einer spezifischen Buchung.
    -   (id, hotel_id, checkin_date, checkout_date, num_guests_adult, num_guests_child, total_price, creditcard_name, etc.)
-   `Guest`: Speichert die Daten der an einer Buchung beteiligten Gäste.
    -   (id, booking_id, first_name, last_name, email, phone, birthdate)
-   Visualisiert: 
   <img width="1057" height="557" alt="image" src="https://github.com/user-attachments/assets/573819a8-446d-411e-aa74-54bc65fc08a3" />


## Setup und Ausführung

Folgen Sie diesen Schritten, um das Projekt lokal auszuführen:

1.  **Repository klonen:**
    ```bash
    git clone https://github.com/ak7no/firstStepsinWebDev.git
    cd firstStepsinWebDev/EigenEntwicklung
    ```

2.  **Abhängigkeiten installieren:**
    Es wird empfohlen, eine virtuelle Umgebung zu verwenden.
    ```bash
    pip install Flask Flask-SQLAlchemy
    ```

3.  **Anwendung starten:**
    Führen Sie das Hauptskript aus.
    ```bash
    python main.py
    ```
    Beim ersten Start wird automatisch eine Datei `instance/database.db` erstellt und mit Beispieldaten für Hotels gefüllt.

4.  **Anwendung im Browser öffnen:**
    Navigieren Sie zu `http://127.0.0.1:5000` in Ihrem Webbrowser.

## Systemaufbau-Diagramm
<img width="3360" height="3352" alt="diagram" src="https://github.com/user-attachments/assets/de9d45e6-7004-4614-b40d-38fe5588a29d" />
