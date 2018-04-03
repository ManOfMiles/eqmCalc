Inputs:
Airport codes: At least two, no more than five. Must be three letters, comma separated.
Flight cost: Must be greater than $10 but less than $1,000.
Airline: Choices are; American, Delta, and United.
Fare Class Code: This is represented as a single letter, not all letters are used by all airlines.


Welcome, this is an EQM Calculator.

EQM stands for Elite Qualifying Miles, these are miles earned by flying on an airline, based on the distance flown. 
EQMs are not the same as 'award miles', award miles are miles earned based on the cost of the ticket and are redeemed for 'free flights'.
EQMs are not redeemable miles, rather they are miles that accumulate towards earning elite status with a given airline.

An example elite status is Delta 'Silver Medallion', you'd need to earn 25,000 EQMs (Delta calls them MQMs) in a single calendar year to qualify. 

Based on the fare class code "letter" of the specific flight booked, an airline will credit you EQMs based on the actual flight distance 
multiplied by the fare class multiplier. The fare class multiplier can range from 0x (basic economy) up to 3x (First Class)

If you are flying in full-fare economy class, known as Y class, you'll earn 1.5x EQMs on the total miles flown. 
Users will need to find the fare class letter while shopping for flights or on their receipt/itinerary.

1. For example, Seattle to Beijing round-trip is 10,820 flight miles. The user would input the airline codes: 'sea, pek'
2. Next, they would enter the flight cost, say $350
3. Now the airline will be entered, say Delta
4. Lastly, the fare class code will be entered, say 'M'

Output: 'This 10,820 mile round-trip flight on Delta Airlines in fare class: M = '1x', which calculates at 3.23 'Cents Per Mile', earns you 10,820 MQMs.'

Once the data points are received, the multiplier dict value is fetched based on the airline and fare class code entered. 
The calculator will then compute the 'Cents Per Mile' by dividing the flight cost by the flight distance, 
then multiplying by the multiplier dict value, finally the decimal place is moved by multiplying 100.

Some traveler-hackers search for "mileage runs", the goal is to find a cheap flight that has a long flight distance while the fare class has a large muliplier.
The qualifier for a "good" mileage run is around three Cents-Per-Mile or less. In the example above you'd earn 3.23 CPM, a decent mileage run for sure.

Select travel-hackers will do a same day 'turn', meaning they will land in their destination only to turn around the same day. The point of the flight is to earn EQM's, not for leisure. This is effectively "buying" your elite status with an airline. 







