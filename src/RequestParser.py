import requests
import json
import datetime
import Model
import Constants

def generateRequest(org, dest, date, itineraryMode, maxPrice):
    validateArguments(org, dest, date, itineraryMode, maxPrice)
    for city in Constants.cities:
        if city["name"] == org:
            origin = city
        if city["name"] == dest:
            destination = city
    data = setData(origin, destination, date)
    return requests.post(Constants.URL, headers=Constants.headers, params=Constants.params, data=data)


def validateArguments(org, dest, date, itineraryMode, maxPrice):
    if org == dest:
        raise Exception('Origin and destination can not be the same city')

    if not itineraryMode is None:
        if itineraryMode != 'D' and itineraryMode != 'A':
            raise Exception('Accepted values: (A)ll flights/(D)irect Flights')

    if not maxPrice is None:
        if maxPrice < 0:
            raise Exception('MaxPrice must be greather than zero')

    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")


def setData(origin, destination, date):
    data_json = json.loads(Constants.dataScheme)
    data_json["legs"][0]["origin"] = origin["id"]
    data_json["legs"][0]["destination"] = destination["id"]
    data_json["legs"][0]["date"] = date
    data_json["outboundDate"] = date
    data_json["destination"] = destination
    data_json["origin"] = origin
    data = json.dumps(data_json)
    return data

def readSegments(response_json):
    segments = {}

    for seg in response_json['segments']:
        segments[seg['id']] = Model.Segment(seg['id'],seg['origin_place_id'],seg['destination_place_id'],seg['arrival'],seg['departure'],seg['duration']
                            ,seg['marketing_flight_number'],seg['marketing_carrier_id'],seg['operating_carrier_id'],seg['mode'])

    return segments

def readAirlines(response_json):
    airlines = {}

    for airline in response_json['carriers']:
        airlines[airline['id']] = Model.Airline(airline['id'],airline['name'],airline['alt_id'],airline['display_code'],airline['display_code_type'])

    return(airlines)

# Leemos a partir de la respuesta los diferentes 'places' y los almacenamos en un Dictionary de objetos Place
def readPlaces(response_json):
    places = {}

    for place in response_json['places']:
        places[place['id']] = Model.Place(place["id"],place["alt_id"],place["parent_id"],place["name"],place["type"],place["display_code"])

    return places

def readLegs(response_json, segments, places):
    legs = {}
    legSegments = {}

    for l in response_json['legs']:
        for s in l['segment_ids']:
            legSegments[s] = segments[s]

        legs[l['id']] = Model.Leg(l['id'], places[l['origin_place_id']], places[l['destination_place_id']],
                            l['departure'], l['arrival'], legSegments, l['duration'], l['stop_count'])
        legSegments = {}

    return legs

def readItineraries(response_json, legs):
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

def getOutputFormat(itineraries, airlines, places):
    # Contador de Itinerarios y Segmentos como identificadores para la salida en formato CSV
    numItinerarios = 1
    numSegmentos = 1

    recordsCSV = []
    for i in itineraries:
        for l in itineraries[i].legs:
            for s in itineraries[i].legs[l].segments:
                recordsCSV.append(Model.RecordCSV(
                    numItinerarios,
                    numSegmentos,
                    places[itineraries[i].legs[l].segments[s].origin_place_id],
                    places[itineraries[i].legs[l].segments[s].destination_place_id],
                    itineraries[i].legs[l].segments[s].departure,
                    itineraries[i].legs[l].segments[s].arrival,
                    itineraries[i].legs[l].segments[s].duration,
                    itineraries[i].legs[l].segments[s].marketing_flight_number,
                    airlines[itineraries[i].legs[l].segments[s].operating_carrier_id].name,
                    airlines[itineraries[i].legs[l].segments[s].operating_carrier_id].display_code,
                    itineraries[i].legs[l].stops,
                    itineraries[i].prices
                ))
                numSegmentos += 1
            numItinerarios += 1

    return recordsCSV

def getDirectFlights(totalFlights):
    directFlights = []

    for flight in totalFlights:
        if flight.escalas == 0:
            directFlights.append(flight)

    return directFlights

def getFlightsByPrice(totalFlights, maxPrice):
    filteredByPrice = []

    for flight in totalFlights:
        if flight.precio <= maxPrice:
            filteredByPrice.append(flight)

    return filteredByPrice