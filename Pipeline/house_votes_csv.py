#!/usr/bin/env python
#Create a csv with values for each bill number, information, votes by democrat/republican/etc
#make a different csv for each year from 2001 to 2017
#Shivam Parikh 2/28/17
#For Liberty, and Justice for All
import requests
import csv
from datetime import datetime
import xml.etree.ElementTree as ET
import os

def house(logname='house_log.txt', min_year=1990, max_year=2020):
    #perform the following operations for each year between 2001 and 2017
    file_base_name = "_bills.csv"
    bill_header = ["Roll Call", "Majority", "Congress Num", "Legislation Number", "Date", "Time", "Question",
                   "Description", "Result", "Republican Yes", "Republican No", "Republican Present", "Republican Not Voting",
                   "Democrat Yes", "Democrat No", "Democrat Present", "Democrat Not Voting",
                   "Independent Yes", "Independent No", "Independent Present", "Independent Not Voting",
                   "Total Yes", "Total No", "Total Present", "Total Not Voting"]
    log = open(logname, 'w')
    log.write("Trying to run the house crawler on house files.\n")
    log.write("Starting at time: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    if not os.path.exists('./HouseCSV'):
        os.makedirs('./HouseCSV')
    for year in range(min_year, max_year+1):
        base_url = "http://clerk.house.gov/evs/" + str(year) + "/"
        print(base_url)
        TABLE = [bill_header]
        i = 1
        next_exists = True
        while(next_exists):
            page = requests.get(base_url + house_gen_string(i))
            try:
                root = ET.fromstring(page.content)
                bill_meta =  root.find('vote-metadata')
                vote_totals = bill_meta.find('vote-totals')
                bill = [i, bill_meta.find('majority').text, bill_meta.find('congress').text,
                        bill_meta.find('legis-num').text, bill_meta.find('action-date').text,
                        bill_meta.find('action-time').text, bill_meta.find('vote-question').text,
                        str(bill_meta.find('vote-desc').text), bill_meta.find('vote-result').text]
                vs = vote_totals.findall('totals-by-party')
                vs.append(vote_totals.find('totals-by-vote'))
                for elem in vs:
                    bill.extend([elem.find('yea-total').text, elem.find('nay-total').text, elem.find('present-total').text, elem.find('not-voting-total').text])
                TABLE.append(bill)
                #print("worked " + str(i))
                i = i + 1
            except AttributeError:
                TABLE.append([i] + ['null' for i in range(1, 22)])
                i = i + 1
            except ET.ParseError:
                log.write("Finished all House files for Year: " + str(year))
                next_exists = False
            except:
                log.write(str(sys.exc_info()) + " in ")
                log.write(str(year) + ", " + str(i) + " Errored\n")
                continue
        #Write created table to csv
        with open(('./HouseCSV/' + str(year) + file_base_name), 'w') as f:
            writer = csv.writer(f)
            writer.writerows(TABLE)
        f.close()

def house_gen_string(num):
    #converts 3 digit num into string for pulling xml files from web
    if(num < 10):
        return ("roll00" + str(num) + ".xml")
    elif(num < 100):
        return ("roll0" + str(num) + ".xml")
    else:
        return ("roll" + str(num) + ".xml")

house(min_year=2017)
