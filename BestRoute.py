"""" Find the combination of cities which yields the lowest high temperature average over 5 days """
import requests
import json
from itertools import permutations


API_KEY = "9cb42201524dd1ed902e26aa1421e1c2"
WS_URL = "https://api.openweathermap.org/data/2.5/forecast"


class City:
    """ Contains the name of the city and its max temp for the next 5 days """
    def __init__(self, name, temperatures):
        self.name = name
        self.temps = temperatures

    def get_temperature(self, day):
        """ Returns maximum forecasted temperature for specified day """
        return self.temps[day]

    def __str__(self):
        return self.name


class Route:
    """ A route represents a sequence of cities """
    def __init__(self, city_route):
        # assuming cities is a list containing 5 City objects
        self.city_list = city_route

    def route_avg(self):
        """ Returns the average of the temperatures for each city in the Route's order """
        temps = [self.city_list[x].get_temperature(x) for x in range(len(self.city_list))]
        avg = sum(temps) / len(self.city_list)
        return avg

    def __str__(self):
        """ Returns the names of the cities of the City objects in the Route in order """
        names = [self.city_list[x].name for x in range(len(self.city_list))]
        sep = ', '
        return sep.join(names)


def fetch_weather(id):
    # request parameter(s): Start with '?'
    # separate name and value with '='
    # multiple parameter name value pairs are separate with '&'
    query_string = "?id={}&units=imperial&APIKEY={}".format(id, API_KEY)
    request_url = WS_URL + query_string
    response = requests.get(request_url)
    if response.status_code == 200:
        d = response.json()
        city_name = d["city"]['name']
        lst = d['list']
        # li = [[x for x in range(len(lst)) if x // 8 == i] for i in range(len(lst) // 8)]
        tmp_list = [] # [[[max([lst[j]["main"]['temp_max']]) for j in k] for k in li[l]] for l in range(len(li))]
        for i in range(len(lst) // 8):
            li = [x for x in range(len(lst)) if x // 8 == i]
            tmp_list.append(max([lst[j]["main"]["temp_max"] for j in li]))
        return City(city_name, tmp_list)
    else:
        print("How should I know?")
        return None


if __name__ == "__main__":
    id_list = json.loads(open("cities.json").read())
    cities = [fetch_weather(id) for id in id_list]
    plist = list(permutations(range(5)))
    # creating the list of all permutations of City objects
    c_routes = [[cities[a] for a in plist[b]] for b in range(len(plist))]
    # creating the list of Route objects from the previous list, and sort by lowest avg temp
    routes = sorted([Route(c_routes[b]) for b in range(len(c_routes))], key=lambda x: x.route_avg())
    # finally, print the lowest average and its associated Route
    print(f"The lowest average temperature high of {round(routes[0].route_avg(), 2)} is forecast for this route:")
    print(routes[0])
