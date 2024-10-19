import plotly.express as px
from dash import html 
from dash import dcc
from dash import Dash
import pandas as pd
from dash.dependencies import Input, Output
import json

# prepare the data
dataDict = {'food': ['chicken', 'pork', 'beef', 'carrots', 'broccoli', 'apples', 'oranges', 'bananas'],
            'sales': [100, 200, 210, 120, 131, 90, 30, 60],
            'category': ['Meat', 'Meat', 'Meat', 'Vegetables', 'Vegetables', 'Fruits', 'Fruits', 'Fruits']}

df = pd.DataFrame(dataDict)

# create a treemap
figTreemap = px.treemap(df, path=['category', 'food'], values='sales')

# create a dash app
app = Dash()

# dash layout
app.layout = html.Div(children=[
    dcc.Graph(
        id='figTreemap', # one id for one component
        figure=figTreemap
    ),
    html.Pre(id='myoutput'), # add another component
])

# decorator tell the dash app to call this function when an event is triggered
@app.callback(
    Output('myoutput', 'children'),
    Input('figTreemap', 'hoverData') # 'hoverData' is one of the callbacks attribute
)
def showHoverData(hoverData):  
    return json.dumps(hoverData, indent=2) # create json format info

# start the dash app
app.run()
