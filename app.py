import pandas as pd
import streamlit as st
import plotly.express as px
from GoogleNews import GoogleNews
import SessionState
import templates
import requests


import odds

team_state= SessionState.get(team=None)
googlenews = GoogleNews(lang='en', period='1d')

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def odds_layout(tname,odds):
    wch_colour_box = (84, 240, 67)
    wch_colour_font = (0, 0, 0)
    fontsize = 24
    valign = "left"
    iconname = "fas fa-check-circle"
    sline = tname + " to win"
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    i = odds

    htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                      {wch_colour_box[1]}, 
                                                      {wch_colour_box[2]}, 0.75); 
                                color: rgb({wch_colour_font[0]}, 
                                           {wch_colour_font[1]}, 
                                           {wch_colour_font[2]}, 0.75); 
                                font-size: {fontsize}px; 
                                border-radius: 7px; 
                                padding-left: 2px; 
                                padding-top: 12px; 
                                padding-bottom: 12px;
                                text-align:center;
                                line-height:25px;'>
                                <i class='{iconname} fa-xs'></i> {i}
                                </style><BR><span style='font-size: 25px; 
                                margin-top: 0;'>{sline}</style></span></p>"""
    return htmlstr,lnk
def odds_layout_draw(odds):
    wch_colour_box = (255, 252, 245)
    wch_colour_font = (0, 0, 0)
    fontsize = 30
    valign = "right"
    iconname = "glyphicon glyphicon-remove"
    sline = "Draw"
    lnk = '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">'
    i = odds

    htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                      {wch_colour_box[1]}, 
                                                      {wch_colour_box[2]}, 0.75); 
                                color: rgb({wch_colour_font[0]}, 
                                           {wch_colour_font[1]}, 
                                           {wch_colour_font[2]}, 0.75); 
                                font-size: {fontsize}px; 
                                border-radius: 7px; 
                                padding-left: 2px; 
                                padding-top: 12px; 
                                padding-bottom: 12px; 
                                line-height:25px;
                                text-align:center;
                                height: 130px;'>
                                <i class='{iconname} fa-xs'></i> {i}
                                </style><BR><span style='font-size: 30px; 
                                margin-top: 0;'>{sline}</style></span></p>"""
    return htmlstr,lnk

def tables(Standard_Stats):
    z=secondary_option(Standard_Stats)
    option_2 = st.selectbox('Select Secondary Data to view',z)
    final_columns=[( 'Unnamed: 0_level_0',  'Player')]
    for i in Standard_Stats.columns:
        if option_2==i[0]:
            final_columns.append(i)
    #print(final_columns)
    Standard_Stats=Standard_Stats[final_columns]
    Standard_Stats.columns=Standard_Stats.columns.droplevel()
    list(Standard_Stats.columns).remove('Player')
    print(Standard_Stats)
    k1 = list(Standard_Stats.columns)
    k1.remove('Player')
    # st.write(k1)
    x_axis = st.selectbox('Select x axis', k1)
    k = list(Standard_Stats.columns)
    k.remove(x_axis)
    k.remove('Player')
    y_axis = st.selectbox('Select y axis', k)
    button1=st.button("Create Graph")
    #df = df[:len(df) - 2]
    #st.table(df)
    if button1:
        df=Standard_Stats[[x_axis,y_axis,'Player']]
        df=df[:len(df)-2]
        print("Result")
        fig = px.scatter(df,x=x_axis,y=y_axis,color='Player')
        st.title("Scatter plot")
        st.write('On this plot, we see the standing of eac player in relation to other players of the same team')
        st.plotly_chart(fig,use_container_width = True)
        st.sidebar.title("Current Table ")
        st.sidebar.dataframe(df)
        Standard_Stats=Standard_Stats.sort_values(x_axis,axis=0,ascending=False).reset_index(drop=True)
        st.title("Box")
        st.write('Here, we look out for the average performence of the team and weather the team as a whole is performing or there are any individual brilliances or individual disasters')
        col1, col2 = st.columns([1, 1])
        fig3 = px.box(Standard_Stats[2:len(Standard_Stats)], y=x_axis)
        fig4 = px.box(Standard_Stats[2:len(Standard_Stats)], y=y_axis)
        col1.plotly_chart(fig3,use_container_width = True)
        col2.plotly_chart(fig4,use_container_width = True)
        df_line=pd.DataFrame()
        print(Standard_Stats)
        for i in list(Standard_Stats.columns):
            if i=='Player':
                continue
            df_line['{}'.format(i)]=Standard_Stats['{}'.format(i)].rank(pct=True)
        df_line['Player']=Standard_Stats['Player']
        df_line=df_line[2:7]
        df_line=df_line.set_index('Player',drop=True)
        df_line=df_line.transpose()
        st.title("Line Plot")
        st.write('Here we take the top 5 players for all the stats and convert the values into percentile.Then we plot each as a line.This shows us the realtion between diffrent statistics')
        fig1 = px.line(df_line)
        st.plotly_chart(fig1,use_container_width = True)



def secondary_option(df):
    z=[]
    for i in df.columns:
        if 'Unnamed' in i[0]:
            continue
        z.append(i[0])
    z=list(set(z))
    return z

def tables1(stat):

    final_columns = [('Unnamed: 0_level_0', 'Player')]
    for i in Standard_Stats.columns:
        if option_2 == i[0]:
            final_columns.append(i)
    print(final_columns)
    Standard_Stats = Standard_Stats[final_columns]
    Standard_Stats.columns = Standard_Stats.columns.droplevel()
    list(Standard_Stats.columns).remove('Player')

