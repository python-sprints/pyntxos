# pyntxos
Visualization and optimization of pintxo routes at EuroSciPy 2019

## Team 1 - Scrapping

Goal: Generate a file `data/bilbao_restaurants.json` with the information of pintxo restaurants in Bilbao. The format could be:

```json
[{"name": "Argotia",
  "latitude": 43.2590929,
  "longitude": -2.9244257,
  "address": "Plaza Nueva, 48005 Bilbao, Vizcaya, Spain"},
 {"name": "Sorginzulo",
  "latitude": 43.259387,
  "longitude": -2.9233905,
  "address": "Plaza Nueva, 12, 48005 Bilbao, BI, Spain"}
]
```

Feel free to use any source of data you find, and any technology you find useful. Some suggestions:

Data sources:

- <http://www.bilbaoturismo.net/BilbaoTurismo/en/pintxo-finder/>
- [Tripadvisor](https://www.tripadvisor.co.uk/Restaurants-g187454-Bilbao_Province_of_Vizcaya_Basque_Country.html)
- Google maps
- [Google geoencoding API](https://developers.google.com/maps/documentation/geocoding/start)

Technologies:

- <https://scrapy.org/>
- <https://3.python-requests.org/>
