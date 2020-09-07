import pandas as pd
import plotly.express as px

import dash 
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output



""" initialize application """
app = dash.Dash(__name__)



"""" import, read, and restructure the data for choropleth map """
df = pd.read_csv("military_expenditure.csv")
df = df.groupby(["Country Name"])[[str(val) for val in range (1960, 2019)]].mean()
df.reset_index(inplace=True)

"""   restructure data by region for line graph """
na = ["United States", "Mexico", "Canada"]
na_df = df.loc[df["Country Name"].isin(na)]
reshaped_na = pd.melt(na_df, id_vars=["Country Name"], var_name="Year")
reshaped_na = reshaped_na.pivot(index='Year', columns='Country Name', values='value')

w_eu = ["France", "Germany", "United Kingdom", "Italy", "Spain"]
w_eu_df = df.loc[df["Country Name"].isin(w_eu)]
reshaped_weu = pd.melt(w_eu_df, id_vars=["Country Name"], var_name="Year")
reshaped_weu = reshaped_weu.pivot(index='Year', columns='Country Name', values='value')

e_eu = ["Russian Federation", "Czech Republic", "Slovokia", "Poland", "Serbia", "Romania", "Hungary"]
e_eu_df = df.loc[df["Country Name"].isin(e_eu)]
reshaped_eeu = pd.melt(e_eu_df, id_vars=["Country Name"], var_name="Year")
reshaped_eeu = reshaped_eeu.pivot(index='Year', columns='Country Name', values='value')

sa = ["Brazil", "Peru", "Columbia", "Argentina", "Ecuador"]
sa_df = df.loc[df["Country Name"].isin(sa)]
reshaped_sa = pd.melt(sa_df, id_vars=["Country Name"], var_name="Year")
reshaped_sa = reshaped_sa.pivot(index='Year', columns='Country Name', values='value')

wa = ["Afghanistan", "Iran, Islamic Rep.", "Iraq", "Israel", "Syrian Arab Republic", "United Arab Emirates", "Turkey", "Saudi Arabia"]
wa_df = df.loc[df["Country Name"].isin(wa)]
reshaped_wa = pd.melt(wa_df, id_vars=["Country Name"], var_name="Year")
reshaped_wa = reshaped_wa.pivot(index='Year', columns='Country Name', values='value')

ea = ["China", "Japan", "Korea, Rep", "India", "Vietnam", "Philippines"]
ea_df = df.loc[df["Country Name"].isin(ea)]
reshaped_ea = pd.melt(ea_df, id_vars=["Country Name"], var_name="Year")
reshaped_ea = reshaped_ea.pivot(index='Year', columns='Country Name', values='value')

af = ["Egypt, Arab Rep.", "Algeria", "Nigera", "Congo, Rep.", "Chad", "Kenya", "Morocco"]
af_df = df.loc[df["Country Name"].isin(af)]
reshaped_af = pd.melt(af_df, id_vars=["Country Name"], var_name="Year")
reshaped_af = reshaped_af.pivot(index='Year', columns='Country Name', values='value')

anz = ["Australia", "New Zealand"]
anz_df = df.loc[df["Country Name"].isin(anz)]
reshaped_anz = pd.melt(anz_df, id_vars=["Country Name"], var_name="Year")
reshaped_anz = reshaped_anz.pivot(index='Year', columns='Country Name', values='value')

world_df = df.loc[df["Country Name"] == "World"]
reshaped_world = pd.melt(world_df, id_vars=["Country Name"], var_name="Year")
reshaped_world = reshaped_world.pivot(index='Year', columns='Country Name', values='value')

""" dash and html components """
slider_font = {"font-family": "Futura", "color": "#e9903a"}

