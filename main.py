import os

import dash
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, dcc, html
from dotenv import load_dotenv
from flask import send_from_directory
from loguru import logger

from caching import cache, retrieve_data
from data.database import Database
from utils import TITLE

load_dotenv()

app = Dash(title=TITLE, external_stylesheets=[dbc.icons.BOOTSTRAP], use_pages=True, suppress_callback_exceptions=True)
server = app.server
if cache is not None:
    cache.init_app(app.server)

df = retrieve_data()
Database().load(df)

CRISP_LOGO = "assets/img/logos/crisp_logo.png"


NAVBAR = {
    "Dados": {
        "Visão Geral": {"icon": "bi bi-house", "relative_path": "/"},
        "Estados": {"icon": "bi bi-globe-americas", "relative_path": "/estados"},
        "Réu": {"icon": "bi bi-person", "relative_path": "/reu"},
        "Vítima": {"icon": "bi bi-person-fill", "relative_path": "/vitima"},
        "Provas": {"icon": "bi bi-fingerprint", "relative_path": "/provas"},
    },
    "Pesquisa": {
        "Histórico": {"icon": "bi bi-folder2-open", "relative_path": "/llm-analysis"},
        "Pesquisadores": {"icon": "bi bi-award-fill", "relative_path": "/pesquisadores"},
    },
    "Mais": {
        "Dados brutos": {"icon": "bi bi-clipboard-data-fill", "relative_path": "/about"},
        "Sobre o CRISP": {"icon": "bi bi-info-circle", "relative_path": "/about"},
        "Sobre o Site": {"icon": "bi bi-code-square", "relative_path": "/about"},
    },
}


def generate_nav_links(navbar_dict):
    nav_items = []
    for category, items in navbar_dict.items():
        # Add a category header
        nav_items.append(html.Div(category, className="navbar-category"))
        # Add links for each item in the category
        for label, details in items.items():
            nav_items.append(
                dbc.NavLink(
                    [
                        html.I(className=details["icon"], style={"margin-right": "0.5rem"}),
                        label,
                    ],
                    href=details["relative_path"],
                    className="nav-link",
                )
            )
    return nav_items


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "overflow-y": "auto",  # Adicione esta linha para rolagem vertical
    "zIndex": 1000,        # Garante que fique acima do conteúdo
}


sidebar = html.Div(
    [
        html.Img(src=CRISP_LOGO, width=230),
        html.Hr(),
        html.P("Mensurando o Tempo do Processo de Homicídio", className="lead"),
        dbc.Nav([], vertical=True, pills=True, id="sidebar-nav"),
    ],
    style=SIDEBAR_STYLE,
    className="d-none d-md-block",  # Hidden on small screens, visible on medium+
    id="sidebar",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            dcc.Link(
                [
                    html.Img(src=CRISP_LOGO, width=30, height=30, className="d-inline-block align-top mr-2"),
                    "CRISP Dashboard",
                ],
                href="/",
                className="navbar-brand",
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                generate_nav_links(NAVBAR),
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="light",
    dark=False,
    className="d-block d-md-none",  # Visible only on small screens, hidden on medium+
)

content = html.Div(
    dbc.Spinner(
        dash.page_container,
        delay_show=0,
        delay_hide=100,
        color="primary",
        spinner_class_name="fixed-top",
        spinner_style={"margin-top": "100px"},
    ),
    className="content",
)

app.layout = html.Div(
    [
        dcc.Location(id="url"),
        sidebar,
        navbar,
        content,
    ]
)


@app.callback(Output("sidebar-nav", "children"), Input("url", "pathname"))
def update_navbar(url: str) -> list:
    return [
        html.Div(
            [
                html.H5(navbar_group),
                html.Hr(),
                html.Div(
                    [
                        dcc.Link(
                            html.Div(
                                [html.I(className=page_values["icon"] + " mr-1"), page_name],
                                className="d-flex align-items-center",
                            ),
                            href=page_values["relative_path"],
                            className="nav-link active mb-1"
                            if page_values["relative_path"] == url
                            else "nav-link mb-1",
                        )
                        for page_name, page_values in navbar_pages.items()
                    ]
                ),
            ],
            className="mb-4",
        )
        for navbar_group, navbar_pages in NAVBAR.items()
    ]


@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks"), Input("url", "pathname")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, _, is_open):
    # close collapse when navigating to new page
    if dash.callback_context.triggered_id == "url":
        return False

    if n:
        return not is_open
    return is_open


# Serve static files
@app.server.route("/static/<path:path>")
def static_file(path):
    static_folder = os.path.join(os.getcwd(), "static")
    return send_from_directory(static_folder, path)


app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        {%css%}
        <link rel="icon" href="assets/img/logos/crisp_logo.png" type="image/png">
    </head>
    <body>
        {%app_entry%}
        {%config%}
        {%scripts%}
        {%renderer%}
    </body>
</html>

<style>
@import url('https://fonts.googleapis.com/css2?family=Figtree:ital,wght@0,300..900;1,300..900&display=swap');
</style>
"""

if __name__ == "__main__":
    app.run(debug=True)
