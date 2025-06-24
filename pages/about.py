import dash
from dash import html

from utils import TITLE

PAGE_TITLE = "About"

dash.register_page(
    __name__,
    name=PAGE_TITLE,
    title=f"{PAGE_TITLE} | {TITLE}",
)


layout = [
    html.H3("Sobre o modelo"),
    html.P(
        [
            "O modelo desse Dashboard é criado por ",
            html.A("Niek van Leeuwen", href="https://niekvanleeuwen.nl"),
            ", como parte do desafio:  ",
            html.A("Autumn App Challenge 2024", href="https://community.plotly.com/t/autumn-app-challenge/87373"),
            " e editado por ", html.A("Marcella Castro", href="")," para a pesquisa 'Mensurando o Tempo do Processo de Homicídio'.",
        ]
    ),
    html.H5("Dados Brutos"),
    html.P(
        [
            "Os dados utilizados neste Dashboard são provenientes do preenchimento de formulários por cada um dos bolsistas do projeto e pelo trabalho das coordenadoras de pesquisa. o DataSet referência de cada estado pode ser encontrado em cada um dos links abaixo: "
        ]
    ),
    html.Ul(
        [
            html.Li(
                [
                    html.B("São Paulo: "),
                    "Processo",
                    html.A("via Wikimedia Commons", href="https://creativecommons.org/licenses/by-sa/3.0"),
                    ".",
                ],
            ),
            html.Li(
                [
                    html.B("Minas Gerais: "),
                    "Processo",
                    html.A("Kaggle", href="https://www.kaggle.com/datasets/ngshiheng/michelin-guide-restaurants-2021"),
                    ".",
                ],
            ),
        ]
    ),
    html.H5("Code"),
    html.P(
        [
            "The code for this app is available on ",
            html.A("Github", href="https://github.com/niekvleeuwen/michelin-guide-restaurants-dashboard"),
            ".",
        ]
    ),
]
