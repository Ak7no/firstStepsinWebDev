document.addEventListener('DOMContentLoaded', function () {
    const configElement = document.getElementById('booking-config');
    if (!configElement) return; 

    const roomPrices = {
        'standard': parseFloat(configElement.dataset.priceStandard),
        'deluxe': parseFloat(configElement.dataset.priceDeluxe),
        'family': parseFloat(configElement.dataset.priceFamily),
        'premium': parseFloat(configElement.dataset.pricePremium)
    };

    function calculatePrice() {
        const selectedRoomInput = document.querySelector('input[name="room_type"]:checked');
        const numAdults = parseInt(document.getElementById('num_adults').value) || 0;
        const numChildren = parseInt(document.getElementById('num_children').value) || 0;
        const checkinInput = document.getElementById('checkin').value;
        const checkoutInput = document.getElementById('checkout').value;

        const totalPriceDisplay = document.getElementById('total_price');
        const totalPriceInput = document.getElementById('total_price_input');

        if (!selectedRoomInput || !checkinInput || !checkoutInput) {
            totalPriceDisplay.textContent = '0,00€';
            return;
        }

        const checkin = new Date(checkinInput.split('.').reverse().join('-'));
        const checkout = new Date(checkoutInput.split('.').reverse().join('-'));

        const nights = Math.ceil((checkout - checkin) / (1000 * 60 * 60 * 24));

        if (nights <= 0) {
            totalPriceDisplay.textContent = '0,00€';
            return;
        }

        const pricePerPerson = roomPrices[selectedRoomInput.value] || 0;

        const pricePerAdult = pricePerPerson * numAdults;
        const pricePerChild = (pricePerPerson * 0.5) * numChildren; 
        const totalPrice = (nights * (pricePerAdult + pricePerChild));

        totalPriceDisplay.textContent = totalPrice.toFixed(2) + '€';
        totalPriceInput.value = totalPrice.toFixed(2); 
    }

    const guestButtons = document.querySelectorAll('.guest-btn');
    
    guestButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetId = this.dataset.target; 
            const change = parseInt(this.dataset.change);
            
            const input = document.getElementById(targetId);
            let value = parseInt(input.value) + change;

            if (targetId === 'num_adults') {
                value = Math.max(1, Math.min(8, value));
            } else {
                value = Math.max(0, Math.min(6, value));
            }

            input.value = value;

            const countSpanId = targetId.replace('num_', '') + '-count';
            document.getElementById(countSpanId).textContent = value;

            calculatePrice();
        });
    });

    const roomCards = document.querySelectorAll('.room-card');
    
    roomCards.forEach(card => {
        card.addEventListener('click', function() {
            roomCards.forEach(c => c.classList.remove('selected'));
            this.classList.add('selected');

            const radio = this.querySelector('input[type="radio"]');
            radio.checked = true;
            
            calculatePrice();
        });
    });

    const checkinEl = document.getElementById('checkin');
    const checkoutEl = document.getElementById('checkout');

    if (checkinEl && checkoutEl) {
        const picker = new Litepicker({
            element: checkinEl,
            elementEnd: checkoutEl,
            singleMode: false,
            numberOfMonths: 2,
            numberOfColumns: 2,
            minDate: new Date(),
            format: 'DD.MM.YYYY',
            lang: 'de-DE',
            tooltipText: { one: 'Nacht', other: 'Nächte' },
            tooltipNumber: (totalDays) => totalDays - 1,
            buttonText: {
                apply: 'Übernehmen',
                cancel: 'Abbrechen',
                previousMonth: '← Vorheriger Monat',
                nextMonth: 'Nächster Monat →',
                reset: 'Zurücksetzen'
            },
            dropdowns: {
                minYear: new Date().getFullYear(),
                maxYear: new Date().getFullYear() + 4,
                months: true,
                years: true
            },
            setup: (picker) => {
                picker.on('selected', (date1, date2) => {
                    if (date1 && date2 && date1.getTime() === date2.getTime()) {
                        alert('Abreise muss nach der Anreise sein!');
                        picker.clearSelection();
                    } else {
                        calculatePrice();
                    }
                });
            }
        });
    }
});