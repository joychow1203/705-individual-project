import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash import dash_table
import plotly.express as px
import pandas as pd
import numpy as np


movies = pd.read_csv("movies_list_df.csv", index_col=0)
directors = pd.read_csv("directors_rating.csv", index_col=0)

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

"""
def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns],
                    style={"font-family": "Calibri"})
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ], style={'margin-left': '50px','margin-right': '50px','padding-left': '200px',"font-family": "Calibri"})
    ])
"""

app = dash.Dash(__name__, external_stylesheets=stylesheet)

movies = movies.drop(['Year Range',"Link"], axis=1)

fig1 = px.scatter(movies, x="Year", y="IMDB Rating", color="Primary Genre", size="Votes", size_max=40, opacity=0.6, 
                  hover_name="Title", title="Movies by Released Year, Rating, and Primary Genre")
fig2 = px.bar(directors, x="Director", y="Count", color="Average Rating", 
              labels={"Count":"Number of Movies"}, title="Average Ratings of Movies from Top Directors")

# dashboard layout
app.layout = html.Div([
    html.H1('Mystery & Horror Movie Dashboard',
            style={'textAlign' : 'left', "font-family": "Source Serif Pro", "color": '#1f77b4', 'padding': 20}),
    html.B("About this dashboard", style={"font-family": "Calibri", "font-size": "22px", "color": '#1f77b4','padding-left': 20}),
    html.P(["You can explore 182 top-rated mystery and horror movies based on the following search criteria:",
            html.Br(),"1) Select a rating value to see all movies with this IMDB score and above.",
            html.Br(),"2) Select a year to see all movies released in this year and later.",
            html.Br(),"3) Select a country to find directors who belong and have more than one movie on this list."],
            style={"font-family": "Calibri", "font-size": "18px", 'padding-left': 20}),

html.Hr(),
    dcc.Graph(figure=fig1, id='movie_plot'),

# section of movies
html.Div([
    html.Div([
    html.H5("Select the rating of the movie:", style={'textAlign' : 'center', "font-family": "Calibri", 'width' : '90%'}),
    html.Div(dcc.Slider(min=5.5,max=9,step=0.5,value=5.5, id='rating_input',
                        tooltip={"placement": "bottom", "always_visible": True}),
             style={'width':'90%', 'padding': 20})],className="six columns"),
    
    html.Div([
    html.H5("Select the year of the movie:", style={'textAlign' : 'center', "font-family": "Calibri", 'width' : '90%',}),
    html.Div(dcc.Slider(
        id='year_input',
        min=1920,
        max=2020,
        value=1920,
        marks={str(year):str(year) for year in range(1920, 2030, 10)},
        step=None
    ),style={'width':'90%','padding': 20})], className="six columns")
    ], className="row"),
    
    html.Div(id='table_div'),
html.Hr(),

# section of directors
html.Div([
    html.Div([
    html.H5("Select a country to find directors:",
            style={"font-family": "Calibri", 'width' : '90%','padding-left': 50}),
    html.Div(dcc.Checklist(
                  options=[{'label': 'United States', 'value': 'US'},
                           {'label': 'United Kingdom', 'value': 'UK'},
                           {'label': 'Other Countries', 'value': 'Other'}],
                  id = 'director_checklist', value = "US",
                  style={'width' : '90%', 'padding': 50, "font-family": "Calibri", "font-size": "18px"}))],
        className="five columns"),
    html.Div([dcc.Graph(figure=fig2, id='director_plot', 
                        style={'float' : 'right'})],
             className="seven columns")], className="row"),

html.Hr(),
# references
    html.B("References", style={"font-family": "Calibri", "font-size": "18px", "color": '#1f77b4','padding-left': 20}),
    html.P(["- Top 100 Mystery & Suspense Movies: https://www.rottentomatoes.com/top/bestofrt/top_100_mystery__suspense_movies/",
            html.Br(),"- Top 100 Horror Movies: https://www.rottentomatoes.com/top/bestofrt/top_100_horror_movies/",
            html.Br(),"- IMDB Database: https://www.imdb.com/interfaces/"],
            style={"font-family": "Calibri", "font-size": "14px", 'padding-left': 20}),
    html.P("MA 705 | Fall 2021 | Joy Chow", style={"font-family": "Calibri", "font-size": "16px", 'padding-left': 20})

])


# directors' ratings plot
@app.callback(
    Output(component_id='director_plot', component_property="figure"),
    [Input(component_id="director_checklist", component_property="value")]
)
def update_plot2(countries):
    directors_selected = directors[directors.Country.isin(countries)].sort_values("Count", ascending=False)
    fig2 = px.bar(directors_selected, x="Director", y="Count", color="Average Rating", 
                  labels={"Count":"Number of Movies"}, title="Average Ratings of Movies from Top Directors")
    return fig2


# movies plot
@app.callback(
    Output(component_id="movie_plot", component_property="figure"),
    [Input(component_id="rating_input", component_property="value"),
     Input(component_id="year_input", component_property="value")]
)
def update_plot1(rating, year):
    selected = movies[(movies["IMDB Rating"]>=rating) & (movies["Year"]>=year)]
    fig1 = px.scatter(selected, x="Year", y="IMDB Rating", color="Primary Genre", size="Votes", size_max=40, opacity=0.6,
                      hover_name="Title", title="Movies by Released Year, Rating, and Primary Genre")
    return fig1

# movies table
@app.callback(
    Output(component_id="table_div", component_property="children"),
    [Input(component_id="rating_input", component_property="value"),
     Input(component_id="year_input", component_property="value")]
)

def update_table(rating, year):
    selected = movies[(movies["IMDB Rating"]>=rating) & (movies["Year"]>=year)]
    return dash_table.DataTable(style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        "font-family": "Calibri", "font-size": "16px"
    },
        style_header={
        "font-family": "Calibri", "font-size": "17px", 'fontWeight': 'bold',
        'backgroundColor': 'rgb(210, 210, 210)',
        'color': 'black'
    },
    style_cell={
        'height': 'auto',
        'minWidth': '30px', 'width': '130px', 'maxWidth': '550px',
        'whiteSpace': 'normal'
    },
    data=selected.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in movies.columns],
    sort_action="native",
    fixed_columns={'headers': True, 'data': 1},
    fixed_rows={'headers': True},
    style_table={'height': 500, 'minWidth': '100%'},
    style_cell_conditional=[
        {'if': {'column_id': 'Description'},
         'width': '550px'},
        {'if': {'column_id': 'Critics Review'},
         'width': '300px'}])


server = app.server

if __name__ == '__main__':
    app.run_server()

