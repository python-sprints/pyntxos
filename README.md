# pyntxos
Visualization and optimization of pintxo routes for [EuroSciPy 2019](https://www.euroscipy.org/2019/)

## Team 1 - Scrapping

**Goal**: Generate a file `data/bilbao_restaurants.json` with the information of pintxo restaurants in Bilbao. The format could be:

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

## Team 2 - Geovisualization

**Goal**: Display visually in a map a set of points (restaurants) and a path (straight lines among the points) given the ordered list of data.

The visualization should use the data computed by the other teams, and should run in a Jupyter notebook. Feel free to use any technology you find useful, some ideas:

- [GeoViews](http://geoviews.org/)
- [GeoPandas](http://geopandas.org/)
- [gmplot](https://github.com/vgm64/gmplot)
- [Folium](https://github.com/python-visualization/folium)

## Team 3 - Optimization

**Goal**: Given a set of geolocations (latitude and longitude of restaurants), compute an optimal path among them. The cost function doesn't necessarily need to optimize for the shortest path, and can be constrained by the number of maximum restaurants, or include other information like the pricing, reviews... The optimization can also receive parameters, like the finishing point (the hotel where people will sleep after the pintxo routes), budget or any other.

Feel free to use any technology you find useful, some ideas:

- [scipy.optimise](https://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html)
- <https://cvxopt.org/>
- <https://www.cvxpy.org/>
- [PuLP](https://github.com/coin-or/pulp)
- [Pyomo](http://www.pyomo.org/)
