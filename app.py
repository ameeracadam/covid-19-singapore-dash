import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# pandas for data load
df = pd.read_csv('data/enigma-jhu/apr-10-data.csv')
df['datetime'] = pd.to_datetime(df['last_update'])

app.layout = html.Div(children=[
    html.H1(children='Ministry of Health COVID-19 Dashboard'),

    html.Div(children='''
        Situation Report in Singapore
    '''),

    dcc.Graph(
        id='Confirmed vs Recovered',
        figure={
            'data': [
                {
                    'x': df['datetime'], 
                    'y': df['confirmed'], 
                    'type': 'line', 
                    'name': 'Confirmed', 
                    'mode':'lines+markers', 
                    'line':{
                        'color':'royalblue'
                        }
                    },
                {
                    'x': df['datetime'], 
                    'y': df['recovered'], 
                    'type': 'line', 
                    'name': 'Recovered', 
                    'mode':'lines+markers',
                    'line':{
                        'color':'pink'
                    }
                    },
            ],
            'layout': {
                'title': 'Confirmed vs Recovered'
            }
        }
    ),

    dcc.Graph(
        id='Recovered vs Deaths',
        figure={
            'data': [
                {
                    'x': df['datetime'], 
                    'y': df['deaths'], 
                    'type': 'line', 
                    'name': 'Deaths', 
                    'mode':'lines+markers', 
                    'line':{
                        'color':'black'
                        }
                    },
                {
                    'x': df['datetime'], 
                    'y': df['recovered'], 
                    'type': 'line', 
                    'name': 'Recovered', 
                    'mode':'lines+markers',
                    'line':{
                        'color':'pink'
                    }},
            ],
            'layout': {
                'title': 'Deaths vs Recovered'
            }
        }
    ),


    
])

if __name__ == '__main__':
    app.run_server(debug=True)