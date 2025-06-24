from dash import dcc, html
import plotly.express as px
import seaborn as sns

def layout():
    iris = sns.load_dataset('iris')
    fig = px.scatter(iris, x='sepal_width', y='sepal_length', color='species', title='Gráfico Plotly')
    return html.Div([
        html.H3('Exemplo Plotly'),
        dcc.Graph(figure=fig)
    ])
