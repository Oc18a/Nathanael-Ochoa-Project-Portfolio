# DSC 510
# Week 12
# Course Project: The following program interacts with a webservice to obtain weather data for the user's desired
#   location. The user can search up an area's weather by using the city name and state code, or by entering a
#   ZIP/postal code. The searches are limited to the U.S. A user will also be able to specify the units of measurement.
#   A user is also able to make as many searches as they please back-to-back. There are also checks in place to ensure
#   only valid input is entered. Enjoy!
# Author: Nathanael Ochoa
# 11/18/2023
import requests
import sys
api_key = "2ef25b6986997cf83162b5b273a78940"  # Api key that is stored in a global variable


# Lines 15-141 are used by the city search option
# Function that removes any whitespace from the user's city name input and returns the new name.
def city_whitespace_check(city):
    city_list = city.split()
    city_checked = " ".join(city_list)
    return city_checked


# Function that removes any whitespace from the user's state code input and returns the new code.
def state_whitespace_check(state):
    state_list = state.split()
    state_checked = "".join(state_list)
    return state_checked


# The geo_code_lookup function uses the user's entered city name and state code and returns the lat and lon coordinates
# from the api.
def geocode_lookup(city, state):
    api_link = ("http://api.openweathermap.org/geo/1.0/direct?q={city_filler},{state_filler},US&appid=" + api_key)
    try:
        geo_response = requests.get(api_link.format(city_filler=city, state_filler=state))
    except requests.exceptions.HTTPError:
        sys.exit("There was an HTTP error. Please try again.")
    except requests.exceptions.TooManyRedirects:
        sys.exit("Too many redirects.")
    except requests.exceptions.InvalidURL:
        sys.exit("The URL provided was invalid. Please double-check the URL.")
    except requests.exceptions.Timeout:
        sys.exit("Your request time out. Please try again.")
    except requests.ConnectionError:
        sys.exit("A connection error occurred.")
    except requests.exceptions.MissingSchema:
        sys.exit("Invalid URL '{link_filler}': No schema supplied.".format(link_filler=api_link
                                                                           .format(city_filler=city,
                                                                                   state_filler=state)))
    except requests.exceptions.InvalidSchema:
        sys.exit("No connection adapters were found for '{link_filler}'".format(link_filler=api_link
                                                                                .format(city_filler=city,
                                                                                        state_filler=state)))
    except requests.exceptions.RequestException:
        sys.exit("There was inexact error that occurred while handling your request. Please try again.")
    geo_response_data = geo_response.json()  # Sets the json data to a variable.
    return geo_response_data  # json variable is returned.


# The city_data_cleanup function retrieves the necessary data from the json data and displays it in a "pretty" format.
def city_data_cleanup(data, city, state, units):
    data_city_name = data["name"]
    data_desc = data["weather"][0]["description"]
    data_temp = data["main"]["temp"]
    data_feels = data["main"]["feels_like"]
    data_max_temp = data["main"]["temp_max"]
    data_min_temp = data["main"]["temp_min"]
    data_pressure = data["main"]["pressure"]
    data_humidity = data["main"]["humidity"]
    data_wind = data["wind"]["speed"]
    data_clouds = data["clouds"]["all"]
    # Lines 89-97 set variables equal to the proper unit symbols
    if units == "imperial":
        unit_symbol = "\xb0F"  # Degrees fahrenheit
        unit_speed = " mph"  # Miles per hour
    elif units == "metric":
        unit_symbol = "\xb0C"  # Degrees celsius
        unit_speed = " m/s"  # meters per second
    else:
        unit_symbol = " K"  # Kelvin
        unit_speed = " m/s"  # meters per second
    print()
    print("You entered: " + city + ", " + state)
    print("Weather data was retrieved for: " + data_city_name + ", " + state.upper())
    print("-------------------------------")
    print("Description: " + data_desc)
    print("Current temperature: {temp_filler}{symbol_filler}".format(temp_filler=data_temp, symbol_filler=unit_symbol))
    print("Feels like: {feel_filler}{symbol_filler}".format(feel_filler=data_feels, symbol_filler=unit_symbol))
    print("Highest temperature: {max_filler}{symbol_filler}".format(max_filler=data_max_temp,
                                                                    symbol_filler=unit_symbol))
    print("Lowest temperature: {min_filler}{symbol_filler}".format(min_filler=data_min_temp, symbol_filler=unit_symbol))
    print("Pressure: {pressure_filler} hPa".format(pressure_filler=data_pressure))
    print("Humidity: {humid_filler} %".format(humid_filler=data_humidity))
    print("Wind speed: {speed_filler}{speed_symbol_filler}".format(speed_filler=data_wind,
                                                                   speed_symbol_filler=unit_speed))
    print("Cloudiness: {cloud_filler} %".format(cloud_filler=data_clouds))
    try:
        data_rain_1h = data["rain"]["1h"]
        print("Rain volume for the last hour: {rain_filler} mm".format(rain_filler=data_rain_1h))
        try:
            data_rain_3h = data["rain"]["3h"]
            print("Rain volume for the last 3 hours: {rain_filler} mm".format(rain_filler=data_rain_3h))
        except KeyError:
            pass
    except KeyError:
        pass
    try:
        data_snow_1h = data["snow"]["1h"]
        print("Snow volume for the last hour: {snow_filler} mm".format(snow_filler=data_snow_1h))
        try:
            data_snow_3h = data["snow"]["3h"]
            print("Snow volume for the last 3 hours: {snow_filler} mm".format(snow_filler=data_snow_3h))
        except KeyError:
            pass
    except KeyError:
        pass


