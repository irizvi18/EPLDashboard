import dash
import json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from flask import Flask
import numpy as np
import plotly.express as px
import pandas as pd

server = Flask(__name__)
app=dash.Dash(__name__, server=server)



def findPointProgression(matchesData, teamID):
    toSubset = [False] * len(matchesData)
    count = 0
    for MN in matchesData['teamsData']:
        if(list(MN.keys())[0] == teamID or list(MN.keys())[1] == teamID):
            
            toSubset[count] = True
        count=count+1
    teamGames = matchesData.loc[toSubset]
    teamGames = teamGames.sort_values('dateutc')

    ptsSeason = [0] * 39
    count = 1
    for win in teamGames['winner']:
        #print(win)
        if(str(win)==teamID):
            ptsSeason[count] = ptsSeason[count-1] + 3
        elif(win == 0):
            ptsSeason[count] = ptsSeason[count-1] + 1
        else:
            ptsSeason[count] = ptsSeason[count-1]
        count=count+1
    return(ptsSeason)


matches={}
nations = ['England']
for nation in nations:
    with open('./matches_%s.json' %nation) as json_data:
        matches[nation] = json.load(json_data)

teams={}
with open('./teams.json') as json_data:
    teams = json.load(json_data)

df_matches = pd.DataFrame(matches['England'])
df_teams = pd.DataFrame(teams)

allTeams = ["Empty"] * 20
allIds = [0] * 20
count = 0
for index,row in df_teams.iterrows():
    if(row['type'] == 'club'):
        if(row['area']['name'] == 'England' or row['area']['name'] == 'Wales'):
            allTeams[count] = row['name']
            allIds[count] = row['wyId']
            count=count+1




GamesPlayed = list(range(0,39))
sznPoints = pd.DataFrame(
{'GamesPlayed': GamesPlayed})

for num in range(20):
    sznPoints[str(allTeams[num])] = findPointProgression(df_matches, str(allIds[num]))




fig = px.line(sznPoints, x="GamesPlayed", y="Manchester City")




app.layout = html.Div(children=[
	html.H1('Premier League 2017/18 Season'),
	dcc.Checklist(
		id = 'whichTeams',
        options=[
            {'label': 'Arsenal', 'value': 'Arsenal'},
            {'label': 'AFC Bournemouth', 'value': 'AFC Bournemouth'},
            {'label': 'Brighton & Hove Albion', 'value': 'Brighton & Hove Albion'},
            {'label': 'Burnley', 'value': 'Burnley'},
            {'label': 'Chelsea', 'value': 'Chelsea'},
            {'label': 'Crystal Palace', 'value': 'Crystal Palace'},
            {'label': 'Everton', 'value': 'Everton'},
            {'label': 'Huddersfield Town', 'value': 'Huddersfield Town'},
            {'label': 'Leicester City', 'value': 'Leicester City'},
            {'label': 'Liverpool', 'value': 'Liverpool'},
            {'label': 'Manchester City', 'value': 'Manchester City'},
            {'label': 'Manchester United', 'value': 'Manchester United'},
            {'label': 'Newcastle United', 'value': 'Newcastle United'},
            {'label': 'Southampton', 'value': 'Southampton'},
            {'label': 'Stoke City', 'value': 'Stoke City'},
            {'label': 'Swansea City', 'value': 'Swansea City'},
            {'label': 'Tottenham Hotspur', 'value': 'Tottenham Hotspur'},
            {'label': 'Watford', 'value': 'Watford'},
            {'label': 'West Bromwich Albion', 'value': 'West Bromwich Albion'},
            {'label': 'West Ham United', 'value': 'West Ham United'}
        ],
        value=''
    ),
	dcc.Graph(
        id='example-graph',
        figure=fig
    )
	])


@app.callback(
	Output(component_id= 'example-graph',component_property='figure'),
	[Input('whichTeams','value')]
)
def update_fig(input_value):
	fig = px.line(sznPoints, x="GamesPlayed", y=input_value, title="Point Total After Each Game")
	return fig

if __name__ == '__main__':
	app.run_server(debug=True)

