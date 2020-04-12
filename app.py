import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# pandas for data load
df = pd.read_csv('data/enigma-jhu/apr-10-data.csv')
df['datetime'] = pd.to_datetime(df['last_update'])

# plots
fig_subplots = make_subplots(
    rows=1, 
    cols=2,
    subplot_titles = ("Confirmed vs Recovered", "Deaths vs Recovered")
)

# Plot 1 - Confirmed vs Recovered
fig_subplots.append_trace(
    go.Scatter(
        x=df['datetime'],
        y=df['confirmed'],
        mode='lines+markers',
        name="Confirmed",
        line={
            'color':'firebrick'
            }
        ),
        row = 1,
        col = 1
)
fig_subplots.append_trace(
    go.Scatter(
        x=df['datetime'],
        y=df['recovered'],
        mode='lines+markers',
        name="Recovered",
        line={
            'color':'royalblue'
            }
        ),
        row=1,
        col=1
)

# Plot 2 - Deaths vs Recovered
fig_subplots.append_trace(
    go.Scatter(
        x=df['datetime'],
        y=df['deaths'],
        mode='lines+markers',
        name="Deaths",
        line={
            'color':'black'
            }
        ),
        row = 1,
        col = 2
)
fig_subplots.append_trace(
    go.Scatter(
        x=df['datetime'],
        y=df['recovered'],
        mode='lines+markers',
        name="Recovered",
        line={
            'color':'royalblue'
            }
        ),
        row = 1,
        col = 2
)

# set theming options
fig_subplots.update_layout(template="plotly_white")

app.layout = html.Div(children=[
    html.H1(children='Ministry of Health COVID-19 Dashboard'),

    html.Div(
        children='by DSAID COVID-19 Data Team',
        style={'font-style':'italic'}
    ),

    dcc.Graph(
        id='Confirmed, Recovered and Deaths',
        figure=fig_subplots
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)