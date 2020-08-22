import geograpy
from geograpy import extraction
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
   
places = geograpy.get_place_context(text="The National Air and Space Museum of the Smithsonian Institution, also called the Air and Space Museum, is a museum  ‘in Washington, D.C. It was established in 1946 as the National Air Museum and opened its main building on the National Mail near L’Enfant Plaza in 1976. In 2018, the museum saw approximately 6.2 million visitors, making it the fifth most visited  _ museum in the world, and the second most visited museum in the United States.!°] The museum contains the Apollo 11  _ Command Module Columbia, the Friendship 7 capsule which was flown by John Glenn, Charles Lindbergh's Spirit of St.  -ouis, the Bell X-1 which broke the sound barrier, the model of the starship Enterprise used in the science fiction television jow Star Trek: The Original Series, and the Wright brothers' Wright Flyer airplane near the entrance.")
places = places.regions
gelocator = Nominatim(user_agent='google_api')
lat_lon = []
for place in places:
    try:
        location = gelocator.geocode(place)
        if location:
            lat_lon.append([location.latitude, location.longitude])
    except GeocoderTimedOut:
        continue

print(places)
