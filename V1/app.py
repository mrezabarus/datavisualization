# import all modules
import dash
from dash import dcc, html, Input, Output
from flask import Flask
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# initiate the app
server  = Flask(__name__)
app     = dash.Dash(__name__, server = server, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])


# read the files
df = pd.read_csv('data.csv')
#print(df)


# build the components
Header_component = html.H1("HC Analysis Dashboard", style = {'color':'darkcyan'}, className='text-center')
space_component = html.H1("", style = {'color':'darkcyan'})


#visual components
#components 1
countfig = go.FigureWidget()

#countfig.px.histogram(name="Join",x=df['Year'], y=df['Join'], fill="tonexty")
#countfig.add_scatter(name="Resign",x=df['Year'], y=df['Resign'], fill="tonexty")
countfig = px.bar(df, x='Year', y='Total', color="Status", barmode="group")
countfig.update_layout(title="Employee")

totalEmp_df = df[df.Status == 'TotalEmployee']

#components 3
indicator = go.FigureWidget(
    go.Indicator(
        
        # fig = px.pie(filtered_df, values='Total',names='Status'),
        mode = "gauge+number",
        value=totalEmp_df['Total'].mean(),
        title = {'text':'Mean Pegawai'},
    )
)

totalEmpJoin_df = df[df.Status == 'TotalJoin']
#components 4
indicator2 = go.FigureWidget(
    go.Indicator(
        
        # fig = px.pie(filtered_df, values='Total',names='Status'),
        mode = "gauge+number",
        value=totalEmpJoin_df['Total'].mean(),
        title = {'text':'Mean Pegawai Join'},
    )
)

totalEmpRsg_df = df[df.Status == 'TotalResign']
#components 5
indicator3 = go.FigureWidget(
    go.Indicator(
        
        # fig = px.pie(filtered_df, values='Total',names='Status'),
        mode = "gauge+number",
        value=totalEmpRsg_df['Total'].mean(),
        title = {'text':'Mean Pegawai Resign'},
    )
)



# Design the app layout
app.layout = html.Div(
    [
        # html.H6("Change the value in the text box to see callbacks in action!"),
        # html.Div([
        #     "Input: ",
        #     dcc.Input(id='my-input', value='initial value', type='text')
        # ]),
        # html.Br(),
        # html.Div(id='my-output'),

        dbc.Row([
            Header_component
        ]),
        dbc.Row(
            [
                dbc.Col(
                    [dcc.Graph(figure=countfig)] , style={'width':'400px'}
                ), 
                dbc.Col(
                    [
                        html.Br(),
                        dcc.Slider(
                            df['Year'].min(),
                            df['Year'].max(),
                            step=None,
                            value=df['Year'].min(),
                            marks={str(Year): str(Year) for Year in df['Year'].unique()},
                            id='year-slider'
                        ),
                        dcc.Graph(id='graph-with-slider')
                    ]
                )
            ]
        ),
        dbc.Container([
            dbc.Row(
                [dbc.Col(
                    [
                        dbc.Card([
                            dbc.CardBody(
                                dcc.Graph(figure = indicator)
                            )
                        ])
                    ]
                ), dbc.Col(
                     [
                        dbc.Card([
                            dbc.CardBody(
                                dcc.Graph(figure = indicator2)
                            )
                        ])
                    ]
                ), dbc.Col(
                     [
                        dbc.Card([
                            dbc.CardBody(
                                dcc.Graph(figure = indicator3)
                            )
                        ])
                    ]
                )]
            ),
        ]),
        
    ]
)


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df[(df.Year == selected_year) & (df.Status != 'TotalEmployee')]

    # fig = px.histogram(filtered_df, x="Join",height=450, width=500)
    # fig = px.histogram(filtered_df, x='Year', y='Status')
    fig = px.pie(filtered_df, values='Total',names='Status')

    fig.update_layout(transition_duration=500)

    # countfig = go.FigureWidget()
    # countfig.add_scatter(filtered_df, x=df['Year'], y=df['Join'], fill="tonexty",log_x=True)
    # #countfig.add_scatter(filtered_df, name="Join",x=df['Year'], y=df['Join'], fill="tonexty")
    # #countfig.add_scatter(filtered_df, name="Resign",x=df['Year'], y=df['Resign'], fill="tonexty")
    # countfig.update_layout(title="Employee")

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)