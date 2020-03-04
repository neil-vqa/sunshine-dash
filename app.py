import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.graph_objects as do

app = dash.Dash(__name__)
app.title='Monthly Hours of Sunlight'
server = app.server

data = pd.read_csv('sunshine_latlon.csv')

map_token = 'pk.eyJ1IjoibmVpbHRoZWdyZWF0ZXN0IiwiYSI6ImNrM2ZqMmhvNjAzN2QzbW5uaHQyamo5NGkifQ.l53kgbZcDGY8U8xHkSWv0w'
map_style = 'mapbox://styles/neilthegreatest/ck7bg78ms00he1iqmu14kb00v'

content = dbc.Container([
	dbc.Row([
		dbc.Col([
			dbc.Row([
				dbc.Col([
					html.Div(html.Img(src=app.get_asset_url('sun.png')),className='mb-3')
				],width=4)],style={'height':'25%'}, align='end', justify='center'
			),
			dbc.Row([
				dbc.Col([
					html.H4(['How much sunshine are you getting?'], style={'text-align':'center'}),
					html.H6(['Average hours of sunlight in a given location.'], style={'text-align':'center'})
				])], justify='center'
			),
			dbc.Row([
				dbc.Col([
					dcc.Dropdown(
						id='continent-select',
						placeholder='Select a continent',
						clearable=False,
						options=[{'label':'Select a continent', 'value':'All'},
								{'label':'Africa', 'value':'Africa'},
								{'label':'Asia', 'value':'Asia'},
								{'label':'Europe', 'value':'Europe'},
								{'label':'North America', 'value':'North America'},
								{'label':'South America', 'value':'South America'},
								{'label':'Oceania', 'value':'Oceania'}],
						value='All'
					)
				],width=9)
			],justify='center',className='mt-3'),
			dbc.Row([
				dbc.Col([
					dcc.Dropdown(
						id='country-select',
						placeholder='Select a country',
						clearable=False
					)
				],width=9)
			],justify='center',className='mt-3'),
			dbc.Row([
				dbc.Col([
					dcc.Dropdown(
						id='city-select',
						placeholder='Select a city',
						clearable=False
					)
				],width=9)
			],justify='center',className='mt-3'),
			dbc.Row([
				dbc.Col(
					dbc.Button("Go!", id="analyze-button", color="success", size="lg"), width=3
				)
			],justify='center',className='mt-5'),
			dbc.Row([
				dbc.Col([
					html.Div("Data Source: Wikipedia | Viz by: nvqa", style={'fontSize':13, 'color':'#8eacd3'})
				])
			],className='mt-5 ml-1')
		],style={'backgroundColor':'#fcfeff','height':'100%'}, md=4),
		
		dbc.Col([
			dbc.Row([
				dcc.Graph(id="map", config={'displayModeBar': False},style={'width':'100%'})
			],style={'height':'65%'}),
			dbc.Row([
				dcc.Graph(id="bar-chart", config={'displayModeBar': False}, responsive=True, style={'width':'100%'})
			],style={'height':'35%'})
		],style={'backgroundColor':'#D4E8D5'}, md=8)
	],className='h-100')
],fluid=True, style={"height": "100vh"})


def serve_layout():
	return html.Div([content])
app.layout = serve_layout

@app.callback(
	Output('country-select','options'),
	[Input('continent-select','value')]
)
def country_options(continent_select):
	if (continent_select == 'All'):
		raw = list(data['Country'].unique())
		opts = [{'label':k, 'value':k} for k in raw]
		return opts
		
	if (continent_select == 'Africa'):
		raw = list(data.loc[data['Continent']=='Africa']['Country'].unique())
		opts = [{'label':k, 'value':k} for k in raw]
		return opts
	
	if (continent_select == 'Asia'):
		raw = list(data.loc[data['Continent']=='Asia']['Country'].unique())
		opts = [{'label':k, 'value':k} for k in raw]
		return opts
		
	if (continent_select == 'Europe'):
		raw = list(data.loc[data['Continent']=='Europe']['Country'].unique())
		opts = [{'label':k, 'value':k} for k in raw]
		return opts
	
	if (continent_select == 'North America'):
		raw = list(data.loc[data['Continent']=='North America']['Country'].unique())
		opts = [{'label':k, 'value':k} for k in raw]
		return opts
		
	if (continent_select == 'South America'):
		raw = list(data.loc[data['Continent']=='South America']['Country'].unique())
		opts = [{'label':k, 'value':k} for k in raw]
		return opts
	
	if (continent_select == 'Oceania'):
		raw = list(data.loc[data['Continent']=='Oceania']['Country'].unique())
		opts = [{'label':k, 'value':k} for k in raw]
		return opts

