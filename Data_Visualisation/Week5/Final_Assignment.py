import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

# Airline Dataframe:
airline_data = pd.read_csv('airline_data.csv',
                           encoding="ISO-8859-1",
                           dtype={'Div1Airport': str, 'Div1TailNum': str,
                                  'Div2Airport': str, 'Div2TailNum': str})

year_list = [i for i in range(2005, 2021, 1)]

# Dash and Layout:
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

app.layout = html.Div(children=[
    html.H1("US Domestic Airline Flights Performance", style={
        'textAlign': 'center', 'color': 'Blue', 'font-size': 35
    }),

    html.Div([
        html.Div(html.H2("Report Type :", style={'margin-right': '2em', 'font-size': 25})),

        dcc.Dropdown(id='report_type', options=[{'label': 'Yearly Airline Performance Report', 'value': 'performance'},
                                                {'label': 'Yearly Airline Delay Report', 'value': 'delay'}],
                     value='performance',
                     style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'})
    ], style={'display': 'flex'}),

    html.Div([
        html.Div(html.H2("Choose Year : ", style={'margin-right': '2em', 'font-size': 25})),

        dcc.Dropdown(id='input_year',
                     options=[{'label': i, 'value': i} for i in year_list],
                     placeholder="Select a year",
                     style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'})],
        style={'display': 'flex'}),


    html.Div([], id='figure1', style={'width': '75%'}),

    html.Div([html.Div([], id='figure2'), html.Div([], id='figure3')], style={'display': 'flex'}),

    html.Div([html.Div([], id='figure4'), html.Div([], id='figure5')], style={'display': 'flex'}),

])


# computing Delay Function:

def compute_delay_info(df):
    avg_car = df.groupby(['Month', 'Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    avg_weather = df.groupby(['Month', 'Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    avg_NAS = df.groupby(['Month', 'Reporting_Airline'])['NASDelay'].mean().reset_index()
    avg_sec = df.groupby(['Month', 'Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    avg_late = df.groupby(['Month', 'Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()

    return avg_car, avg_weather, avg_NAS, avg_sec, avg_late


# computing Performance Function:

def compute_performance_info(df):
    # Cancellation Category Count
    bar_data = df.groupby(['Month', 'CancellationCode'])['Flights'].sum().reset_index()
    # Average flight time by reporting airline
    line_data = df.groupby(['Month', 'Reporting_Airline'])['AirTime'].mean().reset_index()
    # Diverted Airport Landings
    div_data = df[df['DivAirportLandings'] != 0.0]
    # Source state count
    map_data = df.groupby(['OriginState'])['Flights'].sum().reset_index()
    # Destination state count
    tree_data = df.groupby(['DestState', 'Reporting_Airline'])['Flights'].sum().reset_index()

    return bar_data, line_data, div_data, map_data, tree_data


# Callback Function:
@app.callback([Output(component_id='figure1', component_property='children'),
               Output(component_id='figure2', component_property='children'),
               Output(component_id='figure3', component_property='children'),
               Output(component_id='figure4', component_property='children'),
               Output(component_id='figure5', component_property='children')],
              [Input(component_id='report_type', component_property='value'),
               Input(component_id='input_year', component_property='value')]
              )
def get_graph(chart, year):
    df = airline_data[airline_data['Year'] == int(year)]

    if chart == 'performance':
        bar_data, line_data, div_data, map_data, tree_data = compute_performance_info(df)

        # Number of flights under different cancellation categories

        bar_fig = px.bar(bar_data, x='Month', y='Flights', color='CancellationCode',
                         title='Monthly Flight Cancellation')

        # Average flight time by reporting airline

        line_fig = px.line(line_data, x='Reporting_Airline', y='AirTime', color='Reporting_Airline',
                           title='Monthly Airtime by Airline')

        # Percentage of diverted airport landings per reporting airline

        pie_fig = px.pie(div_data, values='Flights', names='Reporting_Airline',
                         title='% of flights by reporting airline')

        # REVIEW5: Number of flights flying from each state using choropleth
        map_fig = px.choropleth(map_data, locations='OriginState', color='Flights',
                                hover_data=['OriginState', 'Flights'],
                                locationmode='USA-states', color_continuous_scale='GnBu',
                                range_color=[0, map_data['Flights'].max()])
        map_fig.update_layout(title_text='Number of flights from origin state',
                              geo_scope='usa')

        # Number of flights flying to each state from each reporting airline
        tree_fig = px.treemap(tree_data, path=['DestState', 'Reporting_Airline'], values='Flights'
                              , color='Flights', color_continuous_scale='RdBu',
                              title=' Flights to Different states by Airline')
        return [dcc.Graph(figure=tree_fig),
                dcc.Graph(figure=pie_fig),
                dcc.Graph(figure=map_fig),
                dcc.Graph(figure=bar_fig),
                dcc.Graph(figure=line_fig)]

    else:

        avg_car, avg_weather, avg_NAS, avg_sec, avg_late = compute_delay_info(df)

        carrier_fig = px.line(avg_car, x='Month', y='CarrierDelay', color='Reporting_Airline',
                              title='Average carrier delay time (minutes) by airline')
        weather_fig = px.line(avg_weather, x='Month', y='WeatherDelay', color='Reporting_Airline',
                              title='Average weather delay time (minutes) by airline')
        nas_fig = px.line(avg_NAS, x='Month', y='NASDelay', color='Reporting_Airline',
                          title='Average NAS delay time (minutes) by airline')
        security_fig = px.line(avg_sec, x='Month', y='SecurityDelay', color='Reporting_Airline',
                               title='Average security delay time (minutes) by airline')
        late_fig = px.line(avg_late, x='Month', y='LateAircraftDelay', color='Reporting_Airline',
                           title='Average aircraft late delay time (minutes) by airline')

        return [dcc.Graph(figure=carrier_fig),
                dcc.Graph(figure=weather_fig),
                dcc.Graph(figure=nas_fig),
                dcc.Graph(figure=security_fig),
                dcc.Graph(figure=late_fig)]


if __name__ == '__main__':
    app.run_server()
