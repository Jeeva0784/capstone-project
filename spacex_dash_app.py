# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                {'label':'All Sites', 'value':'ALL'},
                                                {'label':'CCAFS LC-40', 'value':'site1'},
                                                {'label':'CCAFS SLC-40', 'value':'site2'},
                                                {'label':'KSC LC-39A', 'value':'site3'},
                                                {'label':'VAFB SLC-4E', 'value':'site4'}
                                            ],
                                            value='ALL',
                                            placeholder='Select a Launch Site here',
                                            searchable=True
                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                value=[min_payload, max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
    )
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['class']==1]
        filtered_df = filtered_df.groupby('Launch Site')['class'].count().reset_index()
        fig = px.pie(filtered_df, values='class', names='Launch Site', title='Total Successful Launches from All Sites')
        return fig
    elif entered_site == 'site1':
        site1 = spacex_df[spacex_df['Launch Site']=='CCAFS LC-40']
        site1_df = site1.groupby('class')['Launch Site'].count().reset_index()
        fig = px.pie(site1_df, values='Launch Site', names='class', title='Launch Details of CCAFS LC-40 site',
                        color='class', color_discrete_map={0:'red', 1:'green'})
        return fig
    elif entered_site == 'site2':
        site2 = spacex_df[spacex_df['Launch Site']=='CCAFS SLC-40']
        site2_df = site2.groupby('class')['Launch Site'].count().reset_index()
        fig = px.pie(site2_df, names='class', values='Launch Site', title='Launch Details of CCAFS SLC-40 site',
                        color='class', color_discrete_map={0:'red', 1:'green'})
        return fig
    elif entered_site == 'site3':
        site3 = spacex_df[spacex_df['Launch Site']=='KSC LC-39A']
        site3_df = site3.groupby('class')['Launch Site'].count().reset_index()
        fig = px.pie(site3_df, names='class', values='Launch Site', title='Launch Details of KSC LC-39A site',
                        color='class', color_discrete_map={0:'red', 1:'green'})
        return fig
    else:
        site4 = spacex_df[spacex_df['Launch Site']=='VAFB SLC-4E']
        site4_df = site4.groupby('class')['Launch Site'].count().reset_index()
        fig = px.pie(site4_df, names='class', values='Launch Site', title='Launch Details of VAFB SLC-4E site',
                        color='class', color_discrete_map={0:'red', 1:'green'})
        return fig
    
    

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')]
)

def get_scatter_plot(entered_site,payload_range):
    payload = payload_range
    min_r=payload[0]
    max_r=payload[1]
    if entered_site == 'ALL':
        fig=px.scatter(spacex_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
            title="Correlation between Payload and Success for All Sites") 
        return fig
    elif entered_site == 'site1':
        site1 = spacex_df[spacex_df['Launch Site']=='CCAFS LC-40']
        site1_pay = site1[site1['Payload Mass (kg)']>=min_r]
        site1_pay = site1_pay[site1_pay['Payload Mass (kg)']<=max_r]
        fig = px.scatter(site1_pay, x='Payload Mass (kg)', y='class', color='Booster Version Category',
            title='Correlation between Payload and Success for CCAFS LC-40 site with varying Payload Mass (KG)')
        return fig
    elif entered_site == 'site2':
        site2 = spacex_df[spacex_df['Launch Site']=='CCAFS SLC-40']
        site2_pay = site2[site2['Payload Mass (kg)']>=min_r]
        site2_pay = site2_pay[site2_pay['Payload Mass (kg)']<=max_r]
        fig = px.scatter(site2_pay, x='Payload Mass (kg)', y='class', color='Booster Version Category',
            title='Correlation between Payload and Success for CCAFS SLC-40 site with varying Payload Mass (KG)')
        return fig
    elif entered_site == 'site3':
        site3 = spacex_df[spacex_df['Launch Site']=='KSC LC-39A']
        site3_pay = site3[site3['Payload Mass (kg)']>=min_r]
        site3_pay = site3_pay[site3_pay['Payload Mass (kg)']<=max_r]
        fig = px.scatter(site3_pay, x='Payload Mass (kg)', y='class', color='Booster Version Category',
            title='Correlation between Payload and Success for KSC LC-39A site with varying Payload Mass (KG)')
        return fig
    else:
        site4 = spacex_df[spacex_df['Launch Site']=='VAFB SLC-4E']
        site4_pay = site4[site4['Payload Mass (kg)']>=min_r]
        site4_pay = site4_pay[site4_pay['Payload Mass (kg)']<=max_r]
        fig = px.scatter(site4_pay, x='Payload Mass (kg)', y='class', color='Booster Version Category',
            title='Correlation between Payload and Success for VAFB SLC-4E site with varying Payload Mass (KG)')
        return fig



# Run the app
if __name__ == '__main__':
    app.run_server()
