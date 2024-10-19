import plotly.express as px
from dash import html
from dash import dcc
from dash import Dash
import pandas as pd
from dash.dependencies import Input, Output
import json
import copy 

# prepare the data
dataDict = {'food': ['chicken', 'pork', 'beef', 'carrots', 'broccoli', 'apples', 'oranges', 'bananas'],
            'sales': [100, 200, 210, 120, 131, 90, 30, 60],
            'category': ['Meat', 'Meat', 'Meat', 'Vegetables', 'Vegetables', 'Fruits', 'Fruits', 'Fruits']}

df = pd.DataFrame(dataDict)

# create a treemap
figTreemap = px.treemap(df, path=['category', 'food'], values='sales')

# create a bar chart 
barColor = ['blue','blue','blue','blue','blue','blue','blue','blue']
figBarChart=px.bar(df,x='food',y='sales',height=400,color_discrete_sequence=[barColor])

# create a dash app
app = Dash()

# dash layout
app.layout = html.Div(children=[
    dcc.Graph(
        id='figTreemap',
        figure=figTreemap
    ),
    # add the bar chart to the layout
    dcc.Graph(
        id='figBarChart',
        figure=figBarChart
    )
])


@app.callback(
    Output('figBarChart', 'figure'),
    Input('figTreemap', 'hoverData')
)
def linkTreemapBarChart(hoverData): 
    # make a copy of the bar chart and color
    updateBar = copy.deepcopy(figBarChart)
    updateColor = copy.deepcopy(barColor)
    
    food = dataDict['food']

    if hoverData is not None and 'label' in hoverData['points'][0]: 
        # nothing is hovered on when 'label' is not in the dict or not on valid area

        hoverLabel = hoverData['points'][0]['label'] # get the label

        if hoverLabel in food: # when hovering on any food
            updateColor[food.index(hoverLabel)] = 'red' # change these foods' color to red
            updateBar.update_traces(marker_color=updateColor) # update the bar chart
    
    return updateBar

# start the dash app        
app.run()
