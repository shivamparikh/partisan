#Written by Shivam Parikh
#hello world
#Wednesday, March 8th, 2017

import numpy as np
import datascience
import csv
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def houseDictPerYear(year):
    dict = {'100':0, '95':0, '90':0, '85':0, '80':0, 'together':0, 'total': 0, 'nonpart':0}
    file_name = "../Bill_Documents/House/" + str(year) + "_house_bills.csv"
    with open(file_name, 'r', errors = 'ignore') as f:
        reader = csv.reader(f)
        dataset = list(reader)
    total = int(dataset[1][23])+int(dataset[1][24])

    for vote in dataset[2:]:
        try:
            if(int(vote[21]) == 0 or int(vote[22])==0):
                dict['total'] += 1
                dict['together'] += 1
                continue
            repYes = int(vote[9])/int(vote[21])
            demYes = int(vote[13])/int(vote[21])
            repNo = int(vote[10])/int(vote[22])
            demNo = int(vote[14])/int(vote[22])
            biPart = [repYes,demYes,repNo,demNo]
            totalYes = int(vote[21])/(int(vote[21])+int(vote[22]))
            totalNo = int(vote[22])/(int(vote[21])+int(vote[22]))
            if(testPercentage([totalYes, totalNo], 0.95)):
                dict['together'] += 1
            elif(testPercentage(biPart, 1)):
                dict['100'] += 1
            elif(testPercentage(biPart, 0.95)):
                dict['95'] += 1
            elif(testPercentage(biPart, 0.9)):
                dict['90'] += 1
            elif(testPercentage(biPart, 0.85)):
                dict['85'] += 1
            elif(testPercentage(biPart, 0.8)):
                dict['80'] += 1
            else:
                dict['nonpart'] += 1
            dict['total'] += 1
        except IndexError:
            continue
    return dict

def senateDictPerYear(year):
    dict = {'100':0, '95':0, 'together':0, 'total': 0, 'nonpart':0}
    file_name = "../Bill_Documents/Senate/" + str(year) + "_senate_bills.csv"
    with open(file_name, 'r', errors = 'ignore') as f:
        reader = csv.reader(f)
        dataset = list(reader)

    for vote in dataset[1:]:
        try:
            if(int(vote[22]) == 0 or int(vote[23])==0):
                dict['total'] += 1
                dict['together'] += 1
                continue
            repYes = int(vote[10])/int(vote[22])
            demYes = int(vote[14])/int(vote[22])
            repNo = int(vote[11])/int(vote[23])
            demNo = int(vote[15])/int(vote[23])
            biPart = [repYes,demYes,repNo,demNo]
            totalYes = int(vote[22])/(int(vote[22])+int(vote[23]))
            totalNo = int(vote[23])/(int(vote[22])+int(vote[23]))
            if(testPercentage([totalYes, totalNo], 0.95)):
                dict['together'] += 1
            elif(testPercentage(biPart, 1)):
                dict['100'] += 1
            elif(testPercentage(biPart, 0.95)):
                dict['95'] += 1
            else:
                dict['nonpart'] += 1
            dict['total'] += 1
        except IndexError:
            continue
    return dict

def testPercentage(array, percentage):
    for each in array:
        if(each >= percentage):
            return True
    return False

def houseGenerateLine():
    dict = {}
    plt.axis([1989, 2022, 0, 100])
    plt.xticks(np.arange(1989, 2023, 2))
    for year in range(1990, 2018):
        temp = houseDictPerYear(year)
        partisan = temp['together']/temp['total']
        bipartisan = (temp['100']+temp['95'])/temp['total']
        nonpart = (temp['nonpart']+temp['80']+temp['85']+temp['90'])/temp['total']
        dict[year] = (partisan, bipartisan, nonpart)
    for v in dict.values():
        print(sum(v))
    plt.plot(sorted(dict.keys()), [dict[x][0]*100 for x in sorted(dict.keys())],
             'k', c='g', label=">=95% Agreement in House")
    plt.plot(sorted(dict.keys()), [dict[x][1]*100 for x in sorted(dict.keys())],
             'k', c='r', label="Vote on a >=95% Party Line (Bi-Partisan)")
    plt.plot(sorted(dict.keys()), [dict[x][2]*100 for x in sorted(dict.keys())],
             'k', c='b', label="All Other Votes (Not Extreme Agreement or Disagreement)")
    drawParties(plt, "house")
    plt.legend(bbox_to_anchor=(0.5, -0.1))
    plt.title("(Bi)Partisan Voting in the U.S. House from 1990-2017")
    plt.ylabel("Percentage of Total Votes in the House (0-100%)")
    plt.xlabel("Years (1990-2017)")
    plt.show()
    plt.figure().savefig("house.png")


def drawParties(plot, party="president"):
    with open("/Users/ShivamParikh/Development/partisan/Bill_Documents/majority.csv", 'r', errors = 'ignore') as f:
        reader = csv.reader(f)
        dataset = list(reader)
    dataset = dataset[1:]
    if(party == "president"):
        set = [3, 1, 2]
    elif(party == "senate"):
        set = [2, 1, 3]
    else:
        set = [1, 2, 3]
    for row in dataset:
        plot.gca().add_patch(patches.Rectangle((int(row[0]), 9), 1, 91,
                                        alpha=0.4, facecolor=color(row[set[0]])))
        plot.gca().add_patch(patches.Rectangle((int(row[0]), 4), 1, 3,
                                        alpha=0.4, facecolor=color(row[set[1]])))
        plot.gca().add_patch(patches.Rectangle((int(row[0]), 0), 1, 3,
                                        alpha=0.4, facecolor=color(row[set[2]])))

def color(party):
    if(party == 'D'):
        return 'blue'
    elif(party=='R'):
        return 'red'
    else:
        return 'grey'

def senateGenerateLine():
    dict = {}
    plt.axis([1989, 2018, 0, 100])
    for year in range(1990, 2018):
        temp = senateDictPerYear(year)
        partisan = temp['together']/temp['total']
        bipartisan = (temp['100']+temp['95'])/temp['total']
        nonpart = (temp['nonpart'])/temp['total']
        dict[year] = (partisan, bipartisan, nonpart)
    for v in dict.values():
        print(sum(v))
    plt.plot(sorted(dict.keys()), [dict[x][0]*100 for x in sorted(dict.keys())],
            'k', c='g', label=">=95% Agreement in Senate")
    plt.plot(sorted(dict.keys()), [dict[x][1]*100 for x in sorted(dict.keys())],
            'k', c='r', label="Vote on a >=95% Party Line (Bi-Partisan)")
    plt.plot(sorted(dict.keys()), [dict[x][2]*100 for x in sorted(dict.keys())],
            'k', c='b', label="All Other Votes (Not Extreme Agreement or Disagreement)")
    plt.legend()
    drawParties(plt, "senate")
    plt.title("(Bi)Partisan Voting in the U.S. Senate from 1990-2017")
    plt.ylabel("Percentage of Total Votes in the Senate (0-100%)")
    plt.xlabel("Years (1990-2017)")
    plt.grid(b=True, which='major', color='k')
    plt.show()
    plt.figure().savefig("senate.png")
