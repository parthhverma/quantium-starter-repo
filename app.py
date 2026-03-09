import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd

# Load the processed data
df = pd.read_csv('formatted_sales.csv')
df['date'] = pd.to_datetime(df['date'])

app = dash.Dash(__name__)

app.layout = html.Div([

    # Background decoration
    html.Div(className='bg-orb orb1'),
    html.Div(className='bg-orb orb2'),

    # Header
    html.Div([
        html.Div('🍬', style={'fontSize': '2.5rem', 'marginBottom': '8px'}),
        html.H1('Pink Morsel Sales', style={
            'margin': '0',
            'fontSize': '2.8rem',
            'fontWeight': '800',
            'letterSpacing': '-1px',
            'background': 'linear-gradient(135deg, #ff6eb4, #ff9de2)',
            'WebkitBackgroundClip': 'text',
            'WebkitTextFillColor': 'transparent',
        }),
        html.P('Soul Foods · Sales Performance Dashboard', style={
            'margin': '6px 0 0',
            'color': '#a0aec0',
            'fontSize': '0.95rem',
            'letterSpacing': '0.05em',
            'fontFamily': 'monospace',
        }),
    ], style={
        'textAlign': 'center',
        'padding': '48px 20px 32px',
    }),

    # Card container
    html.Div([

        # Region filter label + radio
        html.Div([
            html.Span('FILTER BY REGION', style={
                'fontSize': '0.7rem',
                'letterSpacing': '0.15em',
                'color': '#718096',
                'fontFamily': 'monospace',
                'fontWeight': '600',
            }),
            dcc.RadioItems(
                id='region-filter',
                options=[
                    {'label': 'All Regions', 'value': 'all'},
                    {'label': 'North',       'value': 'north'},
                    {'label': 'East',        'value': 'east'},
                    {'label': 'South',       'value': 'south'},
                    {'label': 'West',        'value': 'west'},
                ],
                value='all',
                inline=True,
                style={'marginTop': '10px'},
                inputStyle={
                    'marginRight': '6px',
                    'accentColor': '#ff6eb4',
                },
                labelStyle={
                    'marginRight': '24px',
                    'fontSize': '0.9rem',
                    'color': '#e2e8f0',
                    'cursor': 'pointer',
                    'fontFamily': "'DM Sans', sans-serif",
                }
            ),
        ], style={
            'marginBottom': '28px',
            'paddingBottom': '20px',
            'borderBottom': '1px solid rgba(255,255,255,0.07)',
        }),

        # Chart
        dcc.Graph(id='sales-chart', config={'displayModeBar': False}),

        # Footer note
        html.P('↑ Red dashed line marks the price increase on January 15, 2021', style={
            'textAlign': 'center',
            'color': '#718096',
            'fontSize': '0.78rem',
            'marginTop': '16px',
            'fontFamily': 'monospace',
        }),

    ], style={
        'background': 'rgba(255,255,255,0.03)',
        'border': '1px solid rgba(255,255,255,0.08)',
        'borderRadius': '20px',
        'padding': '36px 40px',
        'maxWidth': '1100px',
        'margin': '0 auto 60px',
        'backdropFilter': 'blur(12px)',
        'boxShadow': '0 25px 60px rgba(0,0,0,0.4)',
    }),

], style={
    'minHeight': '100vh',
    'background': 'radial-gradient(ellipse at 20% 20%, #1a0a2e 0%, #0d0d1a 60%, #0a0a0f 100%)',
    'fontFamily': "'DM Sans', 'Segoe UI', sans-serif",
    'position': 'relative',
    'overflow': 'hidden',
})

# Inject Google Font + global CSS
app.index_string = '''
<!DOCTYPE html>
<html>
<head>
    {%metas%}
    <title>Pink Morsel Sales Dashboard</title>
    {%favicon%}
    {%css%}
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700;800&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #0a0a0f; }
        .bg-orb {
            position: fixed;
            border-radius: 50%;
            filter: blur(80px);
            pointer-events: none;
            z-index: 0;
        }
        .orb1 {
            width: 500px; height: 500px;
            background: radial-gradient(circle, rgba(255,110,180,0.15), transparent 70%);
            top: -150px; left: -100px;
        }
        .orb2 {
            width: 400px; height: 400px;
            background: radial-gradient(circle, rgba(130,80,255,0.12), transparent 70%);
            bottom: -100px; right: -80px;
        }
    </style>
</head>
<body>
    {%app_entry%}
    <footer>{%config%}{%scripts%}{%renderer%}</footer>
</body>
</html>
'''


@app.callback(
    Output('sales-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_chart(selected_region):
    filtered = df if selected_region == 'all' else df[df['region'] == selected_region]
    daily = filtered.groupby('date')['sales'].sum().reset_index().sort_values('date')

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=daily['date'],
        y=daily['sales'],
        mode='lines',
        line=dict(color='#ff6eb4', width=2.5, shape='spline'),
        fill='tozeroy',
        fillcolor='rgba(255,110,180,0.08)',
        hovertemplate='<b>%{x|%b %d, %Y}</b><br>Sales: $%{y:,.0f}<extra></extra>',
    ))

    # Price increase line
    price_date = pd.Timestamp('2021-01-15')
    fig.add_shape(
        type='line',
        x0=price_date, x1=price_date,
        y0=0, y1=1, yref='paper',
        line=dict(color='#fc8181', dash='dash', width=1.5)
    )
    fig.add_annotation(
        x=price_date, y=0.97, yref='paper',
        text='Price Increase', showarrow=False,
        xanchor='left', xshift=8,
        font=dict(color='#fc8181', size=11, family='monospace'),
    )

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="'DM Sans', sans-serif", color='#a0aec0'),
        xaxis=dict(
            title='Date',
            gridcolor='rgba(255,255,255,0.05)',
            linecolor='rgba(255,255,255,0.1)',
            tickfont=dict(size=11),
        ),
        yaxis=dict(
            title='Total Sales ($)',
            gridcolor='rgba(255,255,255,0.05)',
            linecolor='rgba(255,255,255,0.1)',
            tickprefix='$',
            tickfont=dict(size=11),
        ),
        margin=dict(l=10, r=10, t=10, b=10),
        height=440,
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#1a1a2e',
            bordercolor='#ff6eb4',
            font=dict(color='white', size=12),
        ),
    )

    return fig


if __name__ == '__main__':
    app.run(debug=True)