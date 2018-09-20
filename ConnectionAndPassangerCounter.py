import requests
import itertools
import operator
import collections
import datetime
import calendar

r = requests.get('https://dbdata.colibri-w.de/api/hackathon/1/systems.json?'
                 'params=%7B%22user%22%3A%22innotrans%22%2C%22password%22%3A%22innotrans2018%22%7D').json()

notNullSystems = list()

# Find coaches that belong to trains
for system in r:
    if system.get('trainNumber') is not None and system.get("trainNumber") != 200 and system.get("trainNumber") > 0:
        notNullSystems.append(system)


sortedList = sorted(notNullSystems, key=lambda k: k['trainNumber'])

# Group them by which train they belong to
for systems in itertools.groupby(sortedList, operator.itemgetter('trainNumber')):
    totalSessions = 0
    totalPassengers = 0
    sessionNumbers = list()
    passengers = list()
    # Loop through coaches of the train
    for system in systems[1]:
        original_mac = system.get("mac")
        encoded_mac = original_mac.replace(":", "%3A")
        s = requests.get("https://dbdata.colibri-w.de/api/hackathon/1/system.json?"
                         "params=%7B%22user%22%3A%22innotrans%22%2C%22password%22%3A%22innotrans2018%22%2C%22mac%22%3A%22"
                         + encoded_mac + "%22%7D").json()

        # If they have wifi traffic data, save it along with the corresponding months
        for month in s["traffic"]:
            if month["sessions"] is not None:
                sessionNumbers.append({"month": month["month"], "sessions": month["sessions"]})

        # If they have passenger count data for the month they have wifi data for, collect it by month
        for index, dp in enumerate(sessionNumbers):
            passengerCount = 0
            year = int(dp["month"][:4])
            month = int(dp["month"][4:])
            day = 1

            start = datetime.datetime(year, month, day).strftime('%s')
            end = datetime.datetime(year, month, calendar.monthrange(year, month)[1]).strftime('%s')
            p = requests.get("https://dbdata.colibri-w.de/api/hackathon/1/afz.json?"
                         "params=%7B%22user%22%3A%22innotrans%22%2C%22password%22%3A%22innotrans2018%22%2C%22mac%22%3A%22"
                         + encoded_mac + "%22%2C%22fromTime%22%3A" + start + "%2C%22toTime%22%3A" + end + "%7D").json()
            for a in p:
                if isinstance(a, collections.Mapping) and ("sensors" in a.keys()):
                    if a["sensors"] is not None:
                        for sensor in a['sensors']:
                            if isinstance(sensor, collections.Mapping) and "current_cat_0_in" in sensor.keys():
                                if sensor["current_cat_0_in"] is not None:
                                    passengerCount += sensor["current_cat_0_in"]
            passengers.append(passengerCount)

        # Log results by train number, more verbose if usable
        print("* Train number: " + str(systems[0]) + "\n")
        for index, dp in enumerate(sessionNumbers):
            if passengers[index] != 0 and dp["sessions"] != 0:
            	print("------------------------------")
            	print(" - Period: " + str(dp["month"][0:4]) + "/" + dp["month"][4:])
            	print(" - AP MAC address: " + str(original_mac))
            	print(" - WiFi sessions established: " + str(dp["sessions"]))
            	print(" - Passengers onboarded: " + str(passengers[index]))
            	print("------------------------------")
            	if index == len(sessionNumbers) - 1:
            		print("")