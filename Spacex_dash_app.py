import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
spacex_df = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
print(spacex_df.head())
app = dash.Dash(__name__)

# Create a dataframe with just "Launch Site" and "class"

filtered_site = spacex_df[['Launch Site', 'class']]

# Get a dataframe with total launches per launch site

launches = filtered_site.groupby('Launch Site', as_index=False).count()

# Create a list of launch site names
site_names = list(launches['Launch Site'])
site_names.append('All')

#  We will define a function to create a pie chart based on the parameters chosen in the dashboard


def create_pie_chart(entered_site='All'):
    if (entered_site == 'All'):
        pie_fig = px.pie(launches, values='class',
                         names='Launch Site', title='Launches by Launch Site')
    else:
        df = filtered_site[filtered_site['Launch Site'] == entered_site]
        lbl = ['Success', 'Failure']
        data = []
        succ = (df['class'] == 1).sum()
        data.append(succ)
        fail = (df['class'] == 0).sum()
        data.append(fail)
        pie_fig = px.pie(values=data, names=lbl, title=(
            f'Launch success and failure of site :{entered_site}'))
    return (pie_fig)

# Define a function to create scatter chart based on the parameters chosen in the dashboard
# Rabge slider vreturns a list of 2 values - min and max


def create_scatter_chart(payload=[1000,3000]):
    dff = spacex_df[spacex_df['Payload Mass (kg)'].between(
        payload[0], payload[1])]
    scatter_fig = px.scatter(dff, x='Payload Mass (kg)',
                             y='class', color='Booster Version Category') 
    scatter_fig.update_traces(marker_size=15)
    return (scatter_fig)


payload = [*range(0, 10000, 100)]

payload_min = 0
payload_max = 10000
mark_values = {0: '0',
               1000: '1000',
               2000: '2000',
               3000: '3000',
               4000: '4000',
               5000: '5000',
               6000: '6000',
               7000: '7000',
               8000: '8000',
               9000: '9000',
               10000: '10000'}

# Create a dropdwon section for the pie chart

entered_site = dcc.Dropdown(id='entered_site', options=site_names, value='All') 

# Create a range slider for payload mass for use with Scatter chart

slide = dcc.RangeSlider(id='slide',
                        min=0,
                        max=10500,
                        value=[1000,3000],
                        marks=mark_values,
                        step=None)


# app=Dash(title='Analysis of Falcon rocket launches')

# Now let us define the layout

app.layout = html.Div(
    children=[
        html.H1('SpaceX launch Records Dashboard',
                style={'text-align': 'center'}),

        html.H4('Select a Launch Site'),
        html.Div(
            children=[entered_site,
                      dcc.Graph(id='pie_chart', figure=create_pie_chart())
                      ]),
        html.H4('Select a range of payloads by sliding the slider'),
        html.Div(
            children=[slide,
                      dcc.Graph(id='scatter_chart',
                                figure=create_scatter_chart())
                      ])
    ])


@app.callback(
    Output('pie_chart', 'figure'), Input('entered_site', 'value'))
def update_pie_chart(entered_site):
    return create_pie_chart(entered_site)


@app.callback(
    Output('scatter_chart', 'figure'), Input('slide', 'value'))
def update_scatter_chart(value):
    return create_scatter_chart(value)

# Visual Analysis of pie chart and scatter plots

# Pie chart analysis

# 1. Site with largest successful launches - KSC LC 39A with 10 successful launches followed by CCAFS LC 40 with 7 successful launches
# 2. Highest success rate launch site - KSC LC 39A - 77% succes rate


# Scatter plot analysis

# 3. Payload range with highest launch succes rate - 2000 - 6000 Kg
# 4. Payload range with lowest launch success rate - 6000 - 7000 Kg
# 5. Booster version with highest launch succes rate - FT

if __name__ == "__main__":
    app.run_server(debug=True)
