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

df_system = pd.read_csv('data/hospital-numbers/latest_data.csv')
df_system['Date'] = pd.to_datetime(df_system['Date'], dayfirst=True)

##### PLOTS #####

# COLORS
IMPORTED = 'rgb(0, 95, 255)'
LOCAL_LINKED = 'rgb(255, 127, 14)'
LOCAL_UNLINKED = 'rgb(214, 39, 40)'

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
    delta = {'reference': (1910 - 460), 'increasing.color':'red'},
    mode = "number+delta",
    title = {'text': 'Active Cases'},
    domain = {'row':0, 'column':1}
))

gauge.add_trace(go.Indicator(
    value = 492,
    delta = {'reference': 460, 'increasing.color':'green'},
    mode = "number+delta",
    title = {'text': 'Recovered'},
    domain = {'row':0, 'column':2}
))

gauge.add_trace(go.Indicator(
    value = 7,
    delta = {'reference': 6, 'increasing.color':'red'},
    mode = "number+delta",
    title = {'text': 'Deaths'},
    domain = {'row':0, 'column':3}
))

gauge.add_trace(go.Indicator(
    value = 32,
    delta = {'reference': 29, 'increasing.color':'red'},
    mode = "number+delta",
    title = {'text': 'ICU'},
    domain = {'row':0, 'column':4}
))

gauge.add_trace(go.Indicator(
    value = 843,
    delta = {
        'reference': 855, 
        'increasing.color':'red', 
        'decreasing.color':'green', 
        'relative':False},
    mode = "number+delta",
    title = {'text': 'Warded'},
    domain = {'row':0, 'column':5}
))

gauge.add_trace(go.Indicator(
    value = 734,
    delta = {'reference': 559, 'increasing.color':'red'},
    mode = "number+delta",
    title = {'text': 'In Isolation'},
    domain = {'row':0, 'column':6}
))

gauge.update_layout(
    grid = {'rows':1, 'columns':7, 'pattern':'independent'},

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
        x=df_epidemic['Date'][df_epidemic.Type == 'Local Unlinked'],
        y=df_epidemic['Value'][df_epidemic.Type == 'Local Unlinked'],
        name='Local Unlinked',
        marker_color = LOCAL_UNLINKED,
        text=df_epidemic['Value'][df_epidemic.Type == 'Local Unlinked'],
        textposition='auto'
    )
) 
fig_epidemic.add_trace(
    go.Bar(
        x=df_epidemic['Date'][df_epidemic.Type == 'Local Linked'],
        y=df_epidemic['Value'][df_epidemic.Type == 'Local Linked'],
        name='Local Linked',
        marker_color = LOCAL_LINKED,
        text=df_epidemic['Value'][df_epidemic.Type == 'Local Linked'],
        textposition='auto'
    )
)
fig_epidemic.add_trace(
    go.Bar(
        x=df_epidemic['Date'][df_epidemic.Type == 'Imported'],
        y=df_epidemic['Value'][df_epidemic.Type == 'Imported'],
        name='Imported',
        marker_color = IMPORTED,
        text=df_epidemic['Value'][df_epidemic.Type == 'Imported'],
        textposition='auto'
    )
)  
fig_epidemic.update_layout(
    title='Total Cases',
    template='plotly_white',
    barmode='stack'
    )

# Plot4: New cases
fig_newcases = go.Figure()
fig_newcases.add_trace(
    go.Bar(
        x=df_newcases['Date'][df_epidemic.Type == 'Local Unlinked'],
        y=df_newcases['Value'][df_epidemic.Type == 'Local Unlinked'],
        name='Local Unlinked',
        marker_color = LOCAL_UNLINKED,
        text=df_newcases['Value'][df_epidemic.Type == 'Local Unlinked'],
        textposition='auto'
    )
) 
fig_newcases.add_trace(
    go.Bar(
        x=df_newcases['Date'][df_epidemic.Type == 'Local Linked'],
        y=df_newcases['Value'][df_epidemic.Type == 'Local Linked'],
        name='Local Linked',
        marker_color = LOCAL_LINKED,
        text=df_newcases['Value'][df_epidemic.Type == 'Local Linked'],
        textposition='auto'
    )
)
fig_newcases.add_trace(
    go.Bar(
        x=df_newcases['Date'][df_epidemic.Type == 'Imported'],
        y=df_newcases['Value'][df_epidemic.Type == 'Imported'],
        name='Imported',
        marker_color = IMPORTED,
        text=df_newcases['Value'][df_epidemic.Type == 'Imported'],
        textposition='auto'
    )
)  
fig_newcases.update_layout(
    title='New Cases',
    template='plotly_white',
    barmode='stack'
    )

