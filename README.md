![Test](https://github.com/python-sprints/pyntxos/workflows/Test/badge.svg)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/python-sprints/pyntxos-dashboard/master?urlpath=voila%2Frender%2Fdashboard.ipynb)
# pyntxos
Visualization and optimization of pintxo routes for [EuroSciPy 2019](https://www.euroscipy.org/2019/)

## Team 1 - Scrapping

**Goal**: Generate a file `data/data.json` with the information of pintxo restaurants in Bilbao. The format could be:

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

### Instructions
- You will need to `pip install -r scrape_data_requirements.txt` for this part.

### Issues
- Uses `geopy` for get longitude and latitude data but does not have that information for all pintxos
- Change `.travis.yml` so that it does not override the data but "updates" it

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

## Team 4 - Dashboarding

**Goal**: Build an interactive dashboard with the components built by the other teams. Interactive widgets can be used, so the user can specify and adjust the parameters of interest, changing the map and any other component of the dashboard.

Feel free to use any technology you find useful, and add to the dashboard anything you think adds value (images, widgets, text, tables...). Some ideas on the technologies to use:

- [voila](https://github.com/QuantStack/voila)
- [Panel](https://panel.pyviz.org/index.html)
- [ipywidgets](https://ipywidgets.readthedocs.io/en/stable/)

## Team 5 - Continuous Integration

**Goal**: Build a system that automatically fetches the data from the scrapping, the optimization, generates the dashboard, and publishes it online. The idea is that the online dashboard is re-generated with fresh data and features after each commit to master. The system can also validate for every pull request that everything is going to work as expected.

Feel free to use any technology that is useful for the task, some ideas:

- [Azure pipelines](https://azure.microsoft.com/en-us/services/devops/pipelines/)
- [Travis CI](https://travis-ci.org/)
- [Binder](https://mybinder.org/)

Currently we have another [repository](https://github.com/python-sprints/pyntxos-dashboard) for data and dashboard. Every time something is pushed to the current repository, it will run `data.utils.scrape` in [Travis CI](https://travis-ci.org/) then push that new data and the dasboard to the second [repository](https://github.com/python-sprints/pyntxos-dashboard).

- It is unclear if the second repository is needed in the first place, the idea is to keep the data separate but maybe this is not necessary
