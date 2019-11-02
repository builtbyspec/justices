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
        go.Table(header=dict(values=['Gender', 'Proportion of Modals Per Line'],line_color='black', fill_color='white', font_size=16, ),
                 cells=dict(values=[['Male', 'Female'], [0.017346, 0.017171]],line_color='black', fill_color='white', font_size=16, height=40)
                 )
    ], 
)

modal_bar =  go.Figure(
    data=[
        go.Bar(name='Sentences starting With Modal', x=["Female","Male"], y=[0.021971, 0.015526],
        hovertext=['Female judges hedge in 0.021971% of sentences', 'Male judges hedge in 0.015526% of sentences'],
        marker_color=['rgba(166, 139, 165, 1)','rgba(209, 153, 182, 1)' ]
        )
    ]
)
interruption_bar =  go.Figure(
    data=[
        go.Bar(
            name='Proportion of sentences that were interrupted', 
            x=["Female","Male"], y=[1789/26931, 1826/71857],
            marker_color=['rgba(166, 139, 165, 1)','rgba(209, 153, 182, 1)'],
            hovertext=['Female judges were interrupted in 0.06642902% of sentences', 'Male judges were interrupted in 0.02541158% of sentences'])
    ]
)
modal_table.update_layout( height=300)
# Change the bar mode
modal_bar.update_layout(barmode='stack', title=go.layout.Title(text='Sentences starting with a Modal'), paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')
interruption_bar.update_layout(barmode='stack', title=go.layout.Title(text='Proportion of sentences that were interrupted'),paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')


# APP COMPONENTS
# ==========
header = dbc.Jumbotron(
    [
        html.H1("Justices", className="display-2"),
        html.P(
            "An Analysis of Supreme Court Case Transcripts Since 2005"
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
    dbc.Container(
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
                    ],md=8,
                )
            ], justify="center"
        )
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

])

if __name__ == '__main__':
    app.run_server(debug=True)