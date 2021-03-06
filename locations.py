import os
import re
import geocoder


def read_locations(file_name):
    """
    (str) -> list
    Reads data from file and returns list with film name, year and location.
    """
    with open(file_name, 'r', encoding='utf-8', errors='ignore') as file:
        line = file.readline()
        while not line.startswith("="):
            line = file.readline()
        location_list = []
        while line:
            try:
                line = file.readline().strip()
            except EOFError:
                break
            lst = re.split("\t+", line)
            if len(lst) == 3:
                lst = lst[:2]
            name = re.search('\"(.+)\"', lst[0])
            year = re.search('\((\d+?)\)', lst[0])
            if name and year:
                name = name.group(1)
                year = year.group(1)
            else:
                continue
            location_list.append([name, year, lst[1]])
    return location_list


def define_coordinates(location):
    """
    (str) -> list(lat, long)
    Returns coordinates of the location as list [lat, long].
    """
    geo = geocoder.osm(location)
    return geo.latlng


def write_location(name, year, lat, long):
    """
    (str, str, num, num) -> None
    Writes location in file with the same year in the name of the file.
    """
    file_name = 'locations/location_' + year + '.txt'
    file = open(file_name, 'a')
    string_write = name + '\t' + str(lat) + '\t' + str(long) + '\n'
    file.write(string_write)
    file.close()


def main():
    """
    () -> None
    Creates files for each year with films' names and it's coordinates.
    """
    file_name = "locations.list"
    locations_list = read_locations(file_name)
    path = 'locations'
    os.mkdir(path)
    for location in locations_list:
        coordinates = define_coordinates(location[-1])
        if not (coordinates is None):
            write_location(location[0], location[1], coordinates[0], coordinates[1])


if __name__ == "__main__":
    main()
