from dash import html
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

def layout():
    iris = sns.load_dataset('iris')
    plt.figure()
    sns.histplot(iris['sepal_length'], kde=True)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return html.Div([
        html.H3('Exemplo Seaborn'),
        html.Img(src='data:image/png;base64,{}'.format(img)),
        html.P('Histograma gerado com Seaborn')
    ])
