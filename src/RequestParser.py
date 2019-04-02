import requests
import json
import datetime

def generateRequest(org,dest,date):
    validateArguments(org,dest,date)
    for city in cities:
        if city["name"] == org:
            origin = city
        if city["name"] == dest:
            destination = city
    data = setData(origin, destination,date)
    return requests.post(URL, headers=headers, params=params, data=data)
      
def validateArguments(org,dest,date):
    if org == dest:
        raise Exception('Origin and destination can not be the same city')
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

def setData (origin, destination, date):
    data_json = json.loads(dataScheme)
    data_json["legs"][0]["origin"] = origin["id"]
    data_json["legs"][0]["destination"] = destination["id"]
    data_json["legs"][0]["date"] = date
    data_json["outboundDate"] = date
    data_json["destination"] = destination
    data_json["origin"] = origin
    data = json.dumps(data_json)
    return data

headers = {
    'x-skyscanner-channelid': 'website',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'content-type': 'application/json; charset=UTF-8'
}

params = (
    ('geo_schema', 'skyscanner'),
    ('response_include', 'query;deeplink;segment;stats;fqs;pqs')
)

dataScheme = '{"market":"UK","currency":"GBP","locale":"en-GB","cabin_class":"economy","prefer_directs":true,"trip_type":"one-way","legs":[{"origin":"","destination":"","date":"","add_alternative_origins":false,"add_alternative_destinations":false}],"origin":{},"destination":{},"outboundDate":"2019-03-31","adults":1,"child_ages":[],"options":{"include_unpriced_itineraries":true,"include_mixed_booking_options":true},"state":{}}'

URL = 'https://www.skyscanner.net/g/conductor/v1/fps3/search/'

cities = [
    {"id":"MAD","name":"Madrid","cityId":"MADR","cityName":"Madrid","countryId":"ES","type":"City","centroidCoordinates":[-3.563333,40.472222]},
    {"id":"BCN","name":"Barcelona","cityId":"BARC","cityName":"Barcelona","countryId":"ES","type":"City","centroidCoordinates":[2.094444,41.302778]},
    {"id":"LOND","name":"London","cityId":"LOND","cityName":"London","countryId":"UK","type":"City","centroidCoordinates":[-0.0943465343,51.5041174139]},
    {"id":"PARI","name":"Paris","cityId":"PARI","cityName":"Paris","countryId":"FR","type":"City","centroidCoordinates":[2.3445033204,48.8600102994]},
    {"id":"ROME","name":"Rome","cityId":"ROME","cityName":"Rome","countryId":"IT","type":"City","centroidCoordinates":[12.4908803859,41.8904833603]},
    {"id":"LIS","name":"Lisbon","cityId":"LISB","cityName":"Lisbon","countryId":"PT","type":"City","centroidCoordinates":[-9.133333,38.781944]},
    {"id":"AMS","name":"Amsterdam","cityId":"AMST","cityName":"Amsterdam","countryId":"NL","type":"City","centroidCoordinates":[4.768056,52.308333]},
    {"id":"BERL","name":"Berlin","cityId":"BERL","cityName":"Berlin","countryId":"DE","type":"City","centroidCoordinates":[13.4245185552,52.4865621581]},
    {"id":"ZRH","name":"Zurich","cityId":"ZURI","cityName":"Zurich","countryId":"CH","type":"City","centroidCoordinates":[8.551667,47.458333]},
    {"id":"BRUS","name":"Brussels","cityId":"BRUS","cityName":"Brussels","countryId":"BE","type":"City","centroidCoordinates":[4.3592416078,50.8384245708]},
    {"id":"DUB","name":"Dublin","cityId":"DUBL","cityName":"Dublin","countryId":"IE","type":"City","centroidCoordinates":[-6.252222,53.4325]},
    {"id":"VIE","name":"Vienna","cityId":"VIEN","cityName":"Vienna","countryId":"AT","type":"City","centroidCoordinates":[16.55751,48.1221]}
]