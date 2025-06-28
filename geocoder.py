import requests
import googlemaps
from unidecode import unidecode
from arcgis.gis import GIS
from arcgis.geocoding import geocode

EXCEPTION_LIST = { # List for places that free geocoders cant find. Google might find them but work already done
    "Sezanne, Tokyo":"1 Chome-11-1 Marunouchi, Chiyoda City, Tokyo 100-6277, Japan", 
    "Orfali Bros Bistro, Dubai":"D92 - Jumeirah - Jumeirah 1 - Dubai - United Arab Emirates", 
    "La Cime, Osaka":"3 Chome-2-15 Kawaramachi, Chuo Ward, Osaka, 541-0048, Japan", 
    "Sazenka, Tokyo":"4 Chome-7-5 Minamiazabu, Minato City, Tokyo 106-0047, Japan", 
    "Central, Lima":"Av. Pedro de Osma 301, Barranco 15063, Peru", 
    "Chef Tam's Seasons, Macau":"Wynn Palace, Av. da Nave Desportiva, Macao", 
    "Evvai, São Paulo":"R. Joaquim Antunes, 108 - Pinheiros, São Paulo - SP, 05415-000, Brazil",
    "Florilege, Tokyo":"Japan, 〒105-0001 Tokyo, Minato City, Toranomon, 5 Chome−10−7 麻布台ヒルズ ガーデンプラザD 2F",
    "Sorn, Bangkok":"56 Soi Sukhumvit 26, Klongton Khlong Toei, Bangkok 10110, Thailand",
    "Nusara, Bangkok": "336 Maha Rat Rd, Phra Borom Maha Ratchawang, Khet Phra Nakhon, Bangkok 10200, Thailand",
    "Twins Garden, Moscow":"Strastnoy Blvd, 8А, Moscow, Russia, 125009",
    "The Chairman, Hong Kong":"3rd Floor, The Wellington, 198 Wellington St, Central, Hong Kong",
    "Felix, Hong Kong":"The Peninsula Hong Kong, Salisbury Rd, Tsim Sha Tsui, Hong Kong",
    "The Lone Star, Mount Standfast": "Hwy 1B, Mount Standfast, Saint James BB24053, Barbados",
    "Fu He Hui, Shanghai": "1037 Yuyuan Rd, Changning District, Shanghai, China, 200085",
    "Koan, Copenhagen": "Langeliniekaj 5, 2100 København, Denmark",
    "El Bulli, Roses": "Carrer la Roca, 4, 17480 Roses, Girona, Spain",
    "Lido 84, Gardone Riviera": "Corso Giuseppe Zanardelli, 196, 25083 Gardone Riviera BS, Italy",
    "Tantris, Munich": "Johann-Fichte-Straße 7, 80805 München, Germany",
    "Vyn, Skillinge": "Höga vägen 72, 272 92 Simrishamn, Sweden",
    "Operakallaren, Stockholm": "Karl XII:s torg 3, 111 47 Stockholm, Sweden",
    "Charlie Trotter's, Chicago": "816 W Armitage Ave, Chicago, IL 60614, USA",
    "Chez Dominique, Helsinki": "Pohjoisesplanadi 37, 00100 Helsinki, Finland",
    "Vong, New York": "885 Third Avenue, Manhattan, New York, United States"
}

class Geocode:
    def __init__(self, locator=None):
        self.locator = locator
        self.address = None
        self.portal = GIS()

    def get_address_google(self):
        print("Using Google API. Careful, it costs money!")

        gmaps = googlemaps.Client(key='XXX')
        
        geocode_result = gmaps.geocode("restaurant "+self.locator)
        if not geocode_result:
            return None
        
        self.address = geocode_result[0]['formatted_address']

    def geocoder_order(self):
        # Check if address_str matches any key in EXCEPTION_LIST
        for exception_key in EXCEPTION_LIST:
            if exception_key == self.locator:
                print("Exception for {}".format(self.locator))
                self.address = EXCEPTION_LIST[exception_key]
                return None
            
        # If the address is not in the exception list, proceed with geocoding
        self.get_address_google()

        '''self.geocode_address_nominatim(self.locator)
        if not self.address:
            self.geocode_address_arcgis()'''

    def geocode_address_arcgis(self):
        # print("Using ArcGis")
        self.address = geocode(self.locator)[0]['attributes']['Place_addr']
        if self.address: 
            self.address = unidecode(self.address)
            
    def geocode_address_nominatim(self, address_str):
        """
        Geocode a string address using the Nominatim API (OpenStreetMap).
        Returns a formatted address string if found, else None.
        """
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': address_str,
            'format': 'json',
            'limit': 1
        }
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data:
                # print(data)
                addressReturned = (data[0]['display_name'])
                # Strip all characters before the first comma, including the comma itself
                if ',' in addressReturned:
                    addressReturned = addressReturned.split(',', 1)[1].strip()
                self.address = addressReturned

                return None
        except Exception as e:
            print(f"Geocoding error: {e}")
        

def get_address(locator):
    geoObject = Geocode(locator=locator)
    geoObject.geocoder_order()
    return geoObject.address

if __name__ == "__main__":
    # Example usage
    locators = ["Disfrutar, Barcelona", "Mountain, London", "Table by Bruno Verjus, Paris", "Gaggan, Bangkok", "Central, Lima"]
    for i in locators:
        address = get_address(i)
        print(f"Geocoded address: {address}")