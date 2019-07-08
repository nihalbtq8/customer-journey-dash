# -*- coding: utf-8 -*-
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from app import app, connect_gp
import basic_funnel
import choropleth

app.layout = html.Div(
    [
        # header
        html.Div([

            html.Div(
                html.Img(
                    src='https://www.boutiqaat.com/static/version1557987838/frontend/Emthemes/everything_beauty/en_US/images/logo.svg',
                    height="100%")
                , style={"float": "left", "height": "100%"})
        ],
            className="row header"
        ),

        # tabs
        html.Div([

            dcc.Tabs(
                id="tabs",
                style={"height": "20", "verticalAlign": "middle"},
                children=[
                    #dcc.Tab(label="Funnel", value="opportunities_tab"),
                    dcc.Tab(label="Choropleth", value="choropleth_tab"),
                    #dcc.Tab(id="cases_tab", label="Funnel", value="cases_tab"),
                ],
                value="choropleth_tab",
            )

        ],
            className="row tabs_div"
        ),

        # divs that save dataframe for each tab
        # Tab content
        html.Div(id="tab_content", className="row", style={"margin": "2% 3%"}),

        html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css", rel="stylesheet"),
        html.Link(
            href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",
            rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
        html.Link(
            href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css",
            rel="stylesheet")
    ],
    className="row",
    style={"margin": "0%"},
)


@app.callback(Output("tab_content", "children"), [Input("tabs", "value")])
def render_content(tab):
    if tab == "opportunities_tab":
        return choropleth.layout
    elif tab == "choropleth_tab":
        return choropleth.layout
    elif tab == "leads_tab":
        return choropleth.layout
    else:
        return choropleth.layout


if __name__ == "__main__":
    app.run_server(port=8050, host='0.0.0.0')