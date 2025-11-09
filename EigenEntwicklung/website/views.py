from datetime import date, datetime
import json 
from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from .models import Guest, Hotel, Booking, Note, Reservation
from . import db

views = Blueprint('views', __name__)


#@views.route('/', methods=['GET', 'POST'])
#@login_required
#def home():
#    if request.method == 'POST': 
#        note = request.form.get('note')#Gets the note from the HTML 
#
#        if len(note) < 1:
#            flash('Note is too short!', category='error') 
#        else:
#            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
#            db.session.add(new_note) #adding the note to the database 
#            db.session.commit()
#            flash('Note added!', category='success')
#
#    return render_template("home.html", user=current_user)


#@views.route('/delete-note', methods=['POST'])
#def delete_note():  
#    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
#    noteId = note['noteId']
#    note = Note.query.get(noteId)
#    if note:
#        if note.user_id == current_user.id:
#            db.session.delete(note)
#            db.session.commit()
#
#    return jsonify({})


@views.route('/', methods=['GET', 'POST'])
@login_required
def booking_search():
    if request.method == 'POST':
        city = request.form.get('city')
        checkin = request.form.get('checkin')
        checkout = request.form.get('checkout')
        
        # Debug print
        print(f"Searching for: City={city}, Check-in={checkin}, Check-out={checkout}")
        
        hotels = Hotel.query.filter(Hotel.city.ilike(f'%{city}%')).all()
        
        # Debug print
        print(f"Found {len(hotels)} hotels")
        
        return render_template("booking_results.html", 
                             user=current_user,
                             hotels=hotels,
                             city=city)
    
    return render_template("booking_search.html", user=current_user)

