class Itinerarie:
    def __init__(self, id, legs, prices):
        self.id = id
        self.legs = legs
        self.prices = prices

    def __str__(self):
        return '\nID: {}\n{}Precio Total: {}'.format(self.id, self.legs, self.prices)

# Clase de lugares (pueden ser ciudades o aeropuertos) que seran origen o destino de las rutas
class Place:
    def __init__(self, id, alt_id, parent_id, name, type, display_code):
        self.id = id
        self.alt_id = alt_id
        self.parent_id = parent_id
        self.name = name
        self.type = type
        self.display_code = display_code

    def __str__(self):
        return '{}'.format(self.name)

# Clase con informacion correspondiente a las aerolineas
class Airline:
    def __init__(self, id, name, alt_id, display_code, display_code_type):
        self.id = id
        self.name = name
        self.alt_id = alt_id
        self.display_code = display_code
        self.display_code_type = display_code_type

    def __str__(self):
        return '{} ({})'.format(self.name, self.display_code)

class Leg:
    def __init__(self,id, origin, destination, departure, arrival, segments, duration, stops):
        self.id = id
        self.origin = origin
        self.destination = destination
        self.departure = departure
        self.arrival = arrival
        self.segments = segments
        self.duration = duration
        self.stops = stops

    def __str__(self):
        return 'Origen: {} Destino: {} ({} escalas). Hora de salida: {} - Hora de llegada: {} (Duración: {}\n{})'.format(self.origin, self.destination, self.stops, self.departure, self.arrival, self.duration, self.segments)

# Clase con informacion correspondiente al objeto JSON 'segment'
class Segment:
    def __init__(self, id, origin_place_id, destination_place_id, arrival, departure, duration, marketing_flight_number, marketing_carrier_id, operating_carrier_id, mode):
        self.id = id
        self.origin_place_id = origin_place_id
        self.destination_place_id = destination_place_id
        self.arrival = arrival
        self.departure = departure
        self.duration = duration
        self.marketing_flight_number = marketing_flight_number
        self.marketing_carrier_id = marketing_carrier_id
        self.operating_carrier_id = operating_carrier_id
        self.mode = mode

    def __str__(self):
        return 'Orig: {} Dest: {}. HoraSalida: {} - HoraLlegada: {}. Compañía: {}'.format(self.origin_place_id, self.destination_place_id,
                                                                                         self.departure, self.arrival, self.operating_carrier_id)

class RecordCSV:
    def __init__(self,id_oferta, origen, destino, hora_salida, hora_llegada, duracion, num_vuelo, aerolinea, cod_aerolinea, escalas, precio):
        self.id_oferta = id_oferta
        self.origen = origen
        self.destino = destino
        self.hora_salida = hora_salida
        self.hora_llegada = hora_llegada
        self.duracion = duracion
        self.num_vuelo = num_vuelo
        self.aerolinea = aerolinea
        self.escalas = escalas
        self.cod_aerolinea = cod_aerolinea
        self.precio = precio

    def __str__(self):
        return '{};{}'.format(self.origen,self.destino)