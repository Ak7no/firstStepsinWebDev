from website import create_app
from website.models import db, Hotel

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Prüfe ob Hotels existieren
        if not Hotel.query.first():
            # Füge Testhotels hinzu
            hotels = [
                Hotel(name='Hotel Berlin', city='Berlin', price_per_night=100),
                Hotel(name='Hotel München', city='München', price_per_night=120),
                Hotel(name='Hotel Hamburg', city='Hamburg', price_per_night=90)
            ]
            db.session.add_all(hotels)
            db.session.commit()
    
    app.run(debug=True)

