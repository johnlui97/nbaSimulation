from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

import csv
import re
import math
import numpy as np
import matplotlib.pyplot as plt


nba_teams_array = ['ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU',
                   'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL',
                   'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
    
def PreviousGamesAnalysis():
    i = 0
    stringIndex = 0
    startFlag = 0
    while( i < len(nba_teams_array)):
        
        with open( nba_teams_array[i] + '_gamesLog.csv', 'w', newline = '') as f:
            writer = csv.writer(f)

            current_url = "https://www.basketball-reference.com/teams/" + nba_teams_array[i] + "/2019/gamelog/"

            print("\n" + current_url + "\n")

            uClient = uReq(current_url)
            page_html = uClient.read()
            uClient.close()
            page_soup = soup(page_html, "html.parser")

            writer.writerow(["Game Number", "Date", "Location", "Result", "Points", "Opp. Points", "FGA", "FG%", "3PA", "3P%", "TO", "ORB"])

            GamesLog = page_soup.find("div", {"class":"table_outer_container"}).table.tbody
            entries = GamesLog.find_all("tr")

            mean_PPG = float(0)
            sum_PPG  = float(0)
            sum_3PP  = float(0)
            sum_fg_pct  = float(0)
            sum_TO = float(0)

            var_PPG_n = float(0)
            var_3PP_n = float(0)
            var_FGP_n = float(0)
            var_TOG_n = float(0)

            for row in entries:
                try:
                    error = 0
                    gameNumber = row.find("td", {"class":"right endpoint tooltip"}).strong.text
                    date       = row.find("td", {"data-stat":"date_game"}).text
                    result = row.find("td", {"data-stat":"game_result"})
                    Result = result.text
                    location   = row.find("td", {"data-stat":"game_location"}).text
                    if(location == ""):
                        location = "v"
                    points     = row.find("td", {"data-stat":"pts"}).text
                    opp_points = row.find("td", {"data-stat":"opp_pts"}).text
                    fga        = row.find("td", {"data-stat":"fga"}).text
                    fg_pct     = row.find("td", {"data-stat":"fg_pct"}).text
                    fg3a       = row.find("td", {"data-stat":"fg3a"}).text
                    fg3_pct    = row.find("td", {"data-stat":"fg3_pct"}).text
                    
                    turnovers  = row.find("td", {"data-stat":"tov"}).text
                    offReb     = row.find("td", {"data-stat":"orb"}).text

                    sum_PPG = sum_PPG + float(points)
                    sum_3PP = sum_3PP + float(fg3_pct)
                    sum_fg_pct = sum_fg_pct + float(fg_pct)
                    sum_TO  = sum_TO + float(turnovers)

                    writer.writerow([gameNumber, date, location, Result, points, opp_points, fga, fg_pct, fg3a, fg3_pct, turnovers, offReb])
                except AttributeError:
                    error = 1
        
            mean_PPG = sum_PPG / (float(gameNumber))
            mean_3PP = sum_3PP / (float(gameNumber))
            mean_FGP = sum_fg_pct / (float(gameNumber))
            mean_TOG = sum_TO / (float(gameNumber))
            
            for row in entries:
                try:
                    error = 0
                    gameNumber = row.find("td", {"class":"right endpoint tooltip"}).strong.text
                    date       = row.find("td", {"data-stat":"date_game"}).text
                    result = row.find("td", {"data-stat":"game_result"})
                    Result = result.text
                    location   = row.find("td", {"data-stat":"game_location"}).text
                    if(location == ""):
                        location = "v"
                    points     = row.find("td", {"data-stat":"pts"}).text
                    opp_points = row.find("td", {"data-stat":"opp_pts"}).text
                    fga        = row.find("td", {"data-stat":"fga"}).text
                    fg_pct     = row.find("td", {"data-stat":"fg_pct"}).text
                    fg3a       = row.find("td", {"data-stat":"fg3a"}).text
                    fg3_pct    = row.find("td", {"data-stat":"fg3_pct"}).text
                    
                    turnovers  = row.find("td", {"data-stat":"tov"}).text
                    offReb     = row.find("td", {"data-stat":"orb"}).text

                    var_PPG_n = var_PPG_n + ((float(points) - mean_PPG)*(float(points) - mean_PPG))
                    var_FGP_n = var_FGP_n + ((float(fg_pct) - mean_FGP)*(float(fg_pct) - mean_FGP))
                    var_3PP_n = var_3PP_n + ((float(fg3_pct) - mean_3PP)*(float(fg3_pct) - mean_3PP))
                    var_TOG_n = var_TOG_n + ((float(turnovers) - mean_TOG)*(float(turnovers) - mean_TOG))
                    
                except AttributeError:
                    error = 1

            var_PPG = var_PPG_n / (float(gameNumber) - 1)
            var_3PP = var_3PP_n / (float(gameNumber) - 1)
            var_FGP = var_FGP_n / (float(gameNumber) - 1)
            var_TOG = var_TOG_n / (float(gameNumber) - 1)
            
            std_PPG = math.sqrt(var_PPG)
            std_3PP = math.sqrt(var_3PP)
            std_FGP = math.sqrt(var_FGP)
            std_TOG = math.sqrt(var_TOG)

            Percentile68_p_PPG = float(mean_PPG + std_PPG)
            Percentile68_n_PPG = float(mean_PPG - std_PPG)

            Percentile68_p_FGP = float(mean_FGP + std_FGP)
            Percentile68_n_FGP = float(mean_FGP - std_FGP)

            Percentile68_p_3PP = float(mean_3PP + std_3PP)
            Percentile68_n_3PP = float(mean_3PP - std_3PP)

            Percentile68_p_TOG = float(mean_TOG + std_TOG)
            Percentile68_n_TOG = float(mean_TOG - std_TOG)

            writer.writerow([])
            writer.writerow(["*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*"])
            writer.writerow([])
            writer.writerow(["PPG+ 68%", "-", "-", "-", Percentile68_p_PPG, "-", "-", "-", "-", "-", "-", "-"])
            writer.writerow(["PPG- 68%", "-", "-", "-", Percentile68_n_PPG, "-", "-", "-", "-", "-", "-", "-"])
            writer.writerow([])
            writer.writerow(["FGP+ 68%", "-", "-", "-", "-", "-", "-", Percentile68_p_FGP, "-", "-", "-", "-"])
            writer.writerow(["FGP- 68%", "-", "-", "-", "-", "-", "-", Percentile68_n_FGP, "-", "-", "-", "-"])
            writer.writerow([])
            writer.writerow(["3PP+ 68%", "-", "-", "-", "-", "-", "-", "-", "-", Percentile68_p_3PP, "-", "-"])
            writer.writerow(["3PP- 68%", "-", "-", "-", "-", "-", "-", "-", "-", Percentile68_n_3PP, "-", "-"])
            writer.writerow([])
            writer.writerow(["TOG+ 68%", "-", "-", "-", "-", "-", "-", "-", "-", "-", Percentile68_p_TOG, "-"])
            writer.writerow(["TOG- 68%", "-", "-", "-", "-", "-", "-", "-", "-", "-", Percentile68_n_TOG, "-"])
            writer.writerow([])
            writer.writerow(["Average", "-", "-", "-", mean_PPG, "-", "-", mean_FGP, "-", mean_3PP, mean_TOG, "-"])
            writer.writerow(["Variance", "-", "-", "-", var_PPG, "-", "-", var_FGP, "-", var_3PP, var_TOG, "-"])
            writer.writerow(["Std Dev", "-", "-", "-", std_PPG, "-", "-", std_FGP, "-", std_3PP, std_TOG, "-"])

        
        i += 1

def loadDataSetPPG(FileName):

    i = int(0)
    dataSet = []
    errorFlag = 0
    
    with open( FileName, 'r', newline = '') as f:

        reader = csv.reader(f)

        for row in reader:

            try:
                errorFlag = 0
                if(row[11] != "-"):
                    if(row[0] != "Game Number"):
                        if(row[0] == "*"):
                            break
                        else:
                            dataSet.append(float(row[4]))
            except IndexError:
                errorFlag = 1

    return dataSet

def loadDataSetFGP(FileName):

    i = int(0)
    dataSet = []
    errorFlag = 0
    
    with open( FileName, 'r', newline = '') as f:

        reader = csv.reader(f)

        for row in reader:

            try:
                errorFlag = 0
                if(row[11] != "-"):
                    if(row[0] != "Game Number"):
                        if(row[0] == "*"):
                            break
                        else:
                            dataSet.append(float(row[7]))
            except IndexError:
                errorFlag = 1

    return dataSet

def loadDataSet3PP(FileName):

    i = int(0)
    dataSet = []
    errorFlag = 0
    
    with open( FileName, 'r', newline = '') as f:

        reader = csv.reader(f)

        for row in reader:

            try:
                errorFlag = 0
                if(row[11] != "-"):
                    if(row[0] != "Game Number"):
                        if(row[0] == "*"):
                            break
                        else:
                            dataSet.append(float(row[9]))
            except IndexError:
                errorFlag = 1

    return dataSet

def loadDataSetTOV(FileName):

    i = int(0)
    dataSet = []
    errorFlag = 0
    
    with open(FileName, 'r', newline = '') as f:

        reader = csv.reader(f)

        for row in reader:

            try:
                errorFlag = 0
                if(row[11] != "-"):
                    if(row[0] != "Game Number"):
                        if(row[0] == "*"):
                            break
                        else:
                            dataSet.append(float(row[10]))
            except IndexError:
                errorFlag = 1

    return dataSet


def daysRest(FileName):

    i = int(0)
    dataSet = []
    errorFlag = 0
    
    with open(FileName, 'r', newline = '') as f:

        reader = csv.reader(f)

        for row in reader:

            try:
                errorFlag = 0
                if(row[11] != "-"):
                    if(row[0] != "Game Number"):
                        if(row[0] == "*"):
                            break
                        else:
                            dataSet.append(str(row[1]))
            except IndexError:
                errorFlag = 1

    return dataSet

def movingAverage(values, window):

    weights = np.repeat(1.0, window)/window
    smas = np.convolve(values, weights, 'valid')
    return smas 


def addMovingAverages():

    index = 0
    while(index < len(nba_teams_array)):

        print(nba_teams_array[index])
        print("\n")

        DataSet = loadDataSetPPG(nba_teams_array[index] + "_gamesLog.csv")
        writePPG_MA = movingAverage(DataSet, 5)

        DataSet = loadDataSetFGP(nba_teams_array[index] + "_gamesLog.csv")
        writeFGP_MA = movingAverage(DataSet, 5)

        DataSet = loadDataSet3PP(nba_teams_array[index] + "_gamesLog.csv")
        write3PP_MA = movingAverage(DataSet, 5)

        DataSet = loadDataSetTOV(nba_teams_array[index] + "_gamesLog.csv")
        writeTOV_MA = movingAverage(DataSet, 5)

        with open( nba_teams_array[index] + '_gamesLog.csv', 'a', newline = '') as f:
            writer = csv.writer(f)

            writer.writerow(["*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*"])
            writer.writerow([])
            
            print(writePPG_MA)
            writer.writerow([])
            writer.writerow(["PPG Moving Averages"])
            writer.writerow(writePPG_MA)
            print("\n")
            print(writeFGP_MA)
            writer.writerow([])
            writer.writerow(["FGP Moving Averages"])
            writer.writerow(writeFGP_MA)
            print("\n")
            print(write3PP_MA)
            writer.writerow([])
            writer.writerow(["3PP Moving Averages"])
            writer.writerow(write3PP_MA)
            print("\n")
            print(writeTOV_MA)
            writer.writerow([])
            writer.writerow(["TOV Moving Averages"])
            writer.writerow(writeTOV_MA)

        index += 1



def createPlot(FileName):

    i = int(0)
    xaxis = []
    yaxis = []
    movingA = movingAverage(loadDataSetPPG(FileName), 5)
    errorFlag = 0
    
    
    with open(FileName, 'r', newline = '') as f:

        reader = csv.reader(f)

        for row in reader:

            try:
                errorFlag = 0
                if(row[11] != "-"):
                    if(row[0] != "Game Number"):
                        if(row[0] == "*"):
                            break
                        else:
                            xaxis.append(float(row[0]))
                            yaxis.append(float(row[4]))
            except IndexError:
                errorFlag = 1

    plt.plot(xaxis, yaxis)
    plt.plot(xaxis[4:len(xaxis)], movingA)
    plt.title(FileName)
    plt.show()


def tonightsGames(month, today):

    current_url = "https://www.basketball-reference.com/leagues/NBA_2019_games-" + month + ".html"

    uClient = uReq(current_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")

    games = page_soup.find("div", {"id":"all_schedule"}).table.tbody
    entries = games.find_all("tr")

    tonightsGamesData = []
    
    for row in entries:
        tonightsGames = row.th.a.text

        if(tonightsGames == today):
            visitor = row.find("td", {"data-stat":"visitor_team_name"}).a.text
            home    = row.find("td", {"data-stat":"home_team_name"}).a.text

            if(visitor == "Brooklyn Nets"):
                visitor = "BRK"
            if(home == "Brooklyn Nets"):
                home = "BRK"
            if(visitor == "Charlotte Hornets"):
                visitor = "CHO"
            if(home == "Charlotte Hornets"):
                home = "CHO"
            if(visitor == "Golden State Warriors"):
                visitor = "GSW"
            if(home == "Golden State Warriors"):
                home = "GSW"
            if(visitor == "Los Angeles Clippers"):
                visitor = "LAC"
            if(home == "Los Angeles Clippers"):
                home = "LAC"
            if(visitor == "Los Angeles Lakers"):
                visitor = "LAL"
            if(home == "Los Angeles Lakers"):
                home = "LAL"
            if(visitor == "New Orleans Pelicans"):
                visitor = "NOP"
            if(home == "New Orleans Pelicans"):
                home = "NOP"
            if(visitor == "New York Knicks"):
                visitor = "NYK"
            if(home == "New York Knicks"):
                home = "NYK"
            if(visitor == "Oklahoma City Thunder"):
                visitor = "OKC"
            if(home == "Oklahoma City Thunder"):
                home = "OKC"
            if(visitor == "San Antonio Spurs"):
                visitor = "SAS"
            if(home == "San Antonio Spurs"):
                home = "SAS"

            visitor = visitor.upper()
            home = home.upper()

            temp = visitor[0:3]
            temp2 = home[0:3]

            tonightsGamesData.append(temp)
            tonightsGamesData.append(temp2)
            
    return tonightsGamesData

def generateTonightsPlots(data):
    i = int(0)
    while(i < len(data)):
        createPlot(data[i] + '_gamesLog.csv')
        i += 1

def numberDaysRested(data, Today):

    x = len(data)
    last_element = data[x-1]
    daysRested = int(Today[8:10]) - int(last_element[8:10])
    return daysRested

def arrayNumberDaysRested(data):

    i = int(0)
    array = []

    while(i < len(data)):
        array.append(numberDaysRested(daysRest(data[i] + "_gamesLog.csv"), "2018-12-08"))
        i += 1

    return array

## Under Development Farming Vegas Odds and Factoring these into prediction
## Model

##def todaysOddsOverUnder():
##
##    current_url = "http://www.vegasinsider.com/nba/odds/las-vegas/"
##
##    uClient = uReq(current_url)
##    page_html = uClient.read()
##    uClient.close()
##    page_soup = soup(page_html, "html.parser")
##
##
##    table = page_soup.find("table", {"class":"frodds-data-tbl"})
##    rows  = table.find_all("tr")
##
##    for row in rows:
##
##        print("Hello")
  

PreviousGamesAnalysis()
addMovingAverages()
print("")
print(tonightsGames("january", "Fri, Jan 11, 2019"))
print(arrayNumberDaysRested(tonightsGames("january", "Fri, Jan 11, 2019")))
generateTonightsPlots(tonightsGames("january", "Fri, Jan 11, 2019"))