# City_w_search is the "control center" for the city/state search option
def city_w_search():
    city_name_input = input("Enter a city: ")
    state_code_input = input("Enter a valid state code: ")
    while True:  # While loop used to ensure only valid input is entered to move on.
        # Lines 142 and 143 are both function calls that return a modified version of the city name and state code.
        # The returned names are stored into new variables and the functions called remove any whitespace the user's
        # input may have.
        city_name_new = city_whitespace_check(city_name_input)
        state_code_new = state_whitespace_check(state_code_input)
        geo_data = geocode_lookup(city_name_new, state_code_new)
        units = units_of_measurement()  # Calls the unit function and return is stored into 'units'
        try:
            latitude = geo_data[0]["lat"]
            longitude = geo_data[0]["lon"]
            # weather_data stored the data from the weather_search function call.
            weather_data = weather_search(latitude, longitude, units)
            city_data_cleanup(weather_data, city_name_new, state_code_new, units)  # Pretty output function call
            break
        except IndexError:  # Catches an IndexError and will ask the user to re-input their desired city/state info.
            print("\nThere may have been a typo or the city entered does not exist. Please try again.")
            city_name_input = input("Re-enter a city: ")
            state_code_input = input("Re-enter a valid state code: ")
            continue


# Lines 163-272 are used by the zip search option.
# The geo_code_lookup function uses the user's entered zip code and returns the lat and lon coordinates from the api.
def geocode_zip_lookup(zipcode):
    api_link = ("http://api.openweathermap.org/geo/1.0/zip?zip={zip_filler},US&appid=" + api_key)
    try:
        geo_response = requests.get(api_link.format(zip_filler=zipcode))
    except requests.exceptions.HTTPError:
        sys.exit("There was an HTTP error. Please try again.")
    except requests.exceptions.TooManyRedirects:
        sys.exit("Too many redirects.")
    except requests.exceptions.InvalidURL:
        sys.exit("The URL provided was invalid. Please double-check the URL.")
    except requests.exceptions.Timeout:
        sys.exit("Your request time out. Please try again.")
    except requests.ConnectionError:
        sys.exit("A connection error occurred.")
    except requests.exceptions.MissingSchema:
        sys.exit("Invalid URL '{link_filler}': No schema supplied.".format(link_filler=api_link
                                                                           .format(zip_filler=zipcode)))
    except requests.exceptions.InvalidSchema:
        sys.exit("No connection adapters were found for '{link_filler}'".format(link_filler=api_link
                                                                                .format(zip_filler=zipcode)))
    except requests.exceptions.RequestException:
        sys.exit("There was inexact error that occurred while handling your request. Please try again.")
    geo_response_data = geo_response.json()  # Sets the json data to a variable.
    return geo_response_data  # json variable is returned.


