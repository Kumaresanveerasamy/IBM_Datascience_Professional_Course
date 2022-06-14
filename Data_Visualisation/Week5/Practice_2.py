import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update

app = dash.Dash(__name__)

# REVIEW1: Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# Add Dataframe
auto_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/Data%20files/automobileEDA.csv',
                            encoding = "ISO-8859-1")


#Layout Section of Dash

app.layout = html.Div(children=[ html.H1("Explore prices of Wheel drives for different Body style",style={'textAlign':'center','font-size':24,'color':'#503D36'}),

                                 html.Div([
                                     html.Div(html.H2('Drive Wheels Type:', style={'margin-right': '2em'})),

                                     dcc.Dropdown( id = 'demo-dropdown',options = [{'label': 'Rear Wheel Drive', 'value': 'rwd'},
                                                                                   {'label': 'Front Wheel Drive', 'value': 'fwd'},
                                                                                   {'label': 'Four Wheel Drive', 'value': '4wd'}],value='rwd')]),
                                 html.Div([html.Div([],id = 'plot1'),
                                           html.Div([],id = 'plot2')], style={'display': 'flex'})

                                 ])


#@app.callback Decorator
@app.callback(Output(component_id='plot1',component_property='children'),
              Output(component_id='plot2',component_property='children'),
              Input(component_id='demo-dropdown',component_property='value'))



#callback function:
def display_selected_drive_charts(value):
    filtered_df = auto_data[auto_data['drive-wheels'] == value].groupby(['drive-wheels', 'body-style'],as_index=False).mean()

    filtered_df = filtered_df
    print(filtered_df.head())
    fig1 = px.pie(filtered_df, values='price', names='body-style', title="Pie Chart")
    fig2 = px.bar(filtered_df, x='body-style', y='price', title='Bar Chart')

    return [dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)]




if __name__ == '__main__':
    app.run_server(debug =True)

