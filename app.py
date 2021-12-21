


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_table
import plotly.express as px
import pandas as pd
import numpy as np


movies = pd.read_csv("movies_list_df.csv", index_col=0)
directors = pd.read_csv("directors_rating.csv", index_col=0)

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

### pandas dataframe to html table
def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app = dash.Dash(__name__, external_stylesheets=stylesheet)

fig1 = px.scatter(movies, x="Year", y="IMDB Rating", color="Primary Genre", size="Votes", size_max=40, opacity=0.6, 
                  hover_name="Title", title="Movies by Released Year, Rating, and Primary Genre")
fig2 = px.bar(directors, x="Director", y="Count", color="Average Rating", labels={"Count":"Number of Movies"}, title="Average Ratings of Movies from Top Directors")


app.layout = html.Div([
    html.H1('Mystery & Horror Movie Dashboard',
            style={'textAlign' : 'left', "font-family": "Source Serif Pro", "color": '#1f77b4'}),
    html.Br(),
    dcc.Graph(figure=fig1, id='movie_plot'),

    html.Div([
    html.H5("Select the rating of the movie:", style={'textAlign' : 'center', "font-family": "Calibri", 'width' : '30%'}),
    html.Div(dcc.Slider(min=5.5,max=9,step=0.5,value=5, id='rating_input',tooltip={"placement": "bottom", "always_visible": True}),style={'width':'35%'})]),
    
    html.Div(id='table_div'),
    html.Br(),
    html.H5("Select countries to find top directors with more than one movie",style={'textAlign' : 'left', "font-family": "Calibri", 'width' : '40%'}),
              html.Div(dcc.Checklist(
                  options=[{'label': 'United States', 'value': 'US'},
                           {'label': 'United Kingdom', 'value': 'UK'},
                           {'label': 'Other Countries', 'value': 'Other'}],
                  id = 'director_checklist', style={'width' : '10%', 'float' : 'left', 'padding': 10})),
    dcc.Graph(figure=fig2, id='director_plot', style={'width' : '60%', 'float' : 'right'})])


# directors' ratings plot
@app.callback(
    Output(component_id='director_plot', component_property="figure"),
    [Input(component_id="director_checklist", component_property="value")]
)
def update_plot2(countries):
    directors_selected = directors[directors.Country.isin(countries)].sort_values("Average Rating", ascending=False)
    fig2 = px.bar(directors_selected, x="Director", y="Count", color="Average Rating", labels={"Count":"Number of Movies"}, title="Average Ratings of Movies from Top Directors")
    return fig2


# movies plot
@app.callback(
    Output(component_id="movie_plot", component_property="figure"),
    [Input(component_id="rating_input", component_property="value")]
)
def update_plot1(rating):
    ratings_selected = movies[movies["IMDB Rating"]>=rating]
    fig1 = px.scatter(ratings_selected, x="Year", y="IMDB Rating", color="Primary Genre", size="Votes", size_max=40, opacity=0.6,
                      hover_name="Title", title="Movies by Released Year, Rating, and Primary Genre")
    return fig1

# movies table
@app.callback(
    Output(component_id="table_div", component_property="children"),
     Input(component_id='rating_input', component_property="value")
)

def update_table(rating):
    ratings_selected = movies[movies["IMDB Rating"]>=rating].drop(['Primary Genre','Year Range',"Link"], axis=1)
    return generate_table(ratings_selected)


server = app.server

if __name__ == '__main__':
    app.run_server()

