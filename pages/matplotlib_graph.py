from dash import html
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

def layout():
    iris = sns.load_dataset('iris')
    plt.figure()
    plt.plot(iris['sepal_length'])
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return html.Div([
        html.H3('Exemplo Matplotlib'),
        html.Img(src='data:image/png;base64,{}'.format(img)),
        html.P('Gráfico de linha gerado com Matplotlib')
    ])
