# firstStepsinWebDev
This repository contains my first steps in the world of web development
# DHBW Portfolio 
## Frontend 
**Technologies:** HTML, CSS, JavaScript, Jinja2 Template-Engine
**Funktion:** Darstellung der Website & dynamische Inhalte auf der Webseite, wie Preisberechnung und Date-Range-Picker.
**Jinja2 Template-Engine:** Jinja2 ist eine Template-Engine für Python, die es ermöglicht, HTML-Templates mit Python-Code zu kombinieren. Dadurch können in das HTML direkt Logiken wie Schleifen oder If-Abfragen durchgeführt werden. Im Code ist das Jinja2 Template schnell zu erkennen, da es mit {{ }} geschrieben wird. Bspw. ist Content enthalten wie {{hotel.description_long}} || hier wird aus der Datenbank das Attribut description_long aus der Relation hotel geholt und direkt in der HTML-Seite eingebunden. 
## Backend
**Technologies:** Python, Flask Micro-Framework
**Funktion:** Logik der Website, Datenbankanbindung, Authentifizierung, Password Hashing, Routing, etc.
**Flask:** Flask ist ein Micro-Framework für Python, das es ermöglicht, Webanwendungen zu erstellen. Flask bietet eine einfache und flexible Möglichkeit, Webanwendungen zu erstellen, ohne dass man sich um die Komplexität eines großen Frameworks kümmern muss. Flask bietet eine Vielzahl von Erweiterungen, die es ermöglichen, zusätzliche Funktionen zu hinzuzufügen, wie hier z.B. die Datenbankanbindung. 
### Site Routing
**Umsetzung:** Flask Blueprints
**Erklärung:** Unter Routing ist zu verstehen, was passiert, wenn jemand /login oder /booking aufruft. Also das URL-Management und die Verteilung. 
Das Routing ist hier modular aufgebaut: 
- In auth.py werden routen für das login definiert.
- In views.py sind die Hauptseiten hinterlegt mit @views.route('/...')
- Diese "Blueprints" werden in der init.py registriert, um die URL-Struktur zusammenzusetzen. 


## Datenbank
**Technologien:** SQLAlchemy, SQLite
**SQLAlchemy:** SQLAlchemy ist eine Python-Bibliothek, die es ermöglicht, mit relationalen Datenbanken zu arbeiten, ohne dass man sich um die Komplexität der Datenbankanbindung kümmern muss. SQLAlchemy übersetzt Python-Objekte automatisch in Datenbank-Befehle ohne rohes SQL zu schreiben. 
**SQLITE:** SQLite ist eine relationale Datenbank, die in eine einzelne Datei gespeichert wird. SQLite ist einfach zu verwenden und eignet sich gut für kleine bis mittelgroße Anwendungen. In diesem Projekt wird SQLite verwendet um folgende Relationen zu speichern: 
- Hotel = (id - Primary Key, name, city, description, price_per_night, price_per_night_u1,price_per_night_u2, price_per_night_u3, descriptio_long, service_details, latitude, longtitude, hotel_email, hotel_phone, hotel_website, hotel_street)
- User = (id - Primary Key, email, password, first_name)
- Booking = (id - Primary Key, user_id - Foreign Key, hotel_id - Foreign Key, check_in_date, check_out_date, num_guests_adult, num_guests_children, special_requests, status, created_at, total_price, creditcard_name, creditcard_number, creditcard_expiry, creditcard_cvc)
- Guest = (id - Primary Key, booking_id - Foreign Key, first_name, last_name, email, phone, birthdate, guest_number)
Hinweis: Alle Relationen befinden sich in 3. Normalform, bis auf Booking, da der total_price partiell abhängig ist von hotel_id, check_in_date, check_out_date, num_guests_adult und num_guests_children.