@views.route('/booking/<int:hotel_id>/step1', methods=['GET', 'POST']) # Buchung Schritt 1
@login_required
def booking_step1(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    
    if request.method == 'POST':
        print("🔵 POST Request empfangen in booking_step1")
        
        checkin_date = request.form.get('checkin')
        checkout_date = request.form.get('checkout')
        num_guests = request.form.get('num_guests')
        
        print(f"📅 Check-in: {checkin_date}")
        print(f"📅 Check-out: {checkout_date}")
        print(f"👥 Gäste: {num_guests}")
        
        # Speichere in Session
        session['booking_data'] = {
            'hotel_id': hotel_id,
            'checkin': checkin_date,
            'checkout': checkout_date,
            'num_guests': num_guests
        }
        
        print(f"💾 Session gespeichert: {session['booking_data']}")
        
        redirect_url = url_for('views.booking_step2', hotel_id=hotel_id)
        print(f"🔀 Redirect zu: {redirect_url}")

        
        return redirect(redirect_url)
    
    print(f"📄 GET Request - Zeige booking_step1.html für Hotel {hotel_id}")
    return render_template('booking_step1.html', user=current_user, hotel=hotel)

@views.route('/booking/<int:hotel_id>/step2', methods=['GET', 'POST']) # Buchung Schritt 2
@login_required
@login_required
def booking_step2(hotel_id):
    print(f"booking_step2 aufgerufen - Method: {request.method}")
    hotel = Hotel.query.get_or_404(hotel_id)
    
    # Prüfe ob booking_data existiert
    if 'booking_data' not in session:
        print("Keine booking_data in Session gefunden!")
        flash("Bitte starte die Buchung von vorne.", "warning")
        return redirect(url_for('views.booking_step1', hotel_id=hotel_id))
    
    booking_data = session.get('booking_data')
    num_guests = int(booking_data.get('num_guests', 1))
    checkin = booking_data.get('checkin')
    checkout = booking_data.get('checkout')
    
    if request.method == 'POST':
        print("POST Request in booking_step2")
        
        try:
            # Neue Buchung in DB erstellen
            booking = Booking(
                hotel_id=hotel_id,
                user_id=current_user.id,
                checkin_date=datetime.strptime(checkin, '%Y-%m-%d').date(),      # ← Hier umwandeln!
                checkout_date=datetime.strptime(checkout, '%Y-%m-%d').date(),    # ← Hier umwandeln!
                num_guests=num_guests,
                special_requests=request.form.get('special_requests', ''),
                status='pending'
            )
            db.session.add(booking)
            db.session.flush()  # Booking-ID generieren
            print(f"✅ Booking erstellt mit ID: {booking.id}")
            
            # Gäste in DB speichern
            for i in range(num_guests):
                first_name = request.form.get(f'firstname_{i}')
                last_name = request.form.get(f'lastname_{i}')
                email = request.form.get(f'email_{i}')
                phone = request.form.get(f'phone_{i}')
                birthdate_str = request.form.get(f'birthdate_{i}')
                
                print(f"👤 Gast {i+1}: {first_name} {last_name}")
                
                # Geburtsdatum konvertieren
                birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date() if birthdate_str else None
                
                guest = Guest(
                    booking_id=booking.id,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone,
                    birthdate=birthdate,
                    guest_number=i + 1
                )
                db.session.add(guest)
                print(f"   → Gast {i+1} hinzugefügt")
            
            # Alles committen
            db.session.commit()
            print(f"💾 Alle Daten in DB gespeichert!")
            
            # Booking-ID in Session speichern
            session['booking_id'] = booking.id
            session['booking_data'].update({
                'special_requests': request.form.get('special_requests', '')
            })
            
            flash(f'✅ Gästeinformationen für {num_guests} Gäste gespeichert!', 'success')
            
            redirect_url = url_for('views.booking_review', hotel_id=hotel_id)
            print(f"🔀 Redirect zu: {redirect_url}")
            return redirect(redirect_url)
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Fehler beim Speichern: {str(e)}")
            flash(f'❌ Fehler beim Speichern: {str(e)}', 'danger')
            return redirect(url_for('views.booking_step2', hotel_id=hotel_id))
    
    print(f"📄 GET Request - Zeige booking_step2.html")
    return render_template('booking_step2.html', 
                         user=current_user, 
                         hotel=hotel,
                         hotel_id=hotel_id,
                         num_guests=num_guests,
                         checkin=checkin,
                         checkout=checkout)


@views.route('/booking/<int:hotel_id>/review', methods=['GET', 'POST'])
@login_required
def booking_review(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    
    print(f"🔵 booking_review aufgerufen - Method: {request.method}")
    
    if request.method == 'POST':
        booking_data = session.get('booking_data')
        print(f"DEBUG: POST /booking/<id>/review, booking_data = {booking_data}")
        
        if not booking_data:
            flash("Buchungsdaten fehlen. Bitte Schritt 1 erneut ausfüllen.", "warning")
            return redirect(url_for('views.booking_step1', hotel_id=hotel_id))

        try:
            # Berechne Anzahl Nächte
            checkin_date = datetime.strptime(booking_data['checkin'], '%Y-%m-%d').date()
            checkout_date = datetime.strptime(booking_data['checkout'], '%Y-%m-%d').date()
            nights = (checkout_date - checkin_date).days
            
            print(f"💰 Nächte: {nights}, Preis pro Nacht: {hotel.price_per_night}")
            
            # ✅ RICHTIG - Verwende die korrekten Feldnamen!
            booking = Booking(
                user_id=current_user.id,
                hotel_id=hotel_id,
                checkin_date=checkin_date,           # ✅ RICHTIG!
                checkout_date=checkout_date,        # ✅ RICHTIG!
                num_guests=int(booking_data.get('num_guests', 1)),
                special_requests=booking_data.get('special_requests', ''),
                status='confirmed'
            )
            
            db.session.add(booking)
            db.session.commit()
            
            print(f"✅ Buchung gespeichert mit ID: {booking.id}")
            
            session.pop('booking_data', None)
            
            flash('Buchung erfolgreich abgeschlossen!', 'success')
            
            redirect_url = url_for('views.booking_confirmation', booking_id=booking.id)
            print(f"🔀 Redirect zu: {redirect_url}")
            
            return redirect(redirect_url)
            
        except Exception as e:
            print(f"❌ FEHLER beim Speichern: {str(e)}")
            flash(f'Fehler bei der Buchung: {str(e)}', 'error')
            return redirect(url_for('views.booking_step1', hotel_id=hotel_id))

    print(f"📄 GET Request - Zeige booking_review.html")
    return render_template('booking_review.html',
                           user=current_user,
                           hotel=hotel,
                           booking_data=session.get('booking_data') or {})


@views.route('/booking/<int:hotel_id>', methods=['GET','POST']) # Detailseite für ein Hotel
@login_required
def booking_detail(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    return render_template("booking_detail.html", user=current_user, hotel=hotel)

@views.route('/booking/results') # Suchergebnisseite
@login_required
def booking_results():
    city = request.args.get('city')
    hotels = Hotel.query.filter(Hotel.city.ilike(f'%{city}%')).all() if city else []
    return render_template("booking_results.html", user=current_user, hotels=hotels, city=city)

@views.route('/booking/confirmation/<int:booking_id>') # Buchungsbestätigungsseite
@login_required
def booking_confirmation(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return render_template('booking_confirmation.html', user=current_user, booking=booking)