st.set_page_config(layout = "wide")

st.header("Football Team Page")



PAGES = {
    "Select Team":"team",
    "News":"news",
    "Statistics":"stats"
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

page1 = PAGES[selection]
opt = ['Manchester United','PSG','Bayern Munich','Real Madrid']
img_url = {
        "Manchester United": "logos/manutd.png",
        "PSG": "logos/psg.png",
        "Bayern Munich": "logos/bayern.png",
        "Real Madrid": "logos/madrid.png"
    }


if page1=='team':
    team_state.team=st.selectbox("Choose your favorite team",opt)
    col1,col2,col3 = st.columns(3)

    col2.image(img_url[team_state.team],width=300)



if page1=='news':

    st.title('Team News')
    team_state.team = st.selectbox("Choose your favorite team", opt)
    
    col1,col2,col3 = st.columns(3)

    col2.image(img_url[team_state.team],width=300)


    #card(title="Hello World!", text="Some description", image="http://placekitten.com/200/300")
    search_button = st.button("Search Team News")



    if search_button:
        #card(title="Hello World!", text="Some description", image=img_url[team_state.team])
        st.write("Next Match Odds presented by MarathonBet")
        col1, col2, col3 = st.columns(3)

        if team_state.team=='Manchester United':
            home_team,away_team,home_odds,draw_odds,away_odds= odds.odds_pl()
        elif team_state.team=='PSG':
            home_team,away_team,home_odds,draw_odds,away_odds= odds.odds_l1()
        elif team_state.team=='Bayern Munich':
            home_team,away_team,home_odds,draw_odds,away_odds= odds.odds_bun()
        elif team_state.team=='Real Madrid':
            home_team,away_team,home_odds,draw_odds,away_odds= odds.odds_ll()

        htmlstr1, lnk1 = odds_layout(home_team, home_odds)
        htmlstr2, lnk2 = odds_layout_draw(draw_odds)
        htmlstr3, lnk3 = odds_layout(away_team, away_odds)

        col1.markdown(lnk1 + htmlstr1, unsafe_allow_html=True)
        col2.markdown(lnk2 + htmlstr2, unsafe_allow_html=True)
        col3.markdown(lnk3 + htmlstr3, unsafe_allow_html=True)
        # googlenews.search(team_state.team)
        # res = googlenews.results()
        # googlenews.clear()

        # i=0
        # for result in res:
        #     print('\n\nTITLE:', result['title'], '\nDESC:', result['desc'], '\nURL: ', result['link'])
        #     res1 = result
        #     res1['url'] = result['link']
        #     res1['highlights'] = result['desc']
        #     res1['title'] = result['title']
        #     st.image(result['img'])
        #     st.write(templates.search_result(i, **res1), unsafe_allow_html=True)
        #     i+=1


        API_KEY = 'fec055a537f44c58ae827c8e15a45dfc'
        #Team = 'Manchester United'
        url = f"https://newsapi.org/v2/everything?q={team_state.team}&sortBy=popularity&apiKey={API_KEY}"
        r = requests.get(url)
        r = r.json()
        art = r['articles']
        i=0

        for a in art:
            col1,col2=st.columns(2)
            res1 = a
            c1 = col1.container()
            c2 = col2.container()
            col1.image(a['urlToImage'],width=400)
            res1['title'] = a['title']
            res1['url'] = a['url']
            res1['highlights'] = a['description']

            col2.write(templates.search_result(i, **res1), unsafe_allow_html=True)
            i+=1
            if i==10:
                break



if page1=='stats':
    #card(title="Hello World!", text="Some description", image='logo')
    team_state.team = st.sidebar.selectbox("Choose your favorite team", opt)
    st.write(
        "Here we look at the individual stats taken from fbref,and compare them using data that you select.Yes this tool is an interactive and user friendly tool which gives user the power of customization which they can use to create their own graphs.")

    team_url = {
        "Manchester United": "https://fbref.com/en/squads/19538871/Manchester-United-Stats",
        "PSG": "https://fbref.com/en/squads/e2d8892c/Paris-Saint-Germain-Stats",
        "Bayern Munich": "https://fbref.com/en/squads/054efa67/Bayern-Munich-Stats",
        "Real Madrid": "https://fbref.com/en/squads/53a2f082/Real-Madrid-Stats"
    }
    u1 = team_url[team_state.team]
    url =  u1
    df = pd.read_html(url)
    print(url)
    Standard_Stats=df[0]
    GoalKeeping=df[2]
    Passing=df[5]
    Advanced_Goalkeeping=df[3]
    Shooting=df[4]
    Pass_Types=df[6]


    option_1=['Standard Stats','Goalkeeping','Passing','Advanced GoalKeeping','Shooting','Pass Types']
    st.sidebar.image(img_url[team_state.team])

    st.title("Team Analysis")
    page = st.selectbox('Select Primary Data to view',option_1)



    if page=='Standard Stats':

        tables(Standard_Stats)

    if page=='Goalkeeping':
        tables(GoalKeeping)
    if page=='Passing':
        tables(Passing)
    if page=='Advanced GoalKeeping':
        tables(Advanced_Goalkeeping)
    if page=='Shooting':
        tables(Shooting)
    if page=='Pass Types':
        tables(Pass_Types)







