import math

import pandas as pd
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import dateutil.parser
from sqlalchemy import create_engine
from config import GP_USER, GP_PWD, GP_HOST, GP_PORT
from config import GA_USER, GA_PWD, GA_HOST



server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
app.config.suppress_callback_exceptions = True


millnames = ["", " K", " M", " B", " T"]  # used to convert numbers


# return html Table with dataframe values
def df_to_table(df):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df.columns])] +

        # Body
        [
            html.Tr(
                [
                    html.Td(df.iloc[i][col])
                    for col in df.columns
                ]
            )
            for i in range(len(df))
        ]
    )


# returns most significant part of a number
def millify(n):
    n = float(n)
    millidx = max(
        0,
        min(
            len(millnames) - 1, int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))
        ),
    )

    return "{:.0f}{}".format(n / 10 ** (3 * millidx), millnames[millidx])


# returns top indicator div
def indicator(color, text, id_value):
    return html.Div(
        [

            html.P(
                text,
                className="twelve columns indicator_text"
            ),
            html.P(
                id=id_value,
                className="indicator_value"
            ),
        ],
        className="four columns indicator",

    )

def connect_gp():
    uri_gp = 'postgresql+psycopg2://' + GP_USER  + ':' + GP_PWD + '@' + GP_HOST + ':' + GP_PORT
    engine_gp = create_engine(uri)
    return engine_gp.connect()

def connect_ga():
    uri_ga = 'mysql://' + GA_USER + ':' + GA_PWD + '@' + GA_HOST + '/ga?charset=utf8'
    engine_ga = create_engine(uri_ga, encoding="utf8", pool_recycle=3600)
    return engine_ga.connect()