@app.callback(
	Output('city-select','options'),
	[Input('country-select','value')]
)
def city_options(country_select):
	raw = list(data.loc[data['Country']==country_select]['Title'].unique())
	opts = [{'label':k, 'value':k} for k in raw]
	
	return opts
	
@app.callback(
	[Output('map','figure'),
	Output('bar-chart','figure')],
	[Input('analyze-button','n_clicks')],
	[State('city-select','value')]
)
def update_charts(n_clicks, city_select):
	if n_clicks is None:
		df_lat = list(data['Lat'])
		df_lon = list(data['Lon'])
		df_city = list(data['Title'])
		midpoint = (np.average(data['Lat']), np.average(data['Lon']))
		
		plot1 = do.Figure()
		plot1.add_trace(
			do.Scattermapbox(
				lat=df_lat,
				lon=df_lon,
				mode='markers',
				marker=do.scattermapbox.Marker(
					size=10,
					color='#29EA8B',
					opacity=0.8
					),
				text= df_city,
				hoverinfo='text',
				showlegend= False
			)
		)
		plot1.update_layout(
			mapbox= do.layout.Mapbox(
				accesstoken= map_token,
				center= do.layout.mapbox.Center(
					lat= midpoint[0],
					lon= midpoint[1]
				),
				zoom= 1.8,
				style= map_style
			),
			margin= do.layout.Margin(
				l=0,
				r=0,
				t=0,
				b=0
			)
		)
		
		plot2 = do.Figure()
		plot2.update_layout(title={'text':'Monthly Average Hours of Sunlight: {}'.format(city_select),'xanchor': 'left','x':0.01},
						showlegend=False, plot_bgcolor='#E2EEF3',paper_bgcolor='#E2EEF3',
						yaxis={'showticklabels':False,'showgrid':False,'zeroline':False},
						xaxis={'showticklabels':False,'showgrid':False,'zeroline':False},
						margin={'t':45, 'b':0, 'l':0, 'r':0})

		return plot1,plot2
	
	else:
		loc_lat = data.loc[data['Title']==city_select]['Lat']
		loc_lon = data.loc[data['Title']==city_select]['Lon']
		loc_name = city_select

		plot1 = do.Figure()
		plot1.add_trace(
			do.Scattermapbox(
				lat=loc_lat,
				lon=loc_lon,
				mode='markers',
				marker=do.scattermapbox.Marker(
					size=20,
					color='#29EA8B',
					opacity=0.8
					),
				text= loc_name,
				hoverinfo='text',
				showlegend= False
			)
		)
		plot1.update_layout(
			mapbox= do.layout.Mapbox(
				accesstoken= map_token,
				center= do.layout.mapbox.Center(
					lat= loc_lat.values[0],
					lon= loc_lon.values[0]
				),
				zoom= 5,
				style= map_style
			),
			margin= do.layout.Margin(
				l=0,
				r=0,
				t=0,
				b=0
			)
		)
		
		df = data.loc[data['Title']==city_select]
		ind = df.index[0]
		x_val = df.columns[5:17]
		y_val = df.loc[ind,list(df[df.columns[5:17]])]
		
		plot2 = do.Figure()
		plot2.add_trace(
			do.Bar(
				x= x_val,
				y= y_val,
				marker={'color':'#ffffff'},
				text= y_val,
				textposition='auto',
				hoverinfo='none'
			)
		)
		plot2.update_layout(title={'text':'Monthly Average Hours of Sunlight: {}'.format(city_select),'xanchor': 'left','x':0.01},
						showlegend=False, plot_bgcolor='#E2EEF3',paper_bgcolor='#E2EEF3',
						yaxis={'showticklabels':False,'showgrid':False},
						margin={'t':45, 'b':0, 'l':0, 'r':0})
	
		return plot1,plot2
		
if __name__=='__main__':
    app.run_server(debug=True)
