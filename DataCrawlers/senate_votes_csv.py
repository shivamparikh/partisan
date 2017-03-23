#!/usr/bin/env python
#Create a csv with values for each bill number, information, votes by democrat/republican/etc
#make a different csv for each year from 2001 to 2017
#Shivam Parikh 2/28/17
#For Liberty, and Justice for All
import requests
import sys
from datetime import datetime
import csv
import xml.etree.ElementTree as ET

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def senate(logname='error_log.txt'):
    #https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_101_2.xml
    #https://www.senate.gov/legislative/LIS/roll_call_votes/vote1011/vote_101_1_00002.xml
    file_base_name = "_senate_bills.csv"
    bill_header = ["Vote Number", "Congress Num", "Session", "Legislation Number", "Date", "Question", "Vote Title", "Document Text", "Result", "Majority Requirement", "Republican Yes", "Republican No", "Republican Present", "Republican Absent", "Democrat Yes", "Democrat No",
                   "Democrat Present", "Democrat Absent", "Independent Yes", "Independent No",
                   "Independent Present", "Independent Absent", "Total Yes", "Total No",
                   "Total Present", "Total Absent", "Tie Breaker"]
    base_url = "https://www.senate.gov/legislative/LIS/roll_call_votes/vote"
    log = open(logname, 'w')
    print("Started1")
    log.write("Trying to run the senate crawler on senate files.\n")
    log.write("Starting at time: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    for congress in range(101, 116):
        for session in range(1,3):
            if(congress == 115 and session==2):
                break
            next_exists = True
            i = 0
            TABLE = [bill_header]
            while(next_exists):
                i+=1
                page = requests.get(base_url + senate_gen_string(congress, session, i), headers=headers)
                #print(base_url + senate_gen_string(congress, session, i))
                try:
                    root = ET.fromstring(page.content)
                    partyDict = {'D': {'Yea':0, 'Nay':0, 'Present':0, 'Not Voting':0, 'Err':0},
                                 'R': {'Yea':0, 'Nay':0, 'Present':0, 'Not Voting':0, 'Err':0},
                                 'I': {'Yea':0, 'Nay':0, 'Present':0, 'Not Voting':0, 'Err':0},
                                 'Total': {'Yea':0, 'Nay':0, 'Present':0, 'Not Voting':0, 'Err':0}}
                    for mems in root.find('members'):
                        partyDict[pParty(mems.find('party').text)][pVote(mems.find('vote_cast').text)] += 1
                    partyDict['Total']['Yea'] = myInt(root.find('count').find('yeas').text)
                    partyDict['Total']['Nay'] = myInt(root.find('count').find('nays').text)
                    partyDict['Total']['Present'] = myInt(root.find('count').find('present').text)
                    partyDict['Total']['Not Voting'] = myInt(root.find('count').find('absent').text)
                    vote = [root.find('vote_number').text, root.find('congress').text, root.find('session').text,
                            root.find('document').find('document_name').text, root.find('vote_date').text,
                            root.find('vote_question_text').text, root.find('vote_title').text,
                            root.find('vote_document_text').text, root.find('vote_result_text').text,
                            "'"+root.find('majority_requirement').text+"'", partyDict['R']['Yea'],
                            partyDict['R']['Nay'], partyDict['R']['Present'],
                            partyDict['R']['Not Voting'], partyDict['D']['Yea'],
                            partyDict['D']['Nay'], partyDict['D']['Present'],
                            partyDict['D']['Not Voting'], partyDict['I']['Yea'],
                            partyDict['I']['Nay'], partyDict['I']['Present'],
                            partyDict['I']['Not Voting'], partyDict['Total']['Yea'],
                            partyDict['Total']['Nay'], partyDict['Total']['Present'],
                            partyDict['Total']['Not Voting'],
                            root.find('tie_breaker').find('tie_breaker_vote').text]
                    TABLE.append(vote)
                except AttributeError:
                    continue
                except ET.ParseError as e:
                    log.write("Finished all Senate files for Congress: " + str(10*congress+session) +'\n')
                    next_exists = False
                except:
                    log.write(str(sys.exc_info()) + " in ")
                    log.write(str(congress) + ", " + str(session) + ", " + str(i) + " Errored\n")
                    continue
            with open((str(10*congress+session) + file_base_name), 'w') as f:
                writer = csv.writer(f)
                writer.writerows(TABLE)
            log.write("Storing table " + (str(10*congress+session) + file_base_name) + "into csv file\n")
            f.close()
    log.write("Finishing at time: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    log.write("Finished Everything, closing file now.\n")

def pVote(vote):
    if(vote == 'Nay' or vote == 'Not Guilty'):
        return 'Nay'
    elif(vote == 'Yea' or vote == 'Guilty'):
        return 'Yea'
    elif(vote == 'Not Voting' or 'Absent'):
        return 'Not Voting'
    elif('Present' in vote):
        return 'Present'
    else:
        print('we found an unknown ' + vote + '\n')
        return 'Err'
def pParty(party):
    if(party == 'D'):
        return 'D'
    elif(party == 'R'):
        return 'R'
    else:
        return 'I'

def myInt(x):
    if(x == None):
        return 0
    else:
        try:
            return int(x)
        except:
            print('error casting ' + x + ' to integer\n')
            return 0

def senate_gen_string(congress, session, bill):
    return str(10*congress+session)+'/vote_'+str(congress)+'_'+str(session)+'_'+'{:05d}'.format(bill)+'.xml'
