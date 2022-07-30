from dash import Dash, dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

class dashboard:
   '''dashboard class used to generate web dashboard app'''

   def __init__(self, project:str) -> None:
      '''initialize dashboard object with project name'''

      self.app = Dash(title='Agile Scrum Tracker')
      self.project = project
   

   def update(self, product_backlog:pd.DataFrame, sprint_backlog:pd.DataFrame, burndown_data:list) -> None:
      '''update dashboard contents'''

      self.app.layout = html.Div([
         html.H1(f'Project: {self.project}'
         ),
         html.Div([
            html.Div([
               html.H3('Product Backlog'),
               html.Div([
                  dash_table.DataTable(product_backlog.to_dict('records'), [{"name": i, "id": i} for i in product_backlog.columns])
               ])
            ], style={'margin': 20}),

            html.Div([
               html.H3('Sprint Backlog'),
               html.Div([
                  dash_table.DataTable(sprint_backlog.to_dict('records'), [{"name": i, "id": i} for i in sprint_backlog.columns])
               ]),
               html.H3('Sprint Burndown Chart'),
               dcc.Graph(
                  id='sprint-burndown',
                  figure={
                     'data': [
                        {'x': burndown_data[0], 'y': burndown_data[1], 'type': 'line', 'markers': True}
                     ],
                     'layout': {
                        'xaxis': {'title': 'Day of Month', 'zeroline': False, 'showgrid': True, 'tickmode': 'array', 'tickvals': burndown_data[0]},
                        'yaxis': {'title': 'Work Remaining (hrs)', 'zeroline': False, 'showgrid': True}
                     }
                  }
               )
            ], style={'margin': 20}),
         ], style={'display': 'flex', 'flex-direction': 'row'})
      ])

   def run(self) -> None:
      '''run web server'''

      self.app.run_server()