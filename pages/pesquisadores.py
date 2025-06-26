import os

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, State, callback, dcc, html

from caching import retrieve_data
from utils import TITLE

PAGE_TITLE = "Pesquisadores"

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", order=2)

COORDENACAO_GERAL = {
    'nome': "Ludmila Ribeiro", 
    'minibio': "Prow scuttle parrel provost Sail ho shrouds spirits boom mizzenmast yardarm. Pinnace holystone mizzenmast quarter crow's nest nipperkin grog yardarm hempen halter furl. Swab barque interloper chantey doubloon starboard grog black jack gangway rutters.",
    'foto': 'assets/img/foto_perfil.png',
    'linkedin': "https://www.linkedin.com/in/ludmilaaribeiro/",
    'lattes': "http://lattes.cnpq.br/1234567890123456",
    'email': "ludmila.ribeiro@crisp.org",
}

COORDENADORAS = [
    {
        'nome': "Betina Barros",
        'minibio': """ Prow scuttle parrel provost Sail ho shrouds spirits boom mizzenmast yardarm. 
                    Pinnace holystone mizzenmast quarter crow's nest nipperkin grog yardarm hempen halter furl. 
                    Swab barque interloper chantey doubloon starboard grog black jack gangway rutters.
                    """,
        'foto': 'assets/img/foto_perfil.png',
        'linkedin': "https://www.linkedin.com/in/mariasilva/",
        'lattes': "http://lattes.cnpq.br/9876543210987654",
        'email': "maria.silva@crisp.org",
    },
    {
        'nome': "Muriel Akkerman",
        'minibio': """ Prow scuttle parrel provost Sail ho shrouds spirits boom mizzenmast yardarm. 
                    Pinnace holystone mizzenmast quarter crow's nest nipperkin grog yardarm hempen halter furl. 
                    Swab barque interloper chantey doubloon starboard grog black jack gangway rutters.
                    """,
        'foto': 'assets/img/foto_perfil.png',
        'linkedin': "https://www.linkedin.com/in/mariasilva/",
        'lattes': "http://lattes.cnpq.br/9876543210987654",
        'email': "muriel.silva@crisp.org",
    }
]

COORDENADORAS += COORDENADORAS*2  # Duplicando as coordenadoras para fins de exemplo

BOLSISTAS = [
    {
        'nome': "Santh Barros",
        'minibio': """ 
                    Pinnace holystone mizzenmast quarter crow's nest nipperkin grog yardarm 
                    hempen halter furl kin grog yardarm hempen halter furl halter furl halter furl
                    """,
        'foto': 'assets/img/foto_perfil.png',
        'linkedin': "https://www.linkedin.com/in/mariasilva/",
        'lattes': "http://lattes.cnpq.br/9876543210987654",
        'email': "maria.silva@crisp.org",
    },
]

BOLSISTAS += BOLSISTAS*6
def create_pesquisador_card(coordenador, foto_size=160):
    return dbc.Card(
        dbc.CardBody(
            dbc.Row([
                # Coluna do texto
                dbc.Col([
                    html.H5(coordenador['nome'], className="card-title"),
                    html.P(coordenador['minibio'], className="card-text"),
                    html.Span(
                        coordenador['email'],
                        id=f"email-span-{coordenador['email']}",
                        className="email-hover",
                        style={"fontStyle": "italic", "cursor": "pointer"},
                        title="Clique para copiar"
                    ),
                    html.Span(
                        html.I(className="bi bi-clipboard", id=f"clipboard-icon-{coordenador['email']}"),
                        className="email-hover",
                        style={"fontSize": "1.2em", "color": "#888", "marginLeft": "0.5em", "cursor": "pointer"},
                        id=f"clipboard-span-{coordenador['email']}"
                    ),
                    html.Br(),
                    html.Br(),
                    html.Div([
                        html.A(
                            html.I(className="bi bi-linkedin"),
                            href=coordenador['linkedin'],
                            target="_blank",
                            style={
                                "fontSize": "2rem",
                                "color": "#f1592a",
                                "marginRight": "3rem",
                                "transition": "color 0.2s"
                            },
                            className="icon-linkedin"
                        ),
                        html.A(
                            html.I(className="bi bi-link-45deg"),
                            href=coordenador['lattes'],
                            target="_blank",
                            style={
                                "fontSize": "2rem",
                                "color": "#f1592a",
                                "marginRight": "3rem",
                                "transition": "color 0.2s"
                            },
                            className="icon-lattes"
                        ),
                    ]),
                ], md=9, xs=12),
                # Coluna da foto
                dbc.Col(
                    html.Div(
                        html.Img(
                            src=coordenador['foto'],
                            style={
                                "width": f"{foto_size}px",
                                "height": f"{foto_size}px",
                                "objectFit": "cover"
                            }
                        ),
                        style={
                            "display": "flex",
                            "alignItems": "flex-start",  # topo
                            "justifyContent": "flex-end",  # direita
                            "height": "100%"
                        }
                    ),
                    md=3, xs=12,
                    style={"paddingTop": "15px", "paddingBottom": "0"}
                ),
            ], align="start"),
        ),
        className="mb-3"
    )

def layout():
    return [
        html.H2("Pesquisadores", className="mb-3"),
        html.P(
            """
            Essa página fornece uma visão geral dos pesquisadores envolvidos no processo.
            """
        ),
        html.Hr(),
        html.H3("Coordenação Geral", className="mb-3"),
        dbc.Row(
            [
                dbc.Col(
                    create_pesquisador_card(COORDENACAO_GERAL, foto_size=200),
                    md=12, sm=12
                )
            ]
        ),
        html.Hr(),
        html.H3("Coordenação de Pesquisa", className="mb-3"),
        dbc.Row(
            [
                dbc.Col(
                    create_pesquisador_card(coordenador),
                    md=6, sm=12
                )
                for coordenador in COORDENADORAS
            ]
        ),
        html.Hr(),
        html.H3("Bolsistas de Pesquisa", className="mb-3"),
        dbc.Row(
            [
                dbc.Col(
                    create_pesquisador_card(bolsista, foto_size=130),
                    md=4, sm=12
                )
                for bolsista in BOLSISTAS
            ]
        )
    ]
    