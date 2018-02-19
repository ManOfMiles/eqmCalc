from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
import sys


#prompting user for three-letter airport codes, minimum of first two inputs
while True:
    airport_1 = input("Input your beginning three-letter airport code: ")
    if airport_1.isalpha() and len(airport_1) == 3:
        break
    print("Please input only three letters")

while True:
    airport_2 = input("Input your 2nd three-letter airport code: ")
    if airport_2.isalpha() and len(airport_2) == 3:
        break
    print("*Try again, please input only three letters*")

while True:
    airport_3 = input("Input your 3rd three-letter airport code or press 'enter' to skip: ")
    if airport_3.isalpha() and len(airport_3) == 3 or len(airport_3) == 0:
        break
    print("*Try again, please input only three letters*")

while True:
    airport_4 = input("Input your 4th three-letter airport code or press 'enter' to skip: ")
    if airport_4.isalpha() and len(airport_4) == 3 or len(airport_4) == 0:
        break
    print("*Try again, please input only three letters*")

while True:
    airport_5 = input("Input your 5th three-letter airport code or press 'enter' to skip: ")
    if airport_5.isalpha() and len(airport_5) == 3 or len(airport_5) == 0:
        break
    print("*Try again, please input only three letters*")

#running the URL query with airport arguments
url_query = ("http://www.webflyer.com/travel/mileage_calculator/getmileage.php?"
"&city={0}"
"&city={1}"
"&city={2}"
"&city={3}"
"&city={4}"
.format(airport_1, airport_2, airport_3, airport_4, airport_5,))

#url request and parsing
my_url = url_query
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_extract = soup(page_html, "html.parser")

table_data = page_extract.find("table", attrs={"class":"table_bg"})

#scraping the single table cell with the flight mileage
distance_td = table_data.findAll("td")[-18].text

distance_figure = re.sub('[^0-9]','',str(distance_td))
print("Your flight distance is " + distance_figure + " miles")

#capturing the cost of the airfare
while True:
    flight_cost = input("What is the cost of the airfare? ")
    if flight_cost.isnumeric() and len(flight_cost) >= 2:
        break
    print("You must enter a dollar amount as a number ")

#calculation of the cost per mile using flight cost divided by flight mileage
distance_as_num = int(distance_figure)
flight_cost_as_num = int(flight_cost)
cpm = (flight_cost_as_num / distance_as_num) * 100
cpm_precision_two = round(cpm, 2)

#prints the outcome of the distance to cpm calculation based on the value proposition
if cpm_precision_two <= 3:
    print("Your flight calculates at " + str(cpm_precision_two) + " cents per mile, that is a great mileage run")
elif cpm_precision_two > 3 and cpm_precision_two <= 6:
    print("Your flight calculates at " + str(cpm_precision_two) + " cents per mile, that is an okay mileage run")
else:
    print("Your flight calculates at " + str(cpm_precision_two) + " cents per mile, that is not a good mileage run")









