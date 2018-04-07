from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as Soup
from functools import reduce
import operator
import re
import requests
import sys


PATTERN = re.compile('^[A-Za-z]{3}$')
FLIGHT_PRICE = re.compile('^[0-9]+')
AIRLINE = re.compile('^(delta|united|american)$', re.IGNORECASE)
FARE_CLASS = re.compile('^[A-Za-z]{1}$')
URL = "http://www.webflyer.com/travel/mileage_calculator/getmileage.php?{url_params}"
FARE_CLASS_MULTIPLIER_DICTIONARY = {
'Delta':
    {
      'N': 0,

      'E': 1,
      'H': 1,
      'K': 1,
      'L': 1,
      'M': 1,
      'Q': 1,
      'S': 1,
      'T': 1,
      'U': 1,
      'V': 1,
      'W': 1,
      'X': 1,

      'A': 1.5,
      'B': 1.5,
      'C': 1.5,
      'D': 1.5,
      'G': 1.5,
      'I': 1.5,
      'P': 1.5,
      'Y': 1.5,
      'Z': 1.5,

      'F': 2,
      'J': 2,
    },
'United':
    {
      'N': 0,

      'M': 1,
      'E': 1,
      'U': 1,
      'H': 1,
      'Q': 1,
      'V': 1,
      'W': 1,
      'S': 1,
      'T': 1,
      'L': 1,
      'K': 1,
      'G': 1,

      'Y': 1.5,
      'B': 1.5,

      'A': 2,
      'C': 2,
      'D': 2,
      'Z': 2,
      'P': 2,
      'F': 3,
      'J': 3,
    },
'American':
    {
      'B': 0,

      'H': 1,
      'K': 1,
      'M': 1,
      'L': 1,
      'V': 1,
      'G': 1,
      'S': 1,
      'N': 1,
      'Q': 1,
      'O': 1,

      'Y': 1.5,
      'W': 1.5,
      'P': 1.5,

      'A': 2,
      'D': 2,
      'I': 2,
      'R': 2,

      'F': 3,
      'J': 3,
    }
}


def is_valid_airport_code(codes):
    return bool(PATTERN.search(codes))


def validate_code(codes):
    return is_valid_airport_code(codes) and len(codes) == 3


def is_valid_flight_cost(valid_flight_cost):
    return bool(FLIGHT_PRICE.search(valid_flight_cost))


def validate_flight_cost(valid_flight_cost):
    return is_valid_flight_cost(valid_flight_cost) and len(valid_flight_cost) >= 2


def is_valid_airline(valid_airline_name):
    return bool(AIRLINE.search(valid_airline_name))


def validate_airline(valid_airline_name):
    return is_valid_airline(valid_airline_name) and len(valid_airline_name) >= 5


def is_valid_fare_class(fare_class):
    return bool(FARE_CLASS.search(fare_class))


def validate_fare_class(fare_class):
    return is_valid_fare_class(fare_class) and len(fare_class) == 1


# Prompts the user for their airports codes as a comma separated string, must be a least two, no more than five.
def get_codes(airport_user_input):
    codes = [c.strip() for c in airport_user_input.split(',')]
    if len(codes) > 5:
        print("You entered {}, max is 5 airport codes".format(len(codes)))
        sys.exit(1)
    elif len(codes) < 2:
        print('You must enter at least 2 codes separated by commas: i.e. lax, sjc')
        sys.exit(1)
    elif not all([validate_code(x) for x in codes]):
        print("All codes must be alphanumeric and 3 digits. You passed in {}".format(codes))
        sys.exit(1)
    print("-- Found properly formatted airport codes: {}".format(codes))
    return codes


# Passes the collected airport codes as a URL query, if 200 code not returned an exception is raised.
def get_city_data(codes):
    params = '&'.join(['city={}'.format(c) for c in codes])
    url = URL.format(url_params=params)
    page_html = requests.get(url)
    if page_html.status_code == 200:
        return page_html.content
    raise Exception('We are unable to query the mileage data at the moment, sorry.')


# Returns the total flight miles as an integer from the HTML parse.
def get_miles_from_html(page_html):
    page_extract = Soup(page_html, "html.parser")
    try:
        table_data = page_extract.find("table", attrs={"class": "table_bg"})
        # On the website the round-trip mileage is stored in a table, it is extracted at the -2 table index.
        flight_mileage = re.search('[0-9]+', table_data.findAll("td")[-2].text)
    except AttributeError:
        raise sys.exit("Error, your airport codes could not be validated")
    else:
        return int(flight_mileage.group())


# Checks for a properly formatted flight cost.
def get_flight_cost(flight_cost_input):
    valid_flight_cost = flight_cost_input.strip('$')
    if len(valid_flight_cost) <= 1:
        print("Please input a flight price greater than $10")
        sys.exit(1)
    elif len(valid_flight_cost) >= 4:
        print("Please input a flight price less than $1,000")
        sys.exit(1)
    elif not validate_flight_cost(valid_flight_cost):
        print("Please use only whole numbers with no symbols or commas")
        sys.exit(1)
    print("-- Flight cost stored: ${}".format(valid_flight_cost))
    return valid_flight_cost


# Returns the airline name if the input matches values; Delta, United, or American.
def get_airline(airline_input):
    valid_airline_name = airline_input.capitalize()
    if not validate_airline(valid_airline_name):
        print("Please input either; Delta, United, or American")
        sys.exit(1)
    print("-- Airline name stored: {}".format(valid_airline_name))
    return valid_airline_name


# Returns fare class character [key] to later lookup the corresponding value [multiplier].
def get_fare_class(fare_class_input):
    fare_class = fare_class_input.upper()
    if len(fare_class) != 1:
        print("You may only enter a single letter for your fare class; i.e. K")
        sys.exit(1)
    elif not validate_fare_class(fare_class):
        print("You may only enter one character A-Z")
        sys.exit(1)
    print("-- Fare code stored: {}".format(fare_class))
    return fare_class


# Returns the fare class multiplier as a float from the nested 'multiplier' dictionary.
def get_from_airline_dict(valid_airline_name, fare_class):
    try:
        multiplier = FARE_CLASS_MULTIPLIER_DICTIONARY[valid_airline_name][fare_class]
        return multiplier
    except KeyError:
        print("Sorry, that fare class is not a choice for {} Airlines.".format(valid_airline_name))
        sys.exit(1)


# Performs calculation to determine the EQM's and CPM by passing in fare cost, multiplier, and distance.
def get_cpm_calculation(multiplier, valid_flight_cost, flight_mileage):
    # The flight cost is divided by the flight mileage, then multiplied by the fare class multiplier to return the CPM.
    cpm = ((int(valid_flight_cost) / int(flight_mileage)) * int(multiplier)) * 100
    # The EQM, or elite qualifying miles,
    elite_miles_earned = int(flight_mileage) * int(multiplier)
    if cpm == 0:
        print("Sorry, your EQM and CPM could not be calculated")
        sys.exit(1)
    elif valid_airline_name == 'Delta':
        print("This " + str("{0:,g}".format(flight_mileage)) + " mile round-trip flight "
              "on Delta Airlines in fare class: " + str(fare_class) + " = '" + str(multiplier) + "x',"
              " which calculates at " + str(format(cpm, '.2f')) + " 'Cents Per Mile',"
              " earns you " + ("{0:,g}".format(elite_miles_earned)) + " MQMs.")
    elif valid_airline_name == 'United':
        print("This " + str("{0:,g}".format(flight_mileage)) + " mile round-trip flight "
              "on United Airlines in fare class: " + str(fare_class) + " = '" + str(multiplier) + "x',"
              " which calculates at " + str(format(cpm, '.2f')) + " 'Cents Per Mile',"
              " earns you " + ("{0:,g}".format(elite_miles_earned)) + " PQMs.")
    elif valid_airline_name == 'American':
        print("This " + str("{0:,g}".format(flight_mileage)) + " mile round-trip flight "
              "on American Airlines in fare class: " + str(fare_class) + " = '" + str(multiplier) + "x',"
              " which calculates at " + str(format(cpm, '.2f')) + " 'Cents Per Mile',"
              " earns you " + ("{0:,g}".format(elite_miles_earned)) + " EQMs.")
    sys.exit(1)


if __name__ == '__main__':
    airport_user_input = input("Input up to 5 airport codes ( i.e. lax, jfk, lhr ) ")
    codes = get_codes(airport_user_input)
    page_html = get_city_data(codes)
    flight_mileage = get_miles_from_html(page_html)
    flight_cost_input = input("What's the round-trip cost as a whole number with no symbols (i.e. 425)? ")
    valid_flight_cost = get_flight_cost(flight_cost_input)
    airline_input = input("Are you flying Delta, United, or American? ")
    valid_airline_name = get_airline(airline_input)
    fare_class_input = input("What is your fare class code? ")
    fare_class = get_fare_class(fare_class_input)
    flight_mileage = get_miles_from_html(page_html)
    multiplier = get_from_airline_dict(valid_airline_name, fare_class)
    get_cpm_calculation(multiplier, valid_flight_cost, flight_mileage)

