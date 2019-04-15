headers = {
    'x-skyscanner-channelid': 'website',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'content-type': 'application/json; charset=UTF-8'
}



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

params = (
    ('geo_schema', 'skyscanner'),
    ('response_include', 'query;deeplink;segment;stats;fqs;pqs')
)

columnsTitles = ['dia_busqueda', 'origen', 'destino', 'hora_salida', 'hora_llegada', 'duracion', 'num_vuelo', 'aerolinea', 'cod_aerolinea', 'precio']