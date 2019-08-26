import folium


def get_map(data, route=None):

    if route is None:
        route = data

    m = folium.Map(location=[43.2590929, -2.9244257])  # , zoom_start=20)

    for index, item in enumerate(data):

        if index in route:
            tooltip = f'{route.index(index)+1}-{item["name"]}'
            icon = folium.features.Icon(color='red')
        else:
            tooltip = item['name']
            icon = None

        folium.features.Marker(
            [item['latitude'], item['longitude']],
            popup=f'<b>{item["name"]}</b><br>{item["address"]}<br>+34 {item["telephone"]}',
            tooltip=tooltip,
            icon=icon,
        ).add_to(m)

    line = [[data[item]['latitude'], data[item]['longitude']] for item in route]

    folium.features.ColorLine(
        line,
        colors=list(range(len(line)-1)),
        weight=5,
    ).add_to(m)

    lat_long = list(map(list, zip(*line)))
    m.fit_bounds(
        [
            [min(lat_long[0]), min(lat_long[1])],
            [max(lat_long[0]), max(lat_long[1])],
        ]
    )

    return m
