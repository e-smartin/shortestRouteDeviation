import pandas as pd
import openrouteservice as ors
from geopy.geocoders import Nominatim
from geopy.distance import distance
import overpy




#initiate ors client
API_KEY = "api_key"# Replace with your API key
client = ors.Client(key=API_KEY)
# create a geolocator object
geolocator = Nominatim(user_agent="my_app")
    
    
    



def getLatLon(location_name):
    """
        Returns Latitude and Longitude of the given name location
    """
    # get the coordinates of a location
    location = geolocator.geocode(location_name)
    latitude = location.latitude
    longitude = location.longitude

    return latitude, longitude


def find_places_nearby(location, place_name, max_distance):
    """
        Find places near location.
    Args:
        location: location to seek in. 
        place_name: name of the place to find near location.
        max_distance: max distance from location to place.

    Returns
        A list containing longitudes and latitudes of the found places.
    """

    #convert location to lat and long
    lat, lon = getLatLon(location)

    # api overpass def
    api = overpy.Overpass()

    #seek for close locations.
    query = f"""
        node["name"="{place_name}"](around:{max_distance},{lat},{lon});
        out center;
    """
    #retrieve results
    result = api.query(query)
    
    longs_and_lats = [] #array to fill

    #save found places:
    for node_ in result.nodes:
        latitude, longitude = node_.lat , node_.lon
        longs_and_lats.append([float(longitude), float(latitude)])

    return longs_and_lats





def getDistanceAndTime(start, end, profile):
    """
        Distance and time estimation from start to end on selected transport
    Args:    
        start: coordinates of starting point.
        end: coordinates of ending point.
        profile: transportation type
    
    Return:
        list containing distance [m] and time [s] 
    """

    #retrieve data
    coords = [start, end]
    data = client.directions(coordinates=coords,
                              profile=profile,
                              format='geojson')

    route = data['features'][0] # Select the first (and only) feature
    

    # Extract the estimated travel time from the response
    travel_distance = route['properties']['segments'][0]['distance'] # In meters
    travel_time = route['properties']['segments'][0]['duration'] # In seconds
    

    return travel_distance, travel_time


    


def joinAndRemoveDuplicates(places_close_to_end, places_close_to_start):

    # convert each sublist into a tuple 
    places_close_to_end_tuples = [tuple(x) for x in places_close_to_end]
    places_close_to_start_tuples = [tuple(x) for x in places_close_to_start]

    # join tuples without duplicates
    combined_set = set(places_close_to_end_tuples).union(set(places_close_to_start_tuples))

    # convert the set of tuples into a list
    combined_list = [list(x) for x in combined_set]

    return combined_list


def printSol(min_row, time_or_distance):
    """Prints the sol. Created for redability"""

    lon_lat, distance_, time_ = min_row
    lon_, lat_ = lon_lat

    print(f'In terms of {time_or_distance}, the best franchise is:', lat_, lon_)
    print('Estimated total travel time:', "%.2f." % time_, 'seconds')
    print('Estimated total travel distance:', "%.2f." % distance_, 'meters')


def main():

    #ask the usr for the required info
    end_name = input("Introduce the destination\n>")
    start_name = input("Introduce the origin\n>")
    franchise = input("Introduce the franchise name\n>")

    
    #get lat and lon of starting and end points
    start_lat, start_lon = getLatLon(start_name)
    end_lat, end_lon = getLatLon(end_name)
    # correct format
    start_d = [start_lon, start_lat]
    end_d = [end_lon, end_lat]
    

    #find franchises close to end and start
    places_close_to_end = find_places_nearby(end_name, franchise, 10000)
    places_close_to_start = find_places_nearby(start_name, franchise, 10000)
    places_longs_lats = joinAndRemoveDuplicates(places_close_to_end, places_close_to_start)

    #compute distance and time of each of the possible travels
    totals = []
    for place_lon_lat in places_longs_lats:

        #from start to franchise
        transport_type = 'cycling-road' # "driving-car"
        s_distance, s_time = getDistanceAndTime(start_d, place_lon_lat, transport_type )

        #from franchise to end
        e_distance, e_time = getDistanceAndTime(place_lon_lat, end_d,  transport_type)

        #totals
        total_distance = s_distance + e_distance
        total_time = s_time + e_time

        #save
        totals.append([place_lon_lat, total_distance, total_time])


    #get min distance and min time: 
    df = pd.DataFrame(totals, columns = ["lon,lat", "distance", "time"]) #convert to df
    min_d = df.sort_values(by='distance').iloc[0].values #min dist
    min_t = df.sort_values(by='time').iloc[0].values #min time

    #print sols:
    print("\n"*3)
    printSol(min_d, "distance")
    print("---"*20)
    printSol(min_t, "time")



if __name__ == '__main__' :
    main()

