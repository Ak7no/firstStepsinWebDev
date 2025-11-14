from website import create_app
from website.models import db, Hotel

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Prüfe ob Hotels existieren
        if not Hotel.query.first():
            # Füge Testhotels hinzu in der DB 
            hotels = [
                Hotel(name='Maritim proArt Hotel Berlin', city='Berlin', price_per_night=279, description='Ein komfortables Hotel in Berlin.', description_long='Erleben Sie Berlin von seiner schönsten Seite in unserem zentral gelegenen Hotel. Direkt im Herzen der Hauptstadt erwarten Sie moderne Zimmer mit urbanem Flair und komfortabler Ausstattung. Starten Sie Ihren Tag mit einem reichhaltigen Frühstück und erkunden Sie die vielfältigen Sehenswürdigkeiten wie das Brandenburger Tor, die Museumsinsel oder den Alexanderplatz, die alle bequem erreichbar sind. Nach einem ereignisreichen Tag entspannen Sie in unserer stilvollen Lounge oder genießen regionale und internationale Spezialitäten in unserem hauseigenen Restaurant. Unser engagiertes Team sorgt dafür, dass Ihr Aufenthalt in Berlin einzigartig und rundum angenehm wird.', service_details='Kostenloses WLAN, Fitnessraum, 24-Stunden-Rezeption, Zimmerservice, Bar/Lounge',latitude=51.85603, longtitude=13.3879579),
                Hotel(name='Mandarin Oriental', city='München', price_per_night=713, description='Ein luxuriöses Hotel in München.', description_long='Willkommen in unserem Hotel im Herzen Münchens! Genießen Sie bayerische Gastfreundschaft in modernen, liebevoll eingerichteten Zimmern. Die zentrale Lage ermöglicht Ihnen einen schnellen Zugang zu den wichtigsten Attraktionen der Stadt, wie dem Marienplatz, dem Englischen Garten oder dem berühmten Viktualienmarkt. Nach einem Tag voller Eindrücke können Sie in unserem Wellnessbereich entspannen oder sich in unserem Restaurant mit regionalen Spezialitäten verwöhnen lassen. Unser freundliches Personal steht Ihnen jederzeit mit Rat und Tat zur Seite und macht Ihren Aufenthalt in München zu einem besonderen Erlebnis.', service_details='Kostenloses WLAN, Fitnessraum, 24-Stunden-Rezeption, Zimmerservice, Bar/Lounge', latitude= 48.1372989, longtitude= 11.5807333),
                Hotel(name='Fairmont Hotel Four Seasons', city='Hamburg', price_per_night=90, description='Ein schönes Hotel in Hamburg.', description_long='Unser Hotel vereint zeitlose Eleganz mit modernem Komfort und bietet Ihnen den perfekten Ort zum Entspannen und Genießen. Die stilvoll eingerichteten Zimmer sind mit hochwertigen Materialien ausgestattet und laden zum Wohlfühlen ein. Beginnen Sie den Tag mit einem abwechslungsreichen Frühstücksbuffet, entdecken Sie die vielfältigen Freizeitmöglichkeiten in der Umgebung oder lassen Sie sich in unserem hauseigenen Restaurant kulinarisch verwöhnen. Dank der zentralen Lage erreichen Sie Sehenswürdigkeiten und Einkaufsmöglichkeiten bequem zu Fuß. Unser freundliches Team steht Ihnen jederzeit zur Seite und sorgt dafür, dass Ihr Aufenthalt rundum angenehm und unvergesslich wird.', service_details='Kostenloses WLAN, Fitnessraum, 24-Stunden-Rezeption, Zimmerservice, Bar/Lounge', latitude = 53.5555409, longtitude= 9.9915198),
            ]
            db.session.add_all(hotels)
            db.session.commit()
    
    app.run(debug=True)