app.layout = html.Div(
	style = {"backgroundColor": "#111111", "margin": "0"}, 
	children = [

	html.Br(),
	html.Br(),

	html.H1("Military Expenditure as a Percentage of GDP", style = {"text-align":"center", "color": "#fde725", "font-family": "Futura"}),

	dcc.Graph(id='military_map', figure={}),

	dcc.Slider(id = "select_year",
		updatemode = "drag",
		value = 2018,
		min = 1960,
		max = 2018,
		marks = {
		2018: {"label": "2018", "style": slider_font},
		2015: {"label": "2015", "style": slider_font},
		2010: {"label": "2010", "style": slider_font},
		2005: {"label": "2005", "style": slider_font},
		2000: {"label": "2000", "style": slider_font},
		1995: {"label": "1995", "style": slider_font},
		1990: {"label": "1990", "style": slider_font},
		1985: {"label": "1985", "style": slider_font},
		1980: {"label": "1980", "style": slider_font},
		1975: {"label": "1975", "style": slider_font},
		1970: {"label": "1970", "style": slider_font},
		1965: {"label": "1965", "style": slider_font},
		1960: {"label": "1960", "style": slider_font}
		}),

	html.Div(id='output_container', children=[]),
	html.Br(),

	dcc.Dropdown(id = "select_region",
	options = [
	{"label": "World", "value": "reshaped_world"},
	{"label": "North America", "value": "reshaped_na"},
	{"label": "South America", "value": "reshaped_sa"},
	{"label": "West Europe", "value": "reshaped_weu"},
	{"label": "East Europe", "value": "reshaped_eeu"},
	{"label": "Africa", "value": "reshaped_af"},
	{"label": "West Asia", "value": "reshaped_wa"},
	{"label": "East Asia", "value": "reshaped_ea"}],
	value = "reshaped_world",
	style = {"width": "40%", "margin": "auto", "font-family": "Futura", "color": "black"}),

	html.Div(id='output', children=[]),
	html.Br(),

	dcc.Graph(id="line_map", figure={}),
	html.Br(),
	html.Br()

	])



""" callback. connect Plotly graphs with Dash Components""" 
@app.callback(
	[Output(component_id = "output_container", component_property = "children"),
	Output(component_id = "military_map", component_property = "figure"),
	Output(component_id= "output", component_property = "children"),
	Output(component_id="line_map", component_property= "figure" )],

	[Input(component_id = "select_year", component_property = "value"),
	Input(component_id = "select_region", component_property = "value")]
	)

def update_graphs(selected_map, selected_graph):
	""" updates line graph and choropleth map given user input from the 
	Dash Component Slider and Dash Component Dropdown """
	container = None
	container2 = None

	""" converts selected variable to its corresponding string """
	selected_map = f"{selected_map}"

	""" user input for the line plot determines the utilized data frame """
	if selected_graph == "reshaped_world":
		selected_graph = reshaped_world
	elif selected_graph == "reshaped_na":
		selected_graph =  reshaped_na
	elif selected_graph == "reshaped_sa":
		selected_graph = reshaped_sa
	elif selected_graph == "reshaped_weu":
		selected_graph = reshaped_weu
	elif selected_graph == "reshaped_eeu":
		selected_graph = reshaped_eeu
	elif selected_graph == "reshaped_wa":
		selected_graph = reshaped_wa
	elif selected_graph == "reshaped_ea":
		selected_graph = reshaped_ea
	elif selected_graph == "reshaped_af":
		selected_graph = reshaped_af

	""" choropleth map """
	fig = px.choropleth(
		title = "Year: " + selected_map,
		data_frame = df,
		locationmode = "country names",
		locations = "Country Name",
		scope = "world",
		color = selected_map,
		color_continuous_scale = "Inferno",
		range_color = [0,20],
		template = "plotly_dark",
		)

	fig.update_layout(
		coloraxis_colorbar = dict(
			title = "Percentage",
			lenmode = "pixels",
			len = 450),
		margin=dict(l=30, r=0, t=50, b=0),
		font_family = "Futura",
		font_color = "#e9903a",
		height = 650,
		title_x = 0.5)

	""" line graph """
	fig2 = px.line(
		data_frame = selected_graph,
		template = "plotly_dark",
		labels = {"value": "Percentage"})

	fig2.update_layout(
		margin=dict(l=80, r=30, t=0, b=0),
		font_family = "Futura",
		font_color = "#e9903a",
		legend_title_font_color = "#fde725",
		xaxis_title_font_color = "#fde725",
		yaxis_title_font_color = "#fde725")

	return container, fig, container2, fig2



""" runs application """
if __name__ == "__main__":
	app.run_server()
