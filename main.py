# IMPORT LIBRARIES
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
from dash import dash_table
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

# LOAD DATASETS
netflix = pd.read_csv("netflix_titles.csv")
prime = pd.read_csv("amazon_prime_titles.csv")
hulu = pd.read_csv("hulu_titles.csv")

# CREATE A DASH APP
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# CREATE ALL COMPONENTS AS A RESPONSIVE BOOTSTRAP CARD

# LEFT CARD
left_card = dbc.Card(

    dbc.CardBody(
        [
            html.H4("Distribution for Movies and TV Shows", className="card-title"),
            dcc.Dropdown(
                id='dpdn',
                options=[
                    {'label': 'Netflix', 'value': 'NFLX'},
                    {'label': 'Prime Video', 'value': 'PRME'},
                    {'label': 'Hulu', 'value': 'HULU'}
                ],
                placeholder="Select a streaming service",
            ),
            dcc.Graph(id='bar-chrt', figure={})

        ]

    )

)

# RIGHT CARD
right_card = dbc.Card(

    dbc.CardBody(

        [
            html.H4("Yearly Releases", className="card-title"),
            dcc.RadioItems(
                id='cl',
                options=[
                    {'label': 'Netflix', 'value': 'NFLX'},
                    {'label': 'Prime Video', 'value': 'PRME'},
                    {'label': 'Hulu', 'value': 'HULU'}
                ],
                labelStyle={'display': 'inline-block'},
                value='NFLX',
            ),

            dcc.Graph(id='lc', figure={})

        ]

    )

)

# DEFINE THE APP LAYOUT

app.layout = dbc.Container([

    dbc.Row(
        dbc.Col(html.H2("STREAMING PLATFORMS INSIGHTS",
                        className='text-center'),
                width=12)
    ),
    dbc.Row(
        dbc.Col(html.H2("Dashboard Introduction",
                        className=''),
                width=12)
    ),
    dbc.Row([

        dbc.Col(left_card, width={'size': 5, 'offset': 0}),

        dbc.Col(right_card, width={'size': 6, 'offset': 1}),

    ]),

    dbc.Row([

        # dbc.Col(map_card)

    ])

], fluid=True,
)

# CALLBACK FOR BAR CHART

netflix['release_year'] = netflix['release_year'].astype(int)
netflixline = netflix[netflix['release_year'] > 2005]

prime['release_year'] = prime['release_year'].astype(int)
primeline = prime[prime['release_year'] > 2005]

hulu['release_year'] = hulu['release_year'].astype(int)
hululine = hulu[hulu['release_year'] > 2005]


@app.callback(
    Output('bar-chrt', 'figure'),
    Input('dpdn', 'value')
)
def update_graph(service_slctd):
    figbar = px.bar()

    if service_slctd == "NFLX":
        figbar = px.bar(netflix, x=netflix['type'].unique(), y=netflix['type'].value_counts(),
                        color_discrete_sequence=["red"],
                        labels={'x': 'Netflix', 'y': 'Count'})
        return figbar

    elif service_slctd == 'PRME':
        figbar = px.bar(prime, x=prime['type'].unique(), y=prime['type'].value_counts(),
                        color_discrete_sequence=["blue"],
                        labels={'x': 'Prime Video', 'y': 'Count'})
        return figbar

    elif service_slctd == 'HULU':
        figbar = px.bar(hulu, x=hulu['type'].unique(), y=hulu['type'].value_counts(), color_discrete_sequence=["green"],
                        labels={'x': 'Hulu', 'y': 'Count'})
        return figbar

    return figbar


# CALLBACK FOR LINE CHART

@app.callback(
    Output('lc', 'figure'),
    Input('cl', 'value')
)
def update_graph(service_selctd):
    figline = px.line()

    if "NFLX" in service_selctd:
        figline = px.line(netflixline, x=netflixline['release_year'].unique(),
                          y=netflixline['release_year'].value_counts(), color_discrete_sequence=["red"],
                          labels={'x': 'Netflix', 'y': 'Releases'}, height=450, markers=True)
        return figline

    elif 'PRME' in service_selctd:
        figline = px.line(primeline, x=primeline['release_year'].unique(), y=primeline['release_year'].value_counts(),
                          color_discrete_sequence=["blue"], labels={'x': 'Prime', 'y': 'Releases'}, height=450,
                          markers=True)
        return figline

    elif 'HULU' in service_selctd:
        figline = px.line(hululine, x=hululine['release_year'].unique(), y=hululine['release_year'].value_counts(),
                          color_discrete_sequence=["green"], labels={'x': 'Hulu', 'y': 'Releases'}, height=450,
                          markers=True)
        return figline

    return figline


# RUN THE APP
app.run_server(debug=True, port=8050)