# Plot5: Average number of days from onset
fig_daysonset = go.Figure()
fig_daysonset.add_trace(
    go.Bar(
        x=df_daysonset['Date'][df_daysonset.Type == 'Daily Average'],
        y=df_daysonset['Value'][df_daysonset.Type == 'Daily Average'],
        name='Daily Average',
        marker_color = 'rgba(0, 0, 153, 0.25)', #alpha is the last value
    )
)
fig_daysonset.add_trace(
    go.Scatter(
        x=df_daysonset['Date'][df_daysonset.Type == 'Moving Average (14-day)'],
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

# Plot6: In system vs Discharged
fig_system = go.Figure()
fig_system.add_trace(
    go.Bar(
        x=df_system['Date'][df_system.Type == 'ICU'],
        y=df_system['Value'][df_system.Type == 'ICU'],
        name='ICU',
        marker_color = LOCAL_UNLINKED,
        text=df_system['Value'][df_system.Type == 'ICU'],
        textposition='auto'
    )
)
fig_system.add_trace(
    go.Bar(
        x=df_system['Date'][df_system.Type == 'General Ward'],
        y=df_system['Value'][df_system.Type == 'General Ward'],
        name='General Ward',
        marker_color=LOCAL_LINKED,
        text=df_system['Value'][df_system.Type == 'General Ward'],
        textposition='auto'
    )
)
fig_system.add_trace(
    go.Bar(
        x=df_system['Date'][df_system.Type == 'In Isolation'],
        y=df_system['Value'][df_system.Type == 'In Isolation'],
        name='In Isolation',
        marker_color='rgb(242,200,15)',
        text=df_system['Value'][df_system.Type == 'In Isolation'],
        textposition='auto'
    )
)
# fig_system.add_trace(
#     go.Scatter(
#         x=df_system[(df_system.Type == 'Discharged') | (df_system.Type == 'Completed Isolation')].groupby('Date')['Value'].sum(),
#         y=df_system['Date'][(df_system.Type == 'Discharged') | (df_system.Type == 'Completed Isolation')],
#         name='Discharged',
#         marker_color="rgb(44, 160, 44)",
#         mode='lines+markers'
#     )
# )
fig_system.update_layout(
    title='Number of Cases in Hospitals and Community Isolation Facilities',
    template='plotly_white',
    barmode='stack'
    )

fig_outofsystem=go.Figure()
fig_outofsystem.add_trace(
    go.Bar(
        y=df_system['Value'][df_system.Type == 'Discharged'],
        x=df_system['Date'][df_system.Type == 'Discharged'],
        name='Discharged',
        marker_color="rgb(44, 160, 44)",
        text=df_system['Value'][df_system.Type == 'Discharged'],
        textposition='auto'
    )
)
fig_outofsystem.add_trace(
    go.Bar(
        y=df_system['Value'][df_system.Type == 'Demised'],
        x=df_system['Date'][df_system.Type == 'Demised'],
        name='Demised',
        marker_color="Black",
        text=df_system['Value'][df_system.Type == 'Demised'],
        textposition='auto'
    )
)

fig_outofsystem.update_layout(
    title="Out of system",
    template='plotly_white',
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

    #dcc.Graph(
    #    id='Confirmed, Recovered and Deaths',
    #    figure=fig_subplots
    #),

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
    ),

    dcc.Graph(
        id='Cases in Healthcare System',
        figure=fig_system
    ),

    dcc.Graph(
        id='Cases out of Healthcare System',
        figure=fig_outofsystem
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)