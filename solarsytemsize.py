from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('data.csv')

app = Dash(__name__)

# Add a dropdown component with planet names as options
app.layout = html.Div([
    dcc.Dropdown(
        id='planet-dropdown',
        options=[{'label': i, 'value': i} for i in df['Name']],
        value=['Earth', 'Mars'],
        multi=True
    ),
    dcc.Graph(id='solar_system_sizes')
], style={'height': '100vh'})  # Set the height of the div to 100% of the viewport height


@app.callback(
    Output('solar_system_sizes', 'figure'),
    [Input('planet-dropdown', 'value')]
)
def update_graph(selected_planets):
    # Filter the DataFrame based on the selected planets
    dff = df[df['Name'].isin(selected_planets)]

    # Set y to 0
    dff['y'] = 0

    # Create a new variable for the x-axis that represents the order of the selected planets
    dff['x'] = range(1, len(dff) + 1)

    # Create the scatter plot
    fig = px.scatter(dff, x="x", y="y", size="Radius_km", color="Name",
                     hover_name="Name", size_max=175, color_discrete_sequence=dff['Colour'].tolist())

    # Update the y-axis to slightly larger than the maximum radius
    fig.update_yaxes(range=[-1.1 * dff['Radius_km'].max(), 1.1 * dff['Radius_km'].max()])

    # Update the layout of the figure to fill the page
    fig.update_layout(height=1000)  # Adjust this value as needed

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
