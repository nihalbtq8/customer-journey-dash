# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from app import app, indicator, millify, df_to_table, connect_gp, connect_ga
import pandas as pd
from datetime import date, timedelta


external_scripts = [
    'https://www.google-analytics.com/analytics.js',
    {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
        'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
        'crossorigin': 'anonymous'
    }
]

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

country_dict = {"Bahrain" : ["BH", "BHR", "048"],
"Oman" : ["OM", "OMN", "512"],
"Kuwait" : ["KW", "KWT", "414"],
"United Arab Emirates" : ["AE", "ARE", "784"],
"Qatar" : ["QA", "QAT", "634"],
"Saudi Arabia" : ["SA", "SAU", "682"]}

conn = connect_ga()

def get_df():
    query_map = "select * from traffic_datewise where country in ('Saudi Arabia', 'Kuwait', 'United Arab Emirates', 'Qatar', \
    'Oman', 'Bahrain') and month(date) = month(subdate(current_date, interval 1 day)) and year(date) = year(subdate(\
    current_date, interval 1 day))"
    return pd.read_sql(query_map, conn)

df_chor = get_df()

def choropleth_map(granularity, metric, df=df_chor):
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    if granularity == 'day':
        df = df.loc[df['date'].dt.date == (date.today() - timedelta(days=1))]
        df['country_code'] = df['country'].apply(lambda x: country_dict[x][1])
    elif granularity == 'week':
        df = df.loc[df['date'].dt.strftime("%U") == (date.today() - timedelta(days=1)).\
            strftime("%U")]
        df['country_code'] = df['country'].apply(lambda x: country_dict[x][1])
    elif granularity == 'month':
        df = df.loc[df['date'].dt.month == (date.today() - timedelta(days=1)).month]
        df['country_code'] = df['country'].apply(lambda x: country_dict[x][1])

    scl = [
        [0, "#0F0020"],
        [0.2, "#37003C"],
        [0.4, "#660053"],
        [0.6, "#A40057"],
        [0.8, "#D9003F"],
        [1, "#E9141C"], ]

    data = [go.Choropleth(
        locations=df['country_code'],
        z=df[metric],
        text=df['country'],  # colorscale="Electric",
        colorscale=scl,
        marker=dict(line=dict(color="rgb(255,255,255)", width=2)),
        colorbar=go.choropleth.ColorBar(
            title=metric.title()),
    )]

    map_layout = go.Layout(
        title=go.layout.Title(
            text='Users by Country'
        ),
        geo=go.layout.Geo(
            showframe=False,
            showcoastlines=False,
            lakecolor="rgb(255, 255, 255)",
            projection=go.layout.geo.Projection(
                type='equirectangular'
            ),
            showland=True,
            landcolor="rgb(229, 229, 229)",
            countrycolor="rgb(255, 255, 255)",
            coastlinecolor="rgb(255, 255, 255)",
            center={"lat": 25.92, "lon": 45.816},
            lonaxis={"range": [30, 60]},
            lataxis={"range": [10, 35]}
        ),
        margin=dict(l=0, r=0, t=0, b=0),
    )

    return dict(data=data, layout=map_layout)



@app.callback(
    Output("choropleth_map", "figure"),
    [Input("granularity_dropdown", "value"), Input("metric_dropdown", "value")],
)
def map_callback(granularity, metric):
    return choropleth_map(granularity, metric, df_chor)


layout = [

    # top controls
    html.Div(
        [
            html.Div(
                dcc.Dropdown(
                    id="granularity_dropdown",
                    options=[
                        {"label": "Yesterday", "value": "day"},
                        {"label": "This week", "value": "week"},
                        {"label": "This month", "value": "month"},
                    ],
                    value="day",
                    clearable=False,
                ),
                className="two columns",
            ),
            html.Div(
                dcc.Dropdown(
                    id="metric_dropdown",
                    options=[
                        {"label": "Traffic", "value": "sessions"},
                        {"label": "Views", "value": "screen_views"},
                        {"label": "Users", "value": "users"},
                        {"label": "Transactions", "value": "transactions"},
                    ],
                    value="users",
                    clearable=False,
                ),
                className="two columns",
            ),

    # charts row div
    html.Div(
        [
            html.Div(
                [
                    #html.P("Metrics By Country" ),
                    dcc.Graph(
                        id="choropleth_map",
                        style={"height": "150%", "width": "200%"},
                        config=dict(displayModeBar=False),
                    ),
                ],
                className="four columns chart_div"
            ),
        ]
    )
        ]
    )
]
