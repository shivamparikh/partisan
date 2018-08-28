#!/usr/bin/env python
#Create a csv with values for each bill number, information, votes by democrat/republican/etc
#make a different csv for each year from 2001 to 2017
#Shivam Parikh 2/28/17
#For Liberty, and Justice for All
import requests
import csv
import xml.etree.ElementTree as ET

def house():
    #perform the following operations for each year between 2001 and 2017
    file_base_name = "_bills.csv"
    bill_header = ["Roll Call", "Majority", "Congress Num", "Legislation Number", "Date", "Time", "Question",
                   "Description", "Result", "Republican Yes", "Republican No", "Republican Present", "Republican Not Voting",
                   "Democrat Yes", "Democrat No", "Democrat Present", "Democrat Not Voting",
                   "Independent Yes", "Independent No", "Independent Present", "Independent Not Voting",
                   "Total Yes", "Total No", "Total Present", "Total Not Voting"]
    for year in range(1990, 2018):
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
                print("Finished all House files for Year: " + str(year))
                next_exists = False
                #break
        #Write created table to csv
        with open((str(year) + file_base_name), 'w') as f:
            writer = csv.writer(f)
            writer.writerows(TABLE)
        f.close()


def senate():
    #https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_101_2.xml
    #https://www.senate.gov/legislative/LIS/roll_call_votes/vote1011/vote_101_1_00002.xml
    file_base_name = "_senate_bills.csv"
    bill_header = ["Vote Number", "Congress Num", "Session", "Legislation Number", "Date", "Question", "Vote Title", "Document Text", "Result", "Majority Requirement", "Republican Yes", "Republican No", "Republican Present", "Republican Absent", "Democrat Yes", "Democrat No",
                   "Democrat Present", "Democrat Absent", "Total Yes", "Total No",
                   "Total Present", "Total Absent", "Tie Breaker"]
    base_url = "https://www.senate.gov/legislative/LIS/roll_call_votes/vote"
    for congress in range(101, 102):
        for session in range(1,2):
            next_exists = True
            i = 0
            TABLE = [bill_header]
            while(i < 20):
                i+=1
                page = requests.get(base_url + senate_gen_string(congress, session, i))
                print(base_url + senate_gen_string(congress, session, i))
                try:
                    root = ET.fromstring(page.content)
                    partyDict = {'D': {'Yea':0, 'Nay':0, 'Present':0, 'Not Voting':0}, 'R': {'Yea':0, 'Nay':0, 'Present':0, 'Not Voting':0}}
                    for mems in root.find('members'):
                        partyDict[mems.find('party').text][mems.find('vote_cast').text] += 1
                    if(sum(partyDict['D'].values()) + sum(partyDict['R'].values()) != 100):
                        print(congress, session, i)
                    vote = [root.find('vote_number').text, root.find('congress').text, root.find('session').text,
                            root.find('document').find('document_name').text, root.find('vote_date').text,
                            root.find('vote_question_text').text, root.find('vote_title').text,
                            root.find('vote_document_text').text, root.find('vote_result_text').text,
                            root.find('majority_requirement').text, partyDict['R']['Yea'],
                            partyDict['R']['Nay'], partyDict['R']['Present'],
                            partyDict['R']['Not Voting'], partyDict['D']['Yea'],
                            partyDict['D']['Nay'], partyDict['D']['Present'],
                            partyDict['D']['Not Voting'], root.find('count').find('yeas').text,
                            root.find('count').find('nays').text, root.find('count').find('present').text,
                            root.find('count').find('absent').text,
                            root.find('tie_breaker').find('tie_breaker_vote').text]
                    TABLE.append(vote)
                except AttributeError:
                    continue
                except ET.ParseError as e:
                    if('mismatched tag' in str(e)):
                        print(congress, session, i)
                        TABLE.append(["not work" for i in range(0, 23)])
                        continue
                    print("Finished all Senate files for Congress: " + str(10*congress+session))
                    next_exists = False
            with open((str(10*congress+session) + file_base_name), 'w') as f:
                writer = csv.writer(f)
                writer.writerows(TABLE)
            f.close()


def senate_gen_string(congress, session, bill):
    return str(10*congress+session)+'/vote_'+str(congress)+'_'+str(session)+'_'+'{:05d}'.format(bill)+'.xml'


def house_gen_string(num):
    #converts 3 digit num into string for pulling xml files from web
    if(num < 10):
        return ("roll00" + str(num) + ".xml")
    elif(num < 100):
        return ("roll0" + str(num) + ".xml")
    else:
        return ("roll" + str(num) + ".xml")
