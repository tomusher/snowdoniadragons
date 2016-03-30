var maps = document.querySelectorAll('.group-map');
var accessToken = 'pk.eyJ1IjoidG9tdXNoZXIiLCJhIjoiNUhKcmlBbyJ9.91k0LU5UXFSXIXYG_--uBg';

for(var i=0; i<maps.length; i++) {
    var mapContainer = maps[i];
    var coords = mapContainer.dataset.coords.split(',');
    var mapObject = leaflet.map(mapContainer).setView(coords, 11);
    leaflet.tileLayer('http://{s}.tiles.mapbox.com/v4/{mapId}/{z}/{x}/{y}.png?access_token={token}', {
        attribution: 'Map data &copy; OpenStreetMap contributors',
        maxZoom: 18,
        subdoains: ['a', 'b', 'c', 'd'],
        mapId: 'mapbox.emerald',
        token: accessToken
    }).addTo(mapObject);
    leaflet.Icon.Default.imagePath = '/static/vendor/leaflet/images';
    var marker = leaflet.marker(coords).addTo(mapObject);
}
