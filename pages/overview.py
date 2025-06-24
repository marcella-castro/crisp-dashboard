import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html

from data.utils import number_of_countries, number_of_restaurants, top_cuisine, number_of_processos
from caching import retrieve_data
from decorators import load_df
from utils import TITLE

PAGE_TITLE = "Visão Geral"

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", path="/", order=0)



def layout():
    return [
        html.H3("Visão Geral", className="mb-3"),
        html.P(
            """Nesta página, que integra a produção intelectual
        da pesquisa nacional “Mensurando o tempo do processo de homicídio: 10 anos depois - Tempo e desfecho de processos penais de homicídio doloso”,
        apresentamos dados de natureza predominantemente quantitativa sobre a dinâmica e
        o tempo de tramitação dos casos no sistema de justiça criminal.
            """
        ),
        html.P(
            '''Esta pesquisa foi realizada pelo Centro de Estudos de Criminalidade e Segurança Pública (CRISP) da Universidade Federal de Minas Gerais (UFMG),
        sob a coordenação da professora Dra. Ludmila Ribeiro, e contou com a
        colaboração de diversos pesquisadores e estudantes de graduação e pós-graduação.'''
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4(
                                    "-",
                                    id="home-number-of-processos",
                                    className="card-title",
                                ),
                                html.H6("Processos Analisados", className="card-subtitle"),
                            ]
                        ),
                    ),
                    class_name="mb-3",
                    md=4,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4(
                                    "-",
                                    id="home-number-of-reus",
                                    className="card-title",
                                ),
                                html.H6("Número de Réus", className="card-subtitle"),
                            ]
                        ),
                    ),
                    class_name="mb-3",
                    md=4,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("-", id="home-top-cuisine", className="card-title"),
                                html.H6("Número de Vítimas", className="card-subtitle"),
                            ]
                        ),
                    ),
                    class_name="mb-3",
                    md=4,
                    sm=12,
                ),
            ],
            class_name="g-3",
        ),
    ]


@callback(
    [
        Output("home-number-of-processos", "children"),
        Output("home-number-of-reus", "children"),
        Output("home-top-cuisine", "children"),
    ],
    Input("url", "pathname"),  # Dispara ao carregar a página
)
@load_df
def update_overview(df: pd.DataFrame, _) -> tuple:
    n_proc = number_of_processos(df)
    if n_proc == 0:
        n_proc_str = "-"
    else:
        n_proc_str = str(n_proc)
    # Número de Réus
    col_reus = 'P0Q1. Número de controle (dado pela equipe)'
    if col_reus in df.columns:
        n_reus = df[col_reus].nunique()
        n_reus_str = str(n_reus)
    else:
        n_reus_str = "-"
    return (
        n_proc_str,
        n_reus_str,
        top_cuisine(df),
    )