# The zip_data_cleanup function retrieves the necessary data from the json data and displays it in a "pretty" format.
def zip_data_cleanup(data, zipcode, units):
    data_city_name = data["name"]
    data_desc = data["weather"][0]["description"]
    data_temp = data["main"]["temp"]
    data_feels = data["main"]["feels_like"]
    data_max_temp = data["main"]["temp_max"]
    data_min_temp = data["main"]["temp_min"]
    data_pressure = data["main"]["pressure"]
    data_humidity = data["main"]["humidity"]
    data_wind = data["wind"]["speed"]
    data_clouds = data["clouds"]["all"]
    # Lines 198-206 set variables equal to the proper unit symbols
    if units == "imperial":
        unit_symbol = "\xb0F"  # Degrees fahrenheit
        unit_speed = " mph"  # Miles per hour
    elif units == "metric":
        unit_symbol = "\xb0C"  # Degrees celsius
        unit_speed = " m/s"  # Meters per second
    else:
        unit_symbol = " K"  # Kelvin
        unit_speed = " m/s"  # Meters per second
    print()
    print("You entered: " + zipcode)
    print("Weather data was retrieved for: " + data_city_name)
    print("-------------------------------")
    print("Description: " + data_desc)
    print("Current temperature: {temp_filler}{symbol_filler}".format(temp_filler=data_temp, symbol_filler=unit_symbol))
    print("Feels like: {feel_filler}{symbol_filler}".format(feel_filler=data_feels, symbol_filler=unit_symbol))
    print("Highest temperature: {max_filler}{symbol_filler}".format(max_filler=data_max_temp,
                                                                    symbol_filler=unit_symbol))
    print("Lowest temperature: {min_filler}{symbol_filler}".format(min_filler=data_min_temp, symbol_filler=unit_symbol))
    print("Pressure: {pressure_filler} hPa".format(pressure_filler=data_pressure))
    print("Humidity: {humid_filler} %".format(humid_filler=data_humidity))
    print("Wind speed: {speed_filler}{speed_symbol_filler}".format(speed_filler=data_wind,
                                                                   speed_symbol_filler=unit_speed))
    print("Cloudiness: {cloud_filler} %".format(cloud_filler=data_clouds))
    try:  # Retrieves this data in the case it is available in the json data.
        data_rain_1h = data["rain"]["1h"]
        print("Rain volume for the last hour: {rain_filler} mm".format(rain_filler=data_rain_1h))
        try:
            data_rain_3h = data["rain"]["3h"]
            print("Rain volume for the last 3 hours: {rain_filler} mm".format(rain_filler=data_rain_3h))
        except KeyError:
            pass
    except KeyError:
        pass
    try:  # Retrieves this data in the case it is available in the json data.
        data_snow_1h = data["snow"]["1h"]
        print("Snow volume for the last hour: {snow_filler} mm".format(snow_filler=data_snow_1h))
        try:
            data_snow_3h = data["snow"]["3h"]
            print("Snow volume for the last 3 hours: {snow_filler} mm".format(snow_filler=data_snow_3h))
        except KeyError:
            pass
    except KeyError:
        pass


# Zipcode_w_search is the "control center" for the zip search option.
def zipcode_w_search():
    zip_code_input = input("Enter a ZIP/postal code: ")
    while True:  # While loop used to ensure only valid input is entered to move on.
        try:
            if isinstance(int(zip_code_input), int):
                break  # Do nothing, just making sure zip entered is strictly an integer
        except ValueError:  # In the case the value is not an int, ask for input again.
            print("\nThere may have been a typo or a nonnumerical value was entered. Please try again.")
            zip_code_input = input("Re-enter a ZIP/postal code: ")
            continue
    while True:
        # Lines 259 and 260 are both function calls that return data. The data is then stored into variables.
        geo_data = geocode_zip_lookup(zip_code_input)  # geo_data is the variable.
        units = units_of_measurement()  # units is the variable.
        try:
            latitude = geo_data["lat"]
            longitude = geo_data["lon"]
            # Weather_data stores the data from the weather_search function call.
            weather_data = weather_search(latitude, longitude, units)
            zip_data_cleanup(weather_data, zip_code_input, units)  # Function call that makes the output pretty.
            break
        except KeyError:  # Catches a KeyError and will ask the user to re-input their desired zip code.
            print("\nThe entered ZIP/postal code was not found.")
            zip_code_input = input("Please enter an existing ZIP/postal code: ")
            continue


# Lines 275-323 are used by BOTH search options.
# Gets the units from the user and is passed on to weather_search.
def units_of_measurement():
    while True:  # While loop used to ensure only valid input is entered to move on.
        units_chosen = input("Enter a 'K' for Kelvin, an 'F' for Fahrenheit, or a 'C' for Celsius: ")
        if units_chosen == "K" or units_chosen == "k":
            units = "kelvin"
            break
        elif units_chosen == "F" or units_chosen == "f":
            units = "imperial"
            break
        elif units_chosen == "C" or units_chosen == "c":
            units = "metric"
            break
        else:
            print("ONLY the 3 options below are accepted. Please try again.")
            continue
    return units  # Returns the units chosen by the user.


