import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Load the processed data
df = pd.read_csv('formatted_sales.csv')
df['date'] = pd.to_datetime(df['date'])

# Aggregate sales by date (sum across all regions)
daily_sales = df.groupby('date')['sales'].sum().reset_index()
daily_sales = daily_sales.sort_values('date')

# Create the line chart
fig = px.line(
    daily_sales,
    x='date',
    y='sales',
    labels={'date': 'Date', 'sales': 'Total Sales ($)'}
)

# Add vertical line using a shape instead of add_vline (more compatible)
price_increase_date = pd.Timestamp('2021-01-15')

fig.add_shape(
    type='line',
    x0=price_increase_date,
    x1=price_increase_date,
    y0=0,
    y1=1,
    yref='paper',
    line=dict(color='red', dash='dash', width=2)
)

fig.add_annotation(
    x=price_increase_date,
    y=1,
    yref='paper',
    text='Price Increase (Jan 15, 2021)',
    showarrow=False,
    xanchor='left',
    yanchor='top',
    font=dict(color='red')
)

fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Total Sales ($)',
    hovermode='x unified'
)

# Build the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(
        'Pink Morsel Sales Visualiser',
        style={'textAlign': 'center', 'fontFamily': 'Arial, sans-serif', 'marginBottom': '10px'}
    ),
    html.P(
        'Visualising the impact of the Pink Morsel price increase on January 15, 2021',
        style={'textAlign': 'center', 'fontFamily': 'Arial, sans-serif', 'color': 'gray'}
    ),
    dcc.Graph(
        id='sales-line-chart',
        figure=fig,
        style={'height': '600px'}
    )
], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px'})

if __name__ == '__main__':
    app.run(debug=True)