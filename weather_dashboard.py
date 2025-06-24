import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import os

# Define available chart options
chart_options = {
    "Temperature Max & Min": ["tempmax", "tempmin"],
    "UV Index": ["uvindex"],
    "Visibility vs Cloud Cover": ["visibility", "cloudcover"],
    "Humidity & Dew Point": ["humidity", "dew"],
    "Pressure & Wind Speed": ["pressure", "windspeed"],
    "Sunrise-Sunset Duration (hrs)": ["daylight_hrs"]
}

# Initialize Dash app
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div([
    html.H1("🌦️ Weather Forecast Dashboard", style={"textAlign": "center"}),
    dcc.Dropdown(
        id='chart-dropdown',
        options=[{"label": label, "value": label} for label in chart_options],
        value="Temperature Max & Min"
    ),
    dcc.Graph(id="line-chart")
])

# Callback to update chart
@app.callback(
    Output('line-chart', 'figure'),
    Input('chart-dropdown', 'value')
)
def update_chart(selected_chart):
    # Reload the latest CSV data
    df = pd.read_csv("21.4434844005937, 87.0234... yeartodate.csv")

    # Parse datetime columns
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['sunrise'] = pd.to_datetime(df['sunrise'])
    df['sunset'] = pd.to_datetime(df['sunset'])

    # Calculate daylight hours
    df['daylight_hrs'] = (df['sunset'] - df['sunrise']).dt.total_seconds() / 3600

    # Plot selected chart
    cols = chart_options[selected_chart]
    fig = px.line(df, x='datetime', y=cols, title=selected_chart)
    return fig

# Required for Render deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=False, host="0.0.0.0", port=port)

   
