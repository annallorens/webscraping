import json
import Constants
import pandas as pd
import RequestParser
import argparse

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--origin", dest='origin', help="Enter origin city")
parser.add_argument("--destination", dest='destination', help="Enter destination city")
parser.add_argument("--date", dest='date', help="Enter date (YYYY-MM-DD) of departure")
parser.add_argument("--itineraryMode", dest='itineraryMode', help="(Optional) Choose only direct flights (D) or all flights (A). Default option: A")
parser.add_argument("--maxPrice", dest='maxPrice', type=int, help="(Optional) Set maximum price (e.g: 100)")
args = parser.parse_args()

response_json = json.loads(RequestParser.generateRequest(args.origin, args.destination, args.date, args.itineraryMode, args.maxPrice).text)

places = RequestParser.readPlaces(response_json)

airlines = RequestParser.readAirlines(response_json)

segments = RequestParser.readSegments(response_json)

legs = RequestParser.readLegs(response_json, segments, places)


itineraries = RequestParser.readItineraries(response_json, legs)

outputData = RequestParser.getOutputFormat(itineraries, airlines, places)

if not args.maxPrice is None:
    outputData = RequestParser.getFlightsByPrice(outputData, args.maxPrice)

if not args.itineraryMode is None and args.itineraryMode == 'D':
    outputData = RequestParser.getDirectFlights(outputData)

outputDataFrame = pd.DataFrame([vars(r) for r in outputData])

outputDataFrame = outputDataFrame.reindex(columns=Constants.columnsTitles)

outputDataFrame.to_csv('./prueba1.csv', index = False)