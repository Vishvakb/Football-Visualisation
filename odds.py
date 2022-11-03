import pandas as pd
import urllib.request

def odds_pl():
    url = 'https://www.marathonbet.com/en/popular/Football/England+-+21517'


    req = urllib.request.Request(url, headers= {"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req)
    dfs = pd.read_html(html)
    #df = dfs[3]
    j = 2
    while j <= len(dfs) - 1:
        try:
            team1 = dfs[j][0][1][4:]
            team2 = dfs[j][0][2][4:]
            team1_odds = dfs[j][2][0]
            team2_odds = dfs[j][6][0]
            draw_odds = dfs[j][4][0]
            if team1 == 'Manchester United' or team2 == 'Manchester United':
                return team1,team2,team1_odds,draw_odds,team2_odds
            j += 3
        except:
            j += 3
            continue


def odds_l1():
    url = 'https://www.marathonbet.com/en/popular/Football/France/Ligue+1+-+21533'

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req)
    dfs = pd.read_html(html)
    # df = dfs[3]

    # df[0][2][4:]
    j = 2
    while j <= len(dfs) - 1:
        try:
            team1 = dfs[j][0][1][4:]
            team2 = dfs[j][0][2][4:]
            team1_odds = dfs[j][2][0]
            team2_odds = dfs[j][6][0]
            draw_odds = dfs[j][4][0]
            if team1 == 'Paris Saint-Germain' or team2 == 'Paris Saint-Germain':
                return team1,team2,team1_odds,draw_odds,team2_odds
            j += 3
        except:
            j += 3
            continue

def odds_bun():
    url = 'https://www.marathonbet.com/en/popular/Football/Germany/Bundesliga+-+22436'


    req = urllib.request.Request(url, headers= {"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req)
    dfs = pd.read_html(html)
    #df = dfs[3]


    #df[0][2][4:]
    j = 2
    while j<=len(dfs)-1:
        try:
            team1 =  dfs[j][0][1][4:]
            team2 = dfs[j][0][2][4:]
            team1_odds = dfs[j][2][0]
            team2_odds  = dfs[j][6][0]
            draw_odds = dfs[j][4][0]
            if team1=='Bayern Munich' or team2=='Bayern Munich':
                return team1,team2,team1_odds,draw_odds,team2_odds
            j+=3
        except:
            j+=3
            continue


def odds_ll():
    url = 'https://www.marathonbet.com/en/popular/Football/Spain/Primera+Division+-+8736'

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req)
    dfs = pd.read_html(html)
    # df = dfs[3]

    # df[0][2][4:]
    j = 2
    while j <= len(dfs) - 1:
        try:
            team1 = dfs[j][0][1][4:]
            team2 = dfs[j][0][2][4:]
            team1_odds = dfs[j][2][0]
            team2_odds = dfs[j][6][0]
            draw_odds = dfs[j][4][0]
            if team1 == 'Real Madrid' or team2 == 'Real Madrid':
                print(team1 + ':' + str(team1_odds) + ':' + str(draw_odds) + ' ' + team2 + ':' + str(team2_odds))
                return team1, team2, team1_odds, draw_odds, team2_odds
            j += 3
        except:
            j += 3
            continue
