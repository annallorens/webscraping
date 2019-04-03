import json
import Constants
import pandas as pd
import RequestParser
import argparse
from datetime import datetime
from datetime import timedelta
import os

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--origin", dest='origin', help="Enter origin city")
parser.add_argument("--destination", dest='destination', help="Enter destination city")
args = parser.parse_args()
 
# Get the flights information from the next 6 months every week
for i in range(1,26):
    date = (datetime.now().date()+timedelta(days=i*7))
    response_json = json.loads(RequestParser.generateRequest(args.origin, args.destination, date.strftime('%Y-%m-%d')).text)
    places = RequestParser.readPlaces(response_json)
    airlines = RequestParser.readAirlines(response_json)
    segments = RequestParser.readSegments(response_json)
    legs = RequestParser.readLegs(response_json, segments, places)
    itineraries = RequestParser.readItineraries(response_json, legs)
    outputData = RequestParser.getOutputFormat(itineraries, airlines, places)

    outputDataFrame = pd.DataFrame([vars(r) for r in outputData])
    outputDataFrame = outputDataFrame.reindex(columns=Constants.columnsTitles)
    fileName = "./pricingFlights.csv"

    if os.stat(fileName).st_size == 0:
        print('f')
        file = open(fileName,'w')
        outputDataFrame.to_csv(file, index = False)
    else:
        print('s')
        file = open(fileName, 'a')
        outputDataFrame.to_csv(file, index = False, header=False)
    file.close()
