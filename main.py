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

# INTRO CARD

intro_card = dbc.Card(

    dbc.CardBody(
        [

            html.H2('Dashboard Introduction', className='card-title'),
            html.P('In this Dashboard, I am comparing different video streaming platforms such as Netflix, '
                   'Prime Video and Hulu.'),
            html.P('I have used 3 datasets for performing this comparison, namely the Netflix, Hulu and Disney+ datasets '
                   'which are all released by Kaggle user Shivam Bansal.'
                   'Netflix Dataset - https://www.kaggle.com/shivamb/netflix-shows '
                    'Prime Dataset - https://www.kaggle.com/shivamb/amazon-prime-movies-and-tv-shows '
                   'Hulu Dataset-https://www.kaggle.com/shivamb/hulu-movies-and-tv-shows')

        ]
    )

)

# LEFT CARD
left_card = dbc.Card(

    dbc.CardBody(
        [
            html.H4("Primary Component- Distribution for Movies and TV Shows", className="card-title"),
            html.P('In the left component, A streaming service provider '
                   'can be selected from the Dropdowns to get insights on the number of Movies and'
                   ' TV shows that are present on the respective service provider.'),
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
            html.P(' In the right component, a line chart visualizing the total releases per year '
                   '(both Movies and TV shows) has been generated. '
                   'The Radiobuttons can be used to toggle between service providers'),
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

# CONTEXTUAL VISUALIZATION 1

cv1_card = dbc.Card(
    dbc.CardBody([

        html.H4("Contextual Visualization 1", className='card-title', style={'margin-bottom': '20px'}),
        html.P('This visualization includes The Disney+ Dataset and compares it with the Netflix data to '
               'give us some additional context. This visualization has been referenced from Kaggle user KS_LAR_WTF in their '
               'EDA analysis comparing Netflix and Disney+ https://www.kaggle.com/kslarwtf/disney-vs-netflix-make-your-eda-great'),
        dbc.CardImg(src=app.get_asset_url('disneyvsnetflix.jpg'), top=True, style={'width': '200px', 'height':'100px'}),
        dbc.CardImg(src=app.get_asset_url('comparison.png'), top=True, style={'width': '600px', 'height':'200px',
                                                                              'padding-right':'40px'}),

    ])
)

# CONTEXTUAL VISUALIZATION 2

cv2_card = dbc.Card(
    dbc.CardBody([

        html.H4("Contextual Visualization 2", className='card-title',style={'margin-bottom': '20px'}),
        html.P('This visualization helps give context about how Disney+ has been releasing its TV shows and Movies '
               'over the years. It is referenced from Kaggle User EMRE ARSLAN where they perform EDA on Disney+ '
               'https://www.kaggle.com/emrearslan123/eda-on-disney-movies-and-tv-shows-dataset'),
    dbc.CardImg(src=app.get_asset_url('disney.png'), top=True, style={'width': '600px', 'height':'200px',
                                                                              'padding-right':'40px'}),

    ])
)

# DEFINE THE APP LAYOUT

app.layout = dbc.Container([

    dbc.Row(
        dbc.Col(html.H2("STREAMING PLATFORMS INSIGHTS",
                        className='text-center'),
                width=12)
    ),

    dbc.Row([

        dbc.Col(intro_card, style={'background': '#0047AB', 'padding': '17px', 'margin': '20px'})

    ]),

    dbc.Row([

        dbc.Col(left_card, width={'size': 5, 'offset': 0},
                style={'background': '#0047AB', 'padding': '17px', 'margin': '20px'}),

        dbc.Col(right_card, width={'size': 6, 'offset': 1},
                style={'background': '#0047AB', 'padding': '17px', 'margin': '20px'}),

    ]),

    dbc.Row([

        dbc.Col(cv1_card, width={'size': 5, 'offset': 0},
                style={'background': '#0047AB', 'padding': '17px', 'margin': '20px'}),
        dbc.Col(cv2_card, width={'size': 6, 'offset': 0},
                style={'background': '#0047AB', 'padding': '17px', 'margin': '20px'})
    ]),

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