# weather_search retrieves the weather data by using the latitude, longitude, and units.
def weather_search(lat, lon, units):
    api_link = ("https://api.openweathermap.org/data/2.5/weather?lat={lat_filler}&lon={lon_filler}&appid=" + api_key)
    try:  # The appropriate unit ending is added depending on the value passed into weather_search.
        if units == "imperial":
            weather_response = requests.get(api_link.format(lat_filler=lat, lon_filler=lon) + "&units=imperial")
        elif units == "metric":
            weather_response = requests.get(api_link.format(lat_filler=lat, lon_filler=lon) + "&units=metric")
        else:
            weather_response = requests.get(api_link.format(lat_filler=lat, lon_filler=lon))
    except requests.exceptions.HTTPError:
        sys.exit("There was an HTTP error. Please try again.")
    except requests.exceptions.TooManyRedirects:
        sys.exit("Too many redirects.")
    except requests.exceptions.InvalidURL:
        sys.exit("The URL provided was invalid. Please double-check the URL.")
    except requests.exceptions.Timeout:
        sys.exit("Your request time out. Please try again.")
    except requests.ConnectionError:
        sys.exit("A connection error occurred.")
    except requests.exceptions.MissingSchema:
        sys.exit("Invalid URL '{link_filler}': No schema supplied.".format(link_filler=api_link.format(lat_filler=lat,
                                                                                                       lon_filler=lon)))
    except requests.exceptions.InvalidSchema:
        sys.exit("No connection adapters were found for '{link_filler}'".format(link_filler=api_link
                                                                                .format(lat_filler=lat,
                                                                                        lon_filler=lon)))
    except requests.exceptions.RequestException:
        sys.exit("There was inexact error that occurred while handling your request. Please try again.")
    weather_response_data = weather_response.json()  # Sets the json data to a variable.
    return weather_response_data  # json variable is returned.


def main():
    print("""
    Hello! This program uses 2 API's from OpenWeatherMap to retrieve the current weather of the location that you enter. 
    You can start a search by entering a city's name or a ZIP/postal code. When searching by city you must specify the 
    state (state code) the city is located in. For example: 'CA' for California. You will also be required to choose the 
    temperature's unit of measurement (Kelvin, Fahrenheit, or Celsius).
    """)
    choice = input("Choose search type. Enter a 'C' for city or a 'Z' for ZIP/postal code: ")
    while True:  # While loop used to ensure only valid input is entered to move on.
        print()  # Blank space.
        if choice == "C" or choice == "c":  # First option for user.
            city_w_search()  # Calls the function that handles the city search.
            another_search = input("Would you like to search another (enter 'Y' or 'N')? ")
            while True:  # While loop used to ensure only 'y' or 'n' are entered.
                if another_search == "Y" or another_search == "y":
                    break
                elif another_search == "N" or another_search == "n":
                    break
                else:
                    print("\nOnly 'Y' and 'N' are valid inputs.")
                    another_search = input("Please try again: ")
                    continue
            if another_search == "Y" or another_search == "y":  # Starts the main loop over again.
                choice = input("\nChoose search type again. Enter a 'C' for city or a 'Z' for ZIP/postal code: ")
                continue
            elif another_search == "N" or another_search == "n":  # Ends the program.
                print("Goodbye! Thank you!")
                break
        elif choice == "Z" or choice == "z":
            zipcode_w_search()  # Calls the function that handles the zip search.
            another_search = input("Would you like to search another (enter 'Y' or 'N')? ")
            while True:  # While loop used to ensure only 'y' or 'n' are entered.
                if another_search == "Y" or another_search == "y":
                    break
                elif another_search == "N" or another_search == "n":
                    break
                else:
                    print("\nOnly 'Y' and 'N' are valid inputs.")
                    another_search = input("Please try again: ")
                    continue
            if another_search == "Y" or another_search == "y":  # Starts the main loop over again.
                choice = input("\nChoose search type again. Enter a 'C' for city or a 'Z' for ZIP/postal code: ")
                continue
            elif another_search == "N" or another_search == "n":  # Ends the program.
                print("Goodbye! Thank you!")
                break
        else:
            print("Only 'C' and 'Z' are valid input.")
            choice = input("Please try again: ")
            continue


if __name__ == "__main__":
    main()
