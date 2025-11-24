from datetime import date, datetime
import json 
from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for, session
from .models import Guest, Hotel, Booking
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def booking_search():
    if request.method == 'POST':
        city = request.form.get('city')
        hotels = Hotel.query.filter(Hotel.city.ilike(f'%{city}%')).all()
        return render_template("booking_results.html", 
                             hotels=hotels,
                             city=city)
    
    return render_template("booking_search.html")

@views.route('/booking/<int:hotel_id>/step1', methods=['GET', 'POST'])
def booking_step1(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    
    if request.method == 'POST':
        checkin_date = request.form.get('checkin')
        checkout_date = request.form.get('checkout')
        total_price = request.form.get('total_price')  
        num_children = request.form.get('num_children', 0)
        num_adults = request.form.get('num_adults', 1) 
        room_type = request.form.get('room_type') 
        
        try:
            total_price = float(total_price)
            if total_price <= 0:
                flash("❌ Ungültiger Preis!", "error")
                return redirect(url_for('views.booking_step1', hotel_id=hotel_id))
        except (ValueError, TypeError):
            flash("❌ Preisberechnung fehlgeschlagen!", "error")
            return redirect(url_for('views.booking_step1', hotel_id=hotel_id))
        
        num_guests = int(num_children) + int(num_adults)
        
        session['booking_data'] = {
            'hotel_id': hotel_id,
            'checkin': checkin_date,
            'checkout': checkout_date,
            'num_children': num_children,
            'num_adults': num_adults,
            'room_type': room_type,
            'total_price': total_price 
        }
        #Print Session Data für Debugging und Validierung 
        print(f"Session gespeichert: {session['booking_data']}")
        return redirect(url_for('views.booking_step2', hotel_id=hotel_id))
    
    return render_template('booking_step1.html', hotel=hotel)


from datetime import datetime

def parse_date_flexible(date_string):
    if not date_string:
        return None
 #Dient um verschiedene Datumsformate zu erkennen und keine Fehler zu werfen bei der Speicherung   
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


@views.route('/booking/<int:hotel_id>/step2', methods=['GET', 'POST']) # Zweiter Schritt der Buchung
def booking_step2(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    
    if 'booking_data' not in session:
        flash("Bitte starte die Buchung von vorne.", "warning")
        return redirect(url_for('views.booking_step1', hotel_id=hotel_id))
    
    booking_data = session.get('booking_data')
    checkin = booking_data.get('checkin')
    checkout = booking_data.get('checkout')
    total_price = booking_data.get('total_price', 0) 
    num_guests_adult = booking_data.get('num_adults')
    num_guests_child = booking_data.get('num_children')
    num_guests = int(num_guests_adult) + int(num_guests_child)
    
    if request.method == 'POST':    
        print("POST Request in booking_step2")
        
        try:
            booking = Booking(
                hotel_id=hotel_id,
                checkin_date=parse_date_flexible(checkin),
                checkout_date=parse_date_flexible(checkout),
                num_guests_adult=int(num_guests_adult),
                num_guests_child=int(num_guests_child),
                special_requests=request.form.get('special_requests', ''),
                total_price=total_price,  
                status='pending'
            )
            db.session.add(booking)
            db.session.flush()
            flash(f'✅ Pending Booking erstellt mit ID: {booking.id}', 'success')
            
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
            flash(f'❌ Fehler beim Speichern: {str(e)}', 'danger')
            return redirect(url_for('views.booking_step2', hotel_id=hotel_id))

    return render_template('booking_step2.html',  
                         hotel=hotel,
                         hotel_id=hotel_id,
                         num_guests=num_guests,
                         checkin=checkin,
                         checkout=checkout,
                         total_price=total_price)


@views.route('/booking/<int:hotel_id>/review', methods=['GET', 'POST'])
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
            
            cardholder = request.form.get('cardholder', '').strip()
            card_number = request.form.get('card_number', '').replace(' ', '')
            expiry = request.form.get('expiry', '').strip()
            cvv = request.form.get('cvv', '').strip()
            
            if not cardholder or len(cardholder) < 3:
                flash("❌ Ungültiger Karteninhaber!", "error")
                return redirect(url_for('views.booking_review', hotel_id=hotel_id))
            
            if not card_number or len(card_number) < 13:
                flash("❌ Ungültige Kartennummer!", "error")
                return redirect(url_for('views.booking_review', hotel_id=hotel_id))
            
            if not expiry or len(expiry) != 5 or '/' not in expiry:
                flash("❌ Ungültiges Verfallsdatum (Format: MM/YY)!", "error")
                return redirect(url_for('views.booking_review', hotel_id=hotel_id))
            
            if not cvv or len(cvv) != 3:
                flash("❌ Ungültiger CVV!", "error")
                return redirect(url_for('views.booking_review', hotel_id=hotel_id))
            
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
            
            total_price = nights * (
                (price_per_person * num_adults) + 
                (price_per_person * 0.5 * num_children)
            )

            booking = Booking(
                hotel_id=hotel_id,
                checkin_date=checkin_date,
                checkout_date=checkout_date,
                num_guests_adult=num_adults,
                num_guests_child=num_children,
                total_price=total_price,
                status='confirmed',
                creditcard_name=cardholder,
                creditcard_number=card_number[-4:],  
                creditcard_expiry=expiry,
                creditcard_cvc=cvv
            )
            
            db.session.add(booking)
            db.session.commit()
            
            flash(f'✅ Buchung Bestätigt und gespeichert mit ID: {booking.id}', 'success')
            
            session.pop('booking_data', None)
            flash('✅ Buchung erfolgreich abgeschlossen!', 'success')
            
            return redirect(url_for('views.booking_confirmation', booking_id=booking.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Fehler bei der Buchung: {str(e)}', 'error')
            return redirect(url_for('views.booking_review', hotel_id=hotel_id))

    return render_template('booking_review.html',
                           hotel=hotel,
                           booking_data=session.get('booking_data') or {})

@views.route('/booking/<int:hotel_id>', methods=['GET','POST'])
def booking_detail(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    return render_template("booking_detail.html", hotel=hotel)

@views.route('/booking/results') 
def booking_results():
    city = request.args.get('city')
    hotels = Hotel.query.filter(Hotel.city.ilike(f'%{city}%')).all() if city else []
    return render_template("booking_results.html", hotels=hotels, city=city)

@views.route('/booking/confirmation/<int:booking_id>')
def booking_confirmation(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return render_template('booking_confirmation.html', booking=booking)

