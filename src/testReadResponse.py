import requests
import json
import Model
import pandas as pd

headers = {
    'x-skyscanner-devicedetection-istablet': 'false',
    'origin': 'https://www.skyscanner.net',
    'accept-encoding': 'gzip, deflate, br',
    'x-skyscanner-mixpanelid': '169bc319f42ec-0682fa1b8bf5ca-36657905-1fa400-169bc319f4534f',
    'accept-language': 'es-ES,es;q=0.9,en;q=0.8,ca;q=0.7',
    'x-skyscanner-traveller-context': '330e3ad6-38be-47db-9b7a-997aa890dc1d',
    'x-skyscanner-viewid': '9f702099-0bf0-45b4-98d7-d603f9851375',
    'x-requested-with': 'XMLHttpRequest',
    'skyscanner-utid': '330e3ad6-38be-47db-9b7a-997aa890dc1d',
    'x-distil-ajax': 'azezcavtdrrxfqrtbw',
    'x-skyscanner-channelid': 'website',
    'x-skyscanner-devicedetection-ismobile': 'false',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'content-type': 'application/json; charset=UTF-8',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'referer': 'https://www.skyscanner.net/transport/flights/mad/lond/190331/?adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=0&preferdirects=true&outboundaltsenabled=false&inboundaltsenabled=false&ref=home',
    'authority': 'www.skyscanner.net',
}

params = (
    ('geo_schema', 'skyscanner'),
    ('carrier_schema', 'skyscanner'),
    ('response_include', 'query;deeplink;segment;stats;fqs;pqs'),
)

data = '{"market":"UK","currency":"GBP","locale":"en-GB","cabin_class":"economy","prefer_directs":true,"trip_type":"one-way","legs":[{"origin":"BCN","destination":"LOND","date":"2019-04-01","add_alternative_origins":false,"add_alternative_destinations":false}],"origin":{"id":"BCN","airportId":"BCN","name":"Madrid","cityId":"MADR","cityName":"Madrid","countryId":"ES","type":"Airport","centroidCoordinates":[-3.563333,40.472222]},"destination":{"id":"LOND","name":"London","cityId":"LOND","cityName":"London","countryId":"UK","type":"City","centroidCoordinates":[-0.0943465343,51.5041174139]},"outboundDate":"2019-03-31","adults":1,"child_ages":[],"options":{"include_unpriced_itineraries":true,"include_mixed_booking_options":true},"state":{}}'

response = requests.post('https://www.skyscanner.net/g/conductor/v1/fps3/search/', headers=headers, params=params, data=data)

# parse to json:
response_json = json.loads(response.text)



# Leemos los datos de los distintos segmentos y los almacenamos
def readSegments():
    segments = {}

    for seg in response_json['segments']:
        segments[seg['id']] = Model.Segment(seg['id'],seg['origin_place_id'],seg['destination_place_id'],seg['arrival'],seg['departure'],seg['duration']
                            ,seg['marketing_flight_number'],seg['marketing_carrier_id'],seg['operating_carrier_id'],seg['mode'])

    return segments

# Leemos los datos de las aerolineas de la respuesta y las almacenamos
def readAirlines():
    airlines = {}

    for airline in response_json['carriers']:
        airlines[airline['id']] = Model.Airline(airline['id'],airline['name'],airline['alt_id'],airline['display_code'],airline['display_code_type'])

    return(airlines)

# Leemos a partir de la respuesta los diferentes 'places' y los almacenamos en un Dictionary de objetos Place
def readPlaces():
    places = {}

    for place in response_json['places']:
        places[place['id']] = Model.Place(place["id"],place["alt_id"],place["parent_id"],place["name"],place["type"],place["display_code"])

    return places

def readLegs():
    legs = {}
    legSegments = {}

    for l in response_json['legs']:
        for s in l['segment_ids']:
            legSegments[s] = segmentos[s]

        legs[l['id']] = Model.Leg(l['id'], readPlaces()[l['origin_place_id']], readPlaces()[l['destination_place_id']],
                            l['departure'], l['arrival'], legSegments, l['duration'], l['stop_count'])
        legSegments = {}

    return legs

def readItineraries():
    itineraries = {}
    itineraryLegs = {}

    for it in response_json['itineraries']:
        precio = 0.0
        for opt in it['pricing_options']:
            if 'amount' in opt['price']:
                precio = opt['price']['amount']
        for l in it['leg_ids']:
            itineraryLegs[l] = legs[l]
        itineraries[it['id']] = Model.Itinerarie(it['id'], itineraryLegs, precio)
        itineraryLegs = {}

    return itineraries

lugares = readPlaces()
aerolineas = readAirlines()
segmentos = readSegments()
legs = readLegs()
itinerarios = readItineraries()

# Contador de Itinerarios y Segmentos como identificadores para la salida en formato CSV
numItinerarios = 1
numSegmentos = 1

recordsCSV = []
for i in itinerarios:
    for l in itinerarios[i].legs:
        for s in itinerarios[i].legs[l].segments:
            recordsCSV.append(Model.RecordCSV(
                numItinerarios,
                numSegmentos,
                lugares[itinerarios[i].legs[l].segments[s].origin_place_id],
                lugares[itinerarios[i].legs[l].segments[s].destination_place_id],
                itinerarios[i].legs[l].segments[s].departure,
                itinerarios[i].legs[l].segments[s].arrival,
                itinerarios[i].legs[l].segments[s].duration,
                itinerarios[i].legs[l].segments[s].marketing_flight_number,
                aerolineas[itinerarios[i].legs[l].segments[s].operating_carrier_id].name,
                aerolineas[itinerarios[i].legs[l].segments[s].operating_carrier_id].display_code,
                itinerarios[i].legs[l].stops,
                itinerarios[i].prices
            ))
            numSegmentos += 1
    numItinerarios += 1

datos = pd.DataFrame([vars(r) for r in recordsCSV])

columnsTitles = ['id_oferta', 'id_vuelo', 'origen', 'destino', 'hora_salida', 'hora_llegada', 'duracion', 'num_vuelo', 'aerolinea', 'cod_aerolinea', 'escalas', 'precio']

datos = datos.reindex(columns=columnsTitles)

datos.to_csv('/home/carlos/prueba1.csv', index = False)