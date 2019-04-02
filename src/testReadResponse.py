import json
import Model
import pandas as pd
import RequestParser
import argparse

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("origin", help="Enter origin city")
parser.add_argument("destination", help="Enter destination city")
parser.add_argument("date", help="Enter date (YYYY-MM-DD) of departure")
args = parser.parse_args()

response_json = json.loads(RequestParser.generateRequest(args.origin, args.destination, args.date).text)


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

recordsCSV = []
for i in itinerarios: 
    for l in itinerarios[i].legs:
        if itinerarios[i].legs[l].stops == 0:
            for s in itinerarios[i].legs[l].segments:
                recordsCSV.append(Model.RecordCSV(
                    numItinerarios,
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
            numItinerarios += 1

datos = pd.DataFrame([vars(r) for r in recordsCSV])

columnsTitles = ['id_oferta', 'origen', 'destino', 'hora_salida', 'hora_llegada', 'duracion', 'num_vuelo', 'aerolinea', 'cod_aerolinea', 'escalas', 'precio']

datos = datos.reindex(columns=columnsTitles)

datos.to_csv('./prueba1.csv', index = False)