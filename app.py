import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import datetime



# LOAD DATA
# ==========
prose_df = prose_df = pd.read_json("data/prose.json").T
# justices = pd.read_csv("data/justices-dialogue.csv")
# DATA INTERACTION
# ==========
'''
Steps for data interaction:
    1. Choose type of graph object. (go.Scatter/go.Bar etc)
    2. Input x data, and y data and store into variable
    3. Group plots into an arrays for easy access
'''

modal_table= go.Figure(
    data=[
        go.Table(header=dict(values=['Gender', 'Proportion of Modals Per Line']),
                 cells=dict(values=[['Male', 'Female'], [95, 85, 75, 95]])
                 )
    ]
)

modal_bar =  go.Figure(
    data=[
        go.Bar(name='Sentences starting With Modal', x=["Female","Male"], y=[0.021971, 0.015526],)
    ]
)
interruption_bar =  go.Figure(
    data=[
        go.Bar(name='Sentences starting With Modal', x=["Female","Male"], y=[1789/26931, 1826/71857],)
    ]
)
# Change the bar mode
modal_bar.update_layout(barmode='stack', title=go.layout.Title(text='Sentences starting with a Modal'))
interruption_bar.update_layout(barmode='stack', title=go.layout.Title(text='Proportion of sentences that were interrupted'))


# example_scatter2 = go.Scatter(x=random_x, y=random_y1,
#                     mode='lines+markers',
#                     name='lines+markers',
#                     line = dict(color = '#3F94AB'),
#                     opacity = 0.8)

# example_scatter3 = go.Scatter(x=random_x, y=random_y2,
#                     mode='lines', 
#                     name='lines',
#                     line = dict(color = '#6285B2'),
#                     opacity = 0.8)


# examplelayout = go.Layout(
#     hovermode = "x",
#     title = "Example Title",
#     xaxis = dict(
#         range = [0,1]
#     ),
#     yaxis = dict(
#         autorange = True
#     )
# )

# examples = [example_scatter1, example_scatter2, example_scatter3]

# APP COMPONENTS
# ==========
header = dbc.Jumbotron(
    [
        html.H1("justices", className="display-3"),
        html.P(
            "Analysis of Supreme Court Case Transcripts Since 2005"
        )
    ],
    className = 'my-div text-center',
)
tab1_content = (
    [
        html.H2(prose_df.loc["modal_use", "title"]),
        html.P(prose_df.loc["modal_use", "prose_1"]),
        dcc.Graph(figure=modal_table),
        html.P([
            prose_df.loc["modal_use", "prose_2a"],
            html.Em(prose_df.loc["modal_use", "prose_2_em"]), 
            prose_df.loc["modal_use", "prose_2_b"]
            ]
        ),
        html.P([
            "\"",
            html.Strong(prose_df.loc["modal_use", "example_1_strong"]),
            prose_df.loc["modal_use", "example_1_b"],
            html.P(prose_df.loc["modal_use", "example_1_c"]),
            prose_df.loc["modal_use", "example_2_a"],
            html.Strong(prose_df.loc["modal_use", "example_2_strong"]),
            prose_df.loc["modal_use", "example_2_b"],
        ]),
        html.P(prose_df.loc["modal_use", "prose_3"]),
        dcc.Graph(figure=modal_bar),
        html.P(prose_df.loc["modal_use", "prose_4"]),

    ]
)
tab2_content = (
    html.H2(prose_df.loc["interruption", "title"]),
    html.P(prose_df.loc["interruption", "prose_1"]),
    html.P(prose_df.loc["interruption", "prose_2"]),
    dcc.Graph(figure=interruption_bar),
    html.P(prose_df.loc["interruption","prose_3"])
)
tab3_content = (
    html.H2("tab3stuff")
)


tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Do female justices use hedging more than male justices?"),
        dbc.Tab(tab2_content, label="Do female or male justices get interrupted more often?"),
        dbc.Tab(tab3_content, label="Does age play a role in the interuption rate of justices?"),
    ]
)

body = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H2(prose_df.loc["intro", "title"]),
                    html.P(prose_df.loc["intro", "prose_1"]),
                    html.P(prose_df.loc["intro", "prose_2"]),
                    html.Div(
                            [html.P(prose_df.loc["intro", "closing_prose"])],
                            className="sidenote-text"
                        ),
                    tabs,
                ],md=12
            )
        ]
    )
)


# examplefig = go.Figure(data=examples, layout=examplelayout)

# APP LAYOUT
# ==========

app = dash.Dash(__name__, external_scripts=['https://raw.githubusercontent.com/robin-dela/hover-effect/master/example/js/three.min.js','https://raw.githubusercontent.com/robin-dela/hover-effect/master/example/js/TweenMax.min.js','https://raw.githubusercontent.com/robin-dela/hover-effect/master/dist/hover-effect.umd.js'], external_stylesheets=[dbc.themes.BOOTSTRAP
])

server = app.server

app.layout = html.Div(children=[
        header,
        body,

        # dcc.Graph(
        #     figure = examplefig
        # ),
        # html.P(prose_df.loc["data explanation", "prose_1"]),
        # html.P(prose_df.loc["data explanation", "prose_2"]),
        # html.P(prose_df.loc["data explanation", "prose_3"]),

])

if __name__ == '__main__':
    app.run_server(debug=True)