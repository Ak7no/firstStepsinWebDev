document.addEventListener('DOMContentLoaded', function() {
    const mapElement = document.getElementById('map');

    if (mapElement) {
        const lat = parseFloat(mapElement.dataset.lat);
        const lng = parseFloat(mapElement.dataset.lng);
        const name = mapElement.dataset.name;
        const street = mapElement.dataset.street;

        if (!isNaN(lat) && !isNaN(lng)) {
            const hotelLocation = [lat, lng];

            const map = L.map('map').setView(hotelLocation, 15);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors',
                maxZoom: 19
            }).addTo(map);

            L.marker(hotelLocation)
                .addTo(map)
                .bindPopup(`<b>${name}</b><br>${street}`)
                .openPopup();
        }
    }
});