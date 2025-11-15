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

@views.route('/booking/<int:hotel_id>/step1', methods=['GET', 'POST'])
@login_required
def booking_step1(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    
    if request.method == 'POST':
        print("🔵 POST Request empfangen in booking_step1")
        
        checkin_date = request.form.get('checkin')
        checkout_date = request.form.get('checkout')
        total_price = request.form.get('total_price')  # ← Vom Frontend
        num_children = request.form.get('num_children', 0)
        num_adults = request.form.get('num_adults', 1)
        room_type = request.form.get('room_type')  # ← WICHTIG!
        
        # ✅ VALIDIERUNG
        try:
            total_price = float(total_price)
            if total_price <= 0:
                flash("❌ Ungültiger Preis!", "error")
                return redirect(url_for('views.booking_step1', hotel_id=hotel_id))
        except (ValueError, TypeError):
            flash("❌ Preisberechnung fehlgeschlagen!", "error")
            return redirect(url_for('views.booking_step1', hotel_id=hotel_id))
        
        num_guests = int(num_children) + int(num_adults)
        
        # ✅ SESSION speichern
        session['booking_data'] = {
            'hotel_id': hotel_id,
            'checkin': checkin_date,
            'checkout': checkout_date,
            'num_children': num_children,
            'num_adults': num_adults,
            'room_type': room_type,
            'total_price': total_price  # ← GESPEICHERT!
        }
        
        print(f"💾 Session gespeichert: {session['booking_data']}")
        return redirect(url_for('views.booking_step2', hotel_id=hotel_id))
    
    return render_template('booking_step1.html', user=current_user, hotel=hotel)


from datetime import datetime

def parse_date_flexible(date_string):
    """Versucht, das Datum in verschiedenen Formaten zu parsen"""
    if not date_string:
        return None
    
    formats = [
        '%Y-%m-%d',      # ISO: 2025-11-01
        '%d.%m.%Y',      # Deutsch: 01.11.2025
        '%d/%m/%Y',      # Alternative: 01/11/2025
        '%Y/%m/%d',      # Alternative: 2025/11/01
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt).date()
        except ValueError:
            continue
    
    raise ValueError(f"Datum '{date_string}' konnte nicht geparst werden")


@views.route('/booking/<int:hotel_id>/step2', methods=['GET', 'POST'])
@login_required
def booking_step2(hotel_id):
    print(f"booking_step2 aufgerufen - Method: {request.method}")
    hotel = Hotel.query.get_or_404(hotel_id)
    
    if 'booking_data' not in session:
        print("Keine booking_data in Session gefunden!")
        flash("Bitte starte die Buchung von vorne.", "warning")
        return redirect(url_for('views.booking_step1', hotel_id=hotel_id))
    
    booking_data = session.get('booking_data')
    checkin = booking_data.get('checkin')
    checkout = booking_data.get('checkout')
    total_price = booking_data.get('total_price', 0)  # ← AUS SESSION
    num_guests_adult = booking_data.get('num_adults')
    num_guests_child = booking_data.get('num_children')
    num_guests = int(num_guests_adult) + int(num_guests_child)
    
    if request.method == 'POST':
        print("POST Request in booking_step2")
        
        try:
            booking = Booking(
                hotel_id=hotel_id,
                user_id=current_user.id,
                checkin_date=parse_date_flexible(checkin),
                checkout_date=parse_date_flexible(checkout),
                num_guests_adult=int(num_guests_adult),
                num_guests_child=int(num_guests_child),
                special_requests=request.form.get('special_requests', ''),
                total_price=total_price,  # ← SPEICHERN!
                status='pending'
            )
            db.session.add(booking)
            db.session.flush()
            print(f"✅ Booking erstellt mit ID: {booking.id}")
            
            # Gäste speichern...
            for i in range(num_guests):
                first_name = request.form.get(f'firstname_{i}')
                last_name = request.form.get(f'lastname_{i}')
                email = request.form.get(f'email_{i}')
                phone = request.form.get(f'phone_{i}')
                birthdate_str = request.form.get(f'birthdate_{i}')
                
                birthdate = parse_date_flexible(birthdate_str) if birthdate_str else None
                
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
            
            db.session.commit()
            print(f"💾 Alle Daten in DB gespeichert!")
            
            session['booking_id'] = booking.id
            flash(f'✅ Gästeinformationen für {num_guests} Gäste gespeichert!', 'success')
            
            return redirect(url_for('views.booking_review', hotel_id=hotel_id))
            
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
                         checkout=checkout,
                         total_price=total_price)


@views.route('/booking/<int:hotel_id>/review', methods=['GET', 'POST'])
@login_required
def booking_review(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    
    if request.method == 'POST':
        booking_data = session.get('booking_data')
        
        if not booking_data:
            flash("Buchungsdaten fehlen.", "warning")
            return redirect(url_for('views.booking_step1', hotel_id=hotel_id))

        try:
            checkin_date = parse_date_flexible(booking_data['checkin'])
            checkout_date = parse_date_flexible(booking_data['checkout'])
            nights = (checkout_date - checkin_date).days
            
            # ✅ WICHTIG: Preis vom Server neu berechnen!
            room_type = booking_data.get('room_type', 'standard')
            room_prices = {
                'standard': hotel.price_per_night,
                'deluxe': hotel.price_per_night_u1,
                'family': hotel.price_per_night_u2,
                'premium': hotel.price_per_night_u3
            }
            
            price_per_person = room_prices.get(room_type, hotel.price_per_night)
            num_adults = int(booking_data.get('num_adults', 1))
            num_children = int(booking_data.get('num_children', 0))
            
            # Berechnung: Erwachsene voller Preis, Kinder 50%
            total_price = nights * (
                (price_per_person * num_adults) + 
                (price_per_person * 0.5 * num_children)
            )
            
            print(f"💰 Finale Berechnung: {nights} Nächte × {price_per_person}€ = {total_price}€")
            
            booking = Booking(
                user_id=current_user.id,
                hotel_id=hotel_id,
                checkin_date=checkin_date,
                checkout_date=checkout_date,
                num_guests_adult=num_adults,
                num_guests_child=num_children,
                special_requests=booking_data.get('special_requests', ''),
                total_price=total_price,  # ← FINALE BERECHNUNG!
                status='confirmed'
            )
            
            db.session.add(booking)
            db.session.commit()
            
            print(f"✅ Buchung gespeichert mit ID: {booking.id}, Preis: {total_price}€")
            
            session.pop('booking_data', None)
            flash('Buchung erfolgreich abgeschlossen!', 'success')
            
            return redirect(url_for('views.booking_confirmation', booking_id=booking.id))
            
        except Exception as e:
            print(f"❌ FEHLER: {str(e)}")
            flash(f'Fehler bei der Buchung: {str(e)}', 'error')
            return redirect(url_for('views.booking_step1', hotel_id=hotel_id))

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

