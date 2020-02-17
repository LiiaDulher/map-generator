import folium
import os
import math
import heapq


class Point(object):
    def __init__(self, title, lat, long, distance):
        self.title = title
        self.lat = lat
        self.long = long
        self.distance = distance

    def __gt__(self, right):
        return self.distance > right.distance

    def __le__(self, right):
        return self.distance < right.distance

    def __eq__(self, right):
        return self.distance == right.distance

    def __str__(self):
        return "{} {} {} {}".format(self.title, self.lat, self.long, self.distance)

    def __repr__(self):
        return "{} {} {} {}".format(self.title, self.lat, self.long, self.distance)


def read_data():
    """
    () -> str, num, num
    Reads year and location of the user.
    """
    print("Please enter a year you would like to have a map for:")
    year = input()
    while True:
        try:
            year = int(year)
            break
        except ValueError:
            print("Wrong year. Please enter the year again:")
            year = input()
    print("Please enter your location (format: lat, long):")
    location = input().split(",")
    lat, long = float(location[0]), float(location[1])
    return str(year), lat, long


def population_layer():
    """
    () -> FeatureGroup
    Creates layer with population and returns it.
    """
    fg_pp = folium.FeatureGroup(name="Population")
    fg_pp.add_child(folium.GeoJson(data=open('world.json', 'r',
                                             encoding='utf-8-sig').read(),
                                   style_function=lambda x: {'fillColor': 'green'
                                   if x['properties']['POP2005'] < 10000000
                                   else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
                                   else 'red'}))
    return fg_pp


def calculate_distance(loc1, loc2):
    """
    (list, list) -> num
    Calculates distance between two locations.
    """
    return math.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)


def find_locations(year, lat, long):
    """
    (str, list) -> list
    Returns list of 10 or less nearest locations.
    """
    if not ("locations" in os.listdir()):
        os.system('python locations.py')
    file_name = 'locations/location_' + year + '.txt'
    if os.path.exists(file_name):
        print('found')
        with open(file_name) as file:
            data = file.readlines()
            locations_heap = []
            for line in data:
                line = line.strip()
                loc = line.split("\t")
                loc_point = Point(loc[0], float(loc[1]), float(loc[2]),
                                  (-1) * calculate_distance([float(loc[1]), float(loc[2])], [lat, long]))
                if len(locations_heap) < 10:
                    heapq.heappush(locations_heap, loc_point)
                else:
                    if loc_point.distance > locations_heap[0].distance:
                        heapq.heapreplace(locations_heap, loc_point)
        return locations_heap
    return None


def locations_layer(loc_heap):
    """
    (list) -> FeatureGroup
    Creates layer with locations in the list and returns it.
    """
    fg_loc = folium.FeatureGroup(name="Film's_locations")
    for loc_point in loc_heap:
        fg_loc.add_child(folium.Marker(location=[loc_point.lat, loc_point.long],
                                       popup=loc_point.title, icon=folium.Icon()))
    return fg_loc


def main():
    """
    Generates map with 3 layers.
    """
    year, lat, long = read_data()
    print("Map is generating...")
    print("Please wait...")
    world_map = folium.Map(location=[lat, long], zoom_start=10)
    world_map.add_child(folium.Marker(location=[lat, long], popup="Your location", icon=folium.Icon()))
    fg_pp = population_layer()
    world_map.add_child(fg_pp)
    loc_heap = find_locations(year, lat, long)
    if not (loc_heap is None):
        fg_loc = locations_layer(loc_heap)
        world_map.add_child(fg_loc)
        world_map.add_child(folium.LayerControl())
    map_name = "Map_" + str(year) + ".html"
    world_map.save(map_name)
    print("Finished. Please have look at the map", map_name)


if __name__ == "__main__":
    main()
