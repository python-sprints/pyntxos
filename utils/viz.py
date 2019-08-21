import folium


def make_and_save_map(data, num_restaurants=None, phone_number=False):

    m = folium.Map(location=[43.2590929, -2.9244257])  # , zoom_start=20)

    tooltip = "Click me!"

    if num_restaurants:
        if not isinstance(num_restaurants, int):
            raise ValueError("`num_restaurants` must be integer or None!")

    if isinstance(num_restaurants, int):
        if num_restaurants < 1:
            raise ValueError("`num_restaurants` must be at least 1!")

    if num_restaurants:
        data = data[:num_restaurants]

    popup = "<i>{name}</i>\n{address}"
    if phone_number:
        popup += "\n+34 {number}"

    for i in data:
        folium.Marker(
            [i["latitude"], i["longitude"]],
            popup=popup.format(
                name=i["name"],
                address=i["address"],
                number=i["telephone"].replace(" ", ""),
            ),
            tooltip=tooltip,
        ).add_to(m)

    for n in range(len(data) - 1):
        folium.ColorLine(
            [
                (data[n]["latitude"], data[n]["longitude"]),
                (data[n + 1]["latitude"], data[n + 1]["longitude"]),
            ],
            [1],
            weight=3,
            colormap=["green", "red"],
        ).add_to(m)
    m.fit_bounds(
        [
            [min([i["latitude"] for i in data]), min([i["longitude"] for i in data])],
            [max([i["latitude"] for i in data]), max([i["longitude"] for i in data])],
        ]
    )

    return m
