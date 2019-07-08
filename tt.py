# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from app import app, indicator, millify, df_to_table


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


layout = [
    html.Div(
        [
            html.Div(
                dcc.Dropdown(
                    id="country_dropdown",
                    options=[
                        {"label": "Oman", "value": "OM"},
                        {"label": "Saudi", "value": "SA"},
                        {"label": "UAE", "value": "AE"},
                        {"label": "Bahrain", "value": "BH"},
                        {"label": "Kuwait", "value": "KW"},
                        {"label": "Qatar", "value": "QA"},
                    ],
                    value="all",
                    clearable=True,
                ),
                className="two columns",
            ),

            html.Div(
                [
            dcc.Graph(
                id="funnel",
                config=dict(displayModeBar=False),
            ),
        ],
        className="two columns"),

        ]),
]




def funnel_chart(country):
    values_vs_country = {
        "OM": [2496, 2070, 673, 452, 122],
        "SA": [13873, 10553, 5443, 3703, 1708],
        "AE": [2496, 2070, 673, 452, 122],
        "BH": [9456, 7853, 3011, 1096, 899],
        "KW": [13873, 10553, 5443, 3703, 1708],
        "QA": [9456, 7853, 3011, 1096, 899],
        "all": [29000, 25487, 18777, 10929, 8989]
    }

    values = values_vs_country[country] if country in values_vs_country.keys() else values_vs_country["all"]
    phases = ['Visit', 'Sign-up', 'Selection', 'Purchase', 'Review']
    colors = ['rgb(32,155,160)', 'rgb(253,93,124)', 'rgb(28,119,139)', 'rgb(182,231,235)', 'rgb(35,154,160)']

    n_phase = len(phases)
    plot_width = 400
    section_h = 100
    section_d = 10
    unit_width = plot_width / max(values)
    phase_w = [int(value * unit_width) for value in values]
    height = section_h * n_phase + section_d * (n_phase - 1)
    shapes = []
    label_y = []

    for i in range(n_phase):
        if (i == n_phase - 1):
            points = [phase_w[i] / 2, height, phase_w[i] / 2, height - section_h]
        else:
            points = [phase_w[i] / 2, height, phase_w[i + 1] / 2, height - section_h]

        path = 'M {0} {1} L {2} {3} L -{2} {3} L -{0} {1} Z'.format(*points)

        shape = {
            'type': 'path',
            'path': path,
            'fillcolor': colors[i],
            'line': {
                'width': 1,
                'color': colors[i]
            }
        }
        shapes.append(shape)

        # Y-axis location for this section's details (text)
        label_y.append(height - (section_h / 2))

        height = height - (section_h + section_d)

    # For phase names
    label_trace = go.Scatter(
        x=[-350] * n_phase,
        y=label_y,
        mode='text',
        text=phases,
        textfont=dict(
            color='rgb(200,200,200)',
            size=15
        )
    )

    # For phase values
    value_trace = go.Scatter(
        x=[350] * n_phase,
        y=label_y,
        mode='text',
        text=values,
        textfont=dict(
            color='rgb(200,200,200)',
            size=15
        )
    )

    data = [label_trace, value_trace]

    layout = go.Layout(
        title="<b>Funnel by Country</b>",
        titlefont=dict(
            size=20,
            color='rgb(203,203,203)'
        ),
        shapes=shapes,
        height=560,
        width=800,
        showlegend=False,
        paper_bgcolor='rgba(44,58,71,1)',
        plot_bgcolor='rgba(44,58,71,1)',
        xaxis=dict(
            showticklabels=False,
            zeroline=False,
        ),
        yaxis=dict(
            showticklabels=False,
            zeroline=False
        )
    )
    return dict(data=data, layout=layout)

# update heat map figure based on dropdown's value and df updates
@app.callback(
    Output("funnel", "figure"),
    [Input("country_dropdown", "value")],
)
def map_callback(country):
    return funnel_chart(country)

