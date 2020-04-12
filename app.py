import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# data loads
df = pd.read_csv('data/enigma-jhu/latest_data.csv')
df['datetime'] = pd.to_datetime(df['last_update'])

df_epidemic = pd.read_csv('data/total-cases-cumulative/latest_data.csv')
df_epidemic['Date'] = pd.to_datetime(df_epidemic['Date'], dayfirst=True)

df_newcases = pd.read_csv('data/total-cases-new/latest_data.csv')
df_newcases['Date'] = pd.to_datetime(df_newcases['Date'], dayfirst=True)

df_daysonset = pd.read_csv('data/symptoms-onset-to-isolation/latest_data.csv')
df_daysonset['Date'] = pd.to_datetime(df_daysonset['Date'], dayfirst=True)

##### PLOTS #####

# Gauge subplot
gauge = go.Figure()

gauge.add_trace(go.Indicator(
    value = 2108, # note: hardcoded for now
    delta = {'reference': 1910, 'increasing.color':'red'},
    mode = "number+delta",
    title = {'text': 'Total Cases'},
    domain = {'row':0, 'column':0}
))

gauge.add_trace(go.Indicator(
    value = 2108 - 492, # note: hardcoded for now
    delta = {'reference': (1910 - 460), 'increasing.color':'orange'},
    mode = "number+delta",
    title = {'text': 'Active Cases'},
    domain = {'row':0, 'column':1}
))

gauge.add_trace(go.Indicator(
    value = 492,
    delta = {'reference': 460, 'increasing.color':'blue'},
    mode = "number+delta",
    title = {'text': 'Recovered'},
    domain = {'row':0, 'column':2}
))

gauge.add_trace(go.Indicator(
    value = 7,
    delta = {'reference': 6, 'increasing.color':'black'},
    mode = "number+delta",
    title = {'text': 'Deaths'},
    domain = {'row':0, 'column':3}
))

gauge.update_layout(
    grid = {'rows':1, 'columns':4, 'pattern':'independent'},

)

# Confirmed vs Recovered / Deaths vs Recovered Subplot
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
            },
        showlegend=False # because this is reported in the next graph
        ),
        row=1,
        col=1,
        
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

# Plot3: Epidemic Curve of COVID-19 Outbreak
fig_epidemic = go.Figure()
fig_epidemic.add_trace(
    go.Bar(
        x=df_epidemic['Date'],
        y=df_epidemic['Value'][df_epidemic.Type == 'Local Unlinked'],
        name='Local Unlinked',
        marker_color = 'indianred'
    )
) 
fig_epidemic.add_trace(
    go.Bar(
        x=df_epidemic['Date'],
        y=df_epidemic['Value'][df_epidemic.Type == 'Local Linked'],
        name='Local Linked',
        marker_color = 'lightsalmon'
    )
) 
fig_epidemic.update_layout(
    title='Epidemic Curve',
    template='plotly_white'
    )

# Plot4: New cases
fig_newcases = go.Figure()
fig_newcases.add_trace(
    go.Bar(
        x=df_newcases['Date'],
        y=df_newcases['Value'][df_epidemic.Type == 'Local Unlinked'],
        name='Local Unlinked',
        marker_color = 'indianred'
    )
) 
fig_newcases.add_trace(
    go.Bar(
        x=df_newcases['Date'],
        y=df_newcases['Value'][df_epidemic.Type == 'Local Linked'],
        name='Local Linked',
        marker_color = 'lightsalmon'
    )
) 
fig_newcases.update_layout(
    title='New Cases',
    template='plotly_white'
    )

# Plot5: Average number of days from onset
fig_daysonset = go.Figure()
fig_daysonset.add_trace(
    go.Bar(
        x=df_daysonset['Date'],
        y=df_daysonset['Value'][df_daysonset.Type == 'Daily Average'],
        name='Daily Average',
        marker_color = 'rgba(154, 154, 154, 0.4)', #alpha is the last value
    )
)
fig_daysonset.add_trace(
    go.Scatter(
        x=df_daysonset['Date'],
        y=df_daysonset['Value'][df_daysonset.Type == 'Moving Average (14-day)'],
        name='Moving Average (14-day)',
        marker_color="rgb(0, 0, 153)",
        mode='lines+markers'
    )
)
fig_daysonset.update_layout(
    title='Average Number of Days from Onset of Symptoms to Isolation for Local Unlinked Cases In Each Day (by Press Release Date)',
    template='plotly_white'
    )

app.layout = html.Div(children=[
    html.H1(children='Ministry of Health COVID-19 Dashboard'),

    html.Div(
        children='by DSAID COVID-19 Data Team',
        style={'font-style':'italic'}
    ),

    dcc.Graph(
        id='Gauge',
        figure=gauge
    ),

    dcc.Graph(
        id='Confirmed, Recovered and Deaths',
        figure=fig_subplots
    ),

    dcc.Graph(
        id='Epidemic Curve',
        figure=fig_epidemic
    ),

    dcc.Graph(
        id='New Cases',
        figure=fig_newcases
    ),

    dcc.Graph(
        id='Moving Averages',
        figure=fig_daysonset
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)