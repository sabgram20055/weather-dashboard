import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output  # ✅ THIS FIXES YOUR ERROR

# Load Data
df = pd.read_csv("21.4434844005937, 87.0234... yeartodate.csv")
df['datetime'] = pd.to_datetime(df['datetime'])
df['sunrise'] = pd.to_datetime(df['sunrise'])
df['sunset'] = pd.to_datetime(df['sunset'])
df['daylight_hrs'] = (df['sunset'] - df['sunrise']).dt.total_seconds() / 3600

# Dropdown options
chart_options = {
    "Temperature (Max/Min)": ["tempmax", "tempmin"],
    "Humidity": ["humidity"],
    "UV Index": ["uvindex"],
    "Cloud Cover": ["cloudcover"],
    "Wind Speed/Gust": ["windspeed", "windgust"],
    "Precipitation": ["precip"],
    "Solar Energy": ["solarenergy"],
    "Daylight Hours": ["daylight_hrs"]
}

# Dash App
app = Dash(__name__)
app.title = "Weather Dashboard"

app.layout = html.Div([
    html.H1("🌦️ Interactive Weather Dashboard", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='chart-dropdown',
        options=[{"label": key, "value": key} for key in chart_options.keys()],
        value="Temperature (Max/Min)"
    ),
    dcc.Graph(id='line-chart')
])

# Callback function
@app.callback(
    Output('line-chart', 'figure'),
    Input('chart-dropdown', 'value')
)
def update_chart(selected_chart):
    cols = chart_options[selected_chart]
    fig = px.line(df, x='datetime', y=cols, title=selected_chart)
    return fig

# Run server
if __name__ == '__main__':
    app.run(debug=True)

