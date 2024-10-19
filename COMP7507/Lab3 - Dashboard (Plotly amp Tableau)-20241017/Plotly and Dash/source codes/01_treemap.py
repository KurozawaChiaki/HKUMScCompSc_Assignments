import plotly.express as px	
import pandas as pd
from dash import html 
from dash import dcc
from dash import Dash

# prepare the data
dataDict = {
    'food':['chicken', 'pork', 'beef', 'carrots', 'broccoli', 'apples', 'oranges', 'bananas'], 
    'sales':[100, 200, 210, 120, 131, 90, 30, 60],
    'category':['Meat','Meat','Meat','Vegetables','Vegetables','Fruits','Fruits','Fruits']
}
df = pd.DataFrame(dataDict)

# create a treemap
figTreemap = px.treemap(df, path=['category', 'food'], values='sales')

# create a dash app
app = Dash()

# dash layout
app.layout = html.Div([
    dcc.Graph(
        id='figTreemap', # one id for one component
        figure=figTreemap
    )
])

# start the dash app
app.run()
