import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html
import plotly.express as px
import geopandas as gpd
from shapely.geometry import Point
from dash import Input, Output, callback, dcc, html
import dash_table
import plotly.graph_objects as go
import numpy as np 
import unicodedata

from utils import TITLE
from decorators import load_df

def carregar_df_estado(estado):
    if estado == "Minas Gerais":
        return pd.read_csv("data/TJMG/df_processo_TJMG.csv")
    else:
        return pd.read_csv("data/TJSP/df_processo_TJSP.csv")
# ----------------------

PAGE_TITLE = "Estados"
dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", order=2)

ESTADOS = {"São Paulo": "SP",
        "Minas Gerais": "MG"}  # Adicione outros estados conforme necessário



# Carregue o shapefile do Brasil 
gdf_brasil = gpd.read_file("data/shapefiles/BR_UF_2024.shp")

# Dicionário de colunas de data: nome amigável -> nome real no DataFrame
COLUNAS_DATA = {
    'Crime': 'P0Q21. Data do crime:',
    'Flagrante': 'P1Q2. Data da prisão em flagrante:',
    'Audiência de Custódia': 'P2Q1. Data da audiência de custódia:',
    'Abertura do Inquérito Policial': 'P3Q1. Data da abertura do Inquérito Policial:',
    'Relatório Final do Inquérito Policial': 'P3Q28. Data do relatório final do Inquérito Policial:',
    'Pedido de Arquivamento': 'P4Q1. Data do pedido de arquivamento:',
    'Decisão de Arquivamento': 'P4Q3. Data da decisão/despacho do juiz após o pedido de arquivamento:',
    'Oferecimento da Denúncia': 'P4Q7. Data do oferecimento da denúncia:',
    'Citação do réu': 'P5Q2. Qual a data da citação do réu?', 
    'Defesa Prévia': 'P5Q5. Qual a data da defesa prévia/resposta à acusação?',
    '1a Audiência de Instrução e Julgamento': 'P6Q0. Qual a data em que a denúncia foi recebida?',
    'Última Audiência de Instrução e Julgamento': "P6Q3. Se sim, qual a data da última audiência de instrução realizada?",
    'Alegações Finais da Acusação': 'P6Q8. Data das alegações finais da acusação:',
    'Alegações Finais da Defesa': 'P6Q13. Data das alegações finais da defesa:',
    'Sentença 1a Fase do Júri':'P7Q2. Data da decisão que finaliza a primeira fase do Júri:',
    'Realização de Audiência de Júri': 'P8Q4. Data em que a audiência de júri foi realizada:',
    'Sentença de Júri': 'P8Q20. Data em que a sentença de júri foi prolatada:',
    'Decisão que extinguiu a punibilidade': 'P9Q0C. Data da decisão que extingue a punibilidade do réu:',
    'Trânsito em julgado': 'P9Q1. Data do trânsito em julgado da sentença:',
    'Arquivamento definitivo': 'P9Q2. Data do arquivamento definitivo do processo:'
}

NOME_PADRONIZADO = {
    "karolayne": "Karolayne Gonsalves",
    "mizaelquerinopereirajunior": "Mizael Pereira Junior",
    "samuelalvesaraujo": "Samuel Araújo",
    "santhbrasilinodasilva": "Santh Brasilino",
    "thaianetittomachadosouto": "Thaiane Souto",
    "ana": "Ana Lívia Fernandes",
    "ana livia fernandes": "Ana Lívia Fernandes",
    "Mizael Querino Pereira Júnior": "Mizael Pereira Junior",
    "mizael querino pereira junior": "Mizael Pereira Junior",
    "camila luiza de sena": "Camila de Sena",
    "camila de sena": "Camila de Sena",
    "gabrielcorrea": "Gabriel Correa",
    "mariagiovana": "Maria Giovana",
    "pablomartins": "Pablo Martins",
    "hana": "Hana Medrado",
    "brunodesantanasantos": "Bruno Santos",
    "emilydossantossilva": "Emily Silva",
    "leticiacheminbulla": "Letícia Chemin",
    "rannadesireecarvalhodosantos": "Ranna Desiree dos Santos",
    "rannadesireecarvalhodossantos": "Ranna Desiree dos Santos",
    "rannadesireecervalhodossantos": "Ranna Desiree dos Santos",
    "ranna desireecarvalho dos santoss": "Ranna Desiree dos Santos",
    "rodrigoraimundo": "Rodrigo Raimundo",
    "amandamariamaianettocampos": "Amanda Campos",
    "liamaiatahim": "Lia Tahim",
    "luannasarres": "Luanna Sarres",
    "mariacleidealmeida": "Maria Cleide Almeida",
    "natalycampolina": "Nataly Campolina",
    "thamiresdeoliveira": "Thamires de Oliveira",
    "maria clara fontes bessa": "Maria Clara Bessa",
    "maria clara": "Maria Clara Bessa",
    "bruno de santana sdantos": "Bruno Santos"
}

# Dicionário de colunas amigáveis para o gráfico donut
COLUNAS_DONUT = {
    "Prisão em Flagrante": "P1Q1. Houve prisão em flagrante desse réu?",
    "Atendimento da Polícia Civil no Local da Morte": 'P3Q11. Há menção ao atendimento da Polícia Civil no local da morte?',
    "Atendimento da Perícia no Local da Morte": 'P3Q12. Há menção ao atendimento da perícia no local da morte?', 
    "Remoção do Corpo pelo IML": 'P3Q13. Há menção de que houve remoção do corpo pelo IML?', 
}

COLUNAS_DONUT_MP = {
    "Pedido de Arquivamento pelo MP": 'P4Q0. Houve pedido de arquivamento pelo Ministério Público (MP)?', 
    "Recurso da Decisão": 'P8Q54. Se sim, o primeiro recurso foi interposto por quem?', 
    "Existência de Defesa no IP": 'P3Q17. Há menção à presença de defesa constituída no termo de interrogatório policial?',
    "Tipo de Defesa no IP": 'P3Q18. Se sim, essa defesa era:',
    "Tipo de Defesa na 1a Fase do Júri": 'P5Q6. Natureza da defesa:',
    "Tipo de Defesa na 1a Fase do Júri": 'P8Q5. Qual foi a natureza da defesa no Tribunal do Júri?',
    "Pedido de Liberdade pela Defesa": 'P6Q16. Em qualquer peça da defesa anterior à sentença de primeira fase, há registro de pedido para revogar prisão ou de qualquer forma colocar o réu em liberdade?', 

}

COLUNAS_DONUT_JUIZ = {
    "Taxa de Extinção da Punibilidade": 'P9Q0A. Houve decisão pela extinção de punibilidade em qualquer momento do processo?', 
    "Taxa de Condenação" : 'P8Q24. Houve decisão pela condenação, absolvição do réu, desclassificação do crime ou imposição de medida de segurança?', 
    "Destinação da Arma de Fogo": 'P9Q0. O juiz analisou a destinação da arma de fogo usada no crime?',
}

import re

def mascarar_numero_processo(numero):
    """
    Mascara o número do processo no padrão CNJ:
    Exemplo: 0000008-44.1994.8.26.0177 -> 000XXX-XX.1994.8.26.0177 -> 000XXX-XX.1994.8.26.XXXX
    Mantém os 3 primeiros dígitos, o ano e os 4 dígitos finais, censurando o restante.
    """
    import re
    if not isinstance(numero, str):
        numero = str(numero)
    # Regex para padrão CNJ: NNNNNNN-DD.AAAA.J.TR.OOOO
    match = re.match(r"(\d{3})\d{4}-\d{2}\.(\d{4})\.(\d)\.(\d{2})\.(\d{4})", numero)
    if match:
        # Mantém os 3 primeiros, ano, e os 4 finais
        return f"{match.group(1)}XXX-XX.{match.group(2)}.{match.group(3)}.{match.group(4)}.XXXX"
    # Se não bater o padrão, retorna só os 3 primeiros e o resto como X
    return numero[:3] + "XXX-XX.XXXX.X.XX.XXXX"

def converter_dias_em_ymd(dias):
    if pd.isna(dias):
        return "-"
    dias = int(dias)
    anos = dias // 365
    meses = (dias % 365) // 30
    dias_restantes = (dias % 365) % 30
    partes = []
    if anos > 0:
        partes.append(f"{anos}a")
    if meses > 0:
        partes.append(f"{meses}m")
    if dias_restantes > 0 or not partes:
        partes.append(f"{dias_restantes}d")
    return ' '.join(partes)
def calcular_linha_tempo_acumulada(df, colunas_data_dict, metrica="media"):
    eventos = list(colunas_data_dict.keys())
    colunas = list(colunas_data_dict.values())
    datas = {}
    for evento, coluna in zip(eventos, colunas):
        if coluna in df.columns:
            datas[evento] = pd.to_datetime(df[coluna], dayfirst=True, errors='coerce')
        else:
            datas[evento] = pd.Series([pd.NaT]*len(df))
    if metrica == "mediana":
        valores = {evento: datas[evento].dropna().median() for evento in eventos}
    else:
        valores = {evento: datas[evento].dropna().mean() for evento in eventos}
    evento_inicial = eventos[0]
    data_inicial = valores[evento_inicial]
    dias_acumulados = []
    for evento in eventos:
        if pd.isna(valores[evento]) or pd.isna(data_inicial):
            dias_acumulados.append(0)
        else:
            dias_acumulados.append((valores[evento] - data_inicial).days)
    return eventos, dias_acumulados, metrica
def montar_linha_tempo(eventos, dias_acumulados, metrica):
    import numpy as np
    # Níveis mais próximos da linha do tempo para eventos acima/abaixo
    levels = np.tile([0.01, -0.01, 0.02, -0.02], int(np.ceil(len(eventos)/2)))[:len(eventos)]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dias_acumulados,
        y=[1]*len(eventos),
        mode="lines+markers",
        marker=dict(size=12, color="#d54d24", line=dict(width=2, color="#2c3e50")),
        line=dict(color="#d54d24", width=2),
        text=eventos,
        hoverinfo="text+x"
    ))
    for idx, (x, evento, dias, level) in enumerate(zip(dias_acumulados, eventos, dias_acumulados, levels)):
        texto_dias = "Marco Inicial" if idx == 0 else f"{converter_dias_em_ymd(round(dias))}"
        level  = 0.002 if idx == 0 else level
        y_base = 1 + level
        # Linha conectando o marcador ao nome do evento
        fig.add_shape(
            type="line",
            x0=x, x1=x,
            y0=1, y1=y_base,
            line=dict(color="lightgray", width=1),
            layer="below"
        )
        # Anotações bem próximas da linha
        fig.add_annotation(x=x, y=y_base + (0.001 if level > 0 else -0.001), text=evento, showarrow=False, font=dict(size=11))
        fig.add_annotation(x=x, y=y_base + (0.0028 if level > 0 else -0.0028), text=texto_dias, showarrow=False, font=dict(size=10, color="gray"))
    fig.update_layout(
        title=f"Linha do Tempo - Dias acumulados entre eventos<br><sup>Valor referência: {metrica.title()}</sup>",
        yaxis=dict(visible=False),
        xaxis_title="Dias acumulados",
        margin=dict(l=40, r=40, t=60, b=40),
        height=350,
        plot_bgcolor="#fff",
        paper_bgcolor="#fff",
        font=dict(family="Arial", size=13),
    )
    return fig
def calcular_diferenca_datas(df, col_data_inicial, col_data_final, col_proc, col_reus):
    df_box = df.copy()
    df_box['Data_Inicial'] = pd.to_datetime(df_box[col_data_inicial], dayfirst=True, errors='coerce')
    df_box['Data_Final'] = pd.to_datetime(df_box[col_data_final], dayfirst=True, errors='coerce')
    df_box['Diferenca_dias'] = (df_box['Data_Final'] - df_box['Data_Inicial']).dt.days
    df_validos = df_box[df_box['Diferenca_dias'].notnull()]
    dados = df_validos['Diferenca_dias']
    n_proc_validos = df_validos[col_proc].nunique() if col_proc else 0
    n_reus_validos = df_validos[col_reus].nunique() if col_reus in df_validos.columns else 0
    return df_validos, dados, n_proc_validos, n_reus_validos
def gerar_boxplot(df_validos, dados, col_data_inicial, col_data_final, media, mediana):
    fig = px.box(
        df_validos, y='Diferenca_dias', points='all',
        labels={"Diferenca_dias": "Diferença em dias"},
        template="plotly_white",
        color_discrete_sequence=["#c77055"]
    )
    fig.update_traces(marker=dict(color="#188e44", size=6, opacity=0.7),
                      line=dict(color="#c77055", width=2))
    nome_inicial = next((k for k, v in COLUNAS_DATA.items() if v == col_data_inicial), col_data_inicial)
    nome_final = next((k for k, v in COLUNAS_DATA.items() if v == col_data_final), col_data_final)
    fig.update_layout(
        title=f"Boxplot da diferença entre '{nome_inicial}' e '{nome_final}'",
        yaxis_title="Dias",
        xaxis_title="",
        showlegend=False,
        height=500,
        font=dict(family="Arial", size=14),
        margin=dict(l=40, r=40, t=60, b=40),
        plot_bgcolor="#fff",
        paper_bgcolor="#fff"
    )
    fig.add_hline(y=media, line_dash="dash", line_color="#0e5327", annotation_text=f"Média: {converter_dias_em_ymd(media)}", annotation_position="top left", annotation_font_color="#0e5327")
    fig.add_hline(y=mediana, line_dash="dot", line_color="#b8431f", annotation_text=f"Mediana: {converter_dias_em_ymd(mediana)}", annotation_position="bottom left", annotation_font_color="#b8431f")
    return fig
def montar_tabela_resumo(n_proc_validos, n_reus_validos, media, mediana, maximo, minimo, desvio_padrao, col_data_inicial=None, col_data_final=None):
    
    dados = [
        {"estatistica": "Nº de Processos (válidos)", "valor": str(n_proc_validos)},
        {"estatistica": "Nº de Réus (válidos)", "valor": str(n_reus_validos)},
        {"estatistica": "Média", "valor": converter_dias_em_ymd(media)},
        {"estatistica": "Mediana", "valor": converter_dias_em_ymd(mediana)},
        {"estatistica": "Máximo", "valor": converter_dias_em_ymd(maximo)},
        {"estatistica": "Mínimo", "valor": converter_dias_em_ymd(minimo)},
        {"estatistica": "Desvio Padrão", "valor": converter_dias_em_ymd(desvio_padrao)},
    ]
    return dados
def padronizar_nome(nome):
    if not nome:
        return ""
    chave = nome.strip().lower().replace(" ","").replace("á","a").replace("ã","a").replace("â","a").replace("é","e").replace("ê","e").replace("í","i").replace("ó","o").replace("ô","o").replace("ú","u").replace("ç","c")
    return NOME_PADRONIZADO.get(chave, NOME_PADRONIZADO.get(nome.strip().lower(), nome))
def gerar_grafico_donut(df, coluna):
    if not coluna or coluna not in df.columns:
        return go.Figure()
    dados = df[coluna].dropna()
    if dados.empty:
        return go.Figure()
    contagem = dados.value_counts()
    labels = contagem.index.tolist()
    valores = contagem.values.tolist()

    col_reu = 'P0Q1. Número de controle (dado pela equipe)'
    col_proc = 'P0Q2. Número do Processo:'
    # Cálculo de réus e processos únicos
    reus_validos = df.loc[dados.index, col_reu].unique()
    df_reus = df[df[col_reu].isin(reus_validos)]
    n_processos_unicos = df_reus[col_proc].nunique()
    n_reus = df_reus[col_reu].nunique()

    # Texto da legenda
    texto_legenda = (
        f"Processos únicos: {n_processos_unicos}<br>"
        f"Réus: {n_reus}"
    )

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=valores,
        hole=0.45,
        marker=dict(colors=px.colors.qualitative.Plotly),
        textinfo='percent+value',
        insidetextorientation='radial',
        sort=False
    )])
    fig.update_traces(
        textfont_size=14,
        pull=[0.02]*len(labels),
        hovertemplate='%{label}: %{percent} (%{value})<extra></extra>'
    )
    fig.update_layout(
        title=f"{coluna}",
        annotations=[
            dict(
                text=texto_legenda,
                x=0.5, y=0.02, showarrow=False,
                xref="paper", yref="paper",
                font=dict(size=13),
                align='left',
                bgcolor='white',
                bordercolor='gray',
                borderwidth=1,
                opacity=0.85
            )
        ],
        margin=dict(l=40, r=40, t=60, b=40),
        height=450,
        showlegend=True,
        legend_title_text="Resposta"
    )

    
    return fig

def layout():
    estados = list(ESTADOS.keys())
    colunas_data_options = [{"label": k, "value": v} for k, v in COLUNAS_DATA.items()]
    marcos_options = [{"label": k, "value": k} for k in COLUNAS_DATA.keys()]
    marcos_padrao = [
        'Crime',
        'Oferecimento da Denúncia',
        'Sentença de Júri',
        'Trânsito em julgado'
    ]
    return [
        html.H3("Estados", className="mb-3"),
        html.P("Visualize dados por estado."),
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    options=[{"label": estado, "value": estado} for estado in estados],
                    value="São Paulo",
                    clearable=False,
                    id="estado-dropdown-selection"
                ),
                md=3,
                sm=12,
            ),
            class_name="mt-1",
        ),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H4("-", id="estados-numero-processos", className="card-title"),
                        html.H6("Número de Processos", className="card-subtitle"),
                    ])
                ),
                className="mb-3",
                md=6,
                sm=12,
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H4("-", id="estados-numero-reus", className="card-title"),
                        html.H6("Número de Réus", className="card-subtitle"),
                    ])
                ),
                className="mb-3",
                md=6,
                sm=12,
            ),
        ], className="g-3"),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Linha do Tempo de Processamento - Geral", className="mb-3"),
                        dbc.Row([
                            dbc.Col([
                                html.Label("Métrica:"),
                                dcc.Dropdown(
                                    options=[
                                        {"label": "Média", "value": "media"},
                                        {"label": "Mediana", "value": "mediana"},
                                    ],
                                    value="media",
                                    id="estados-metrica-linha-tempo",
                                    clearable=False,
                                    style={"width": "100%"}
                                ),
                            ], md=4, sm=12),
                            dbc.Col([
                                html.Label("Marcos temporais:"),
                                dcc.Dropdown(
                                    options=marcos_options,
                                    value=marcos_padrao,
                                    id="estados-marcos-linha-tempo",
                                    multi=True,
                                    clearable=False,
                                    style={"width": "100%"}
                                ),
                            ], md=8, sm=12),
                        ], className="mb-3"),
                        dcc.Graph(id="estados-linha-tempo"),
                        html.Hr(),
                        html.H5("Linha do Tempo - Processo Específico", className="mb-3 mt-4"),
                        dbc.Row([
                            dbc.Col([
                                html.Label("Selecione o Processo:"),
                                dcc.Dropdown(
                                    id="estados-processo-individual-dropdown",
                                    options=[],  # será preenchido via callback
                                    value=None,
                                    clearable=False,
                                    style={"width": "100%"}
                                ),
                            ], md=6, sm=12),
                            dbc.Col([
                                html.Label("Selecione o Réu:"),
                                dcc.Dropdown(
                                    id="estados-reu-individual-dropdown",
                                    options=[],  # será preenchido via callback
                                    value=None,
                                    clearable=False,
                                    style={"width": "100%"}
                                ),
                            ], md=6, sm=12),
                        ], className="mb-2"),
                        dbc.Row([
                            dbc.Col([
                                html.Label("Marcos temporais:"),
                                dcc.Dropdown(
                                    id="estados-marcos-individual-dropdown",
                                    options=[{"label": k, "value": k} for k in COLUNAS_DATA.keys()],
                                    value=[k for k in list(COLUNAS_DATA.keys())[:4]],
                                    multi=True,
                                    clearable=False,
                                    style={"width": "100%"}
                                ),
                            ], md=12, sm=12),
                        ], className="mb-3"),
                        dcc.Graph(id="estados-linha-tempo-individual"),
                    ])
                ),
                md=12,
                sm=12,
            ),
        ], className="g-3"),
        html.Hr(),
        # Boxplot e Resumo Estatístico juntos em um mesmo CardBody
        dbc.Row([
            dbc.Col(
            dbc.Card(
                dbc.CardBody([
                html.H5("Boxplot da diferença entre datas e Resumo Estatístico", className="mb-3 mt-4"),
                dbc.Row([
                    dbc.Col(
                    [
                        html.Label("Data Inicial:"),
                        dcc.Dropdown(
                        options=colunas_data_options,
                        value=colunas_data_options[0]["value"] if colunas_data_options else None,
                        id="estados-data-inicial-dropdown",
                        clearable=False
                        ),
                    ],
                    md=6, sm=12
                    ),
                    dbc.Col(
                    [
                        html.Label("Data Final:"),
                        dcc.Dropdown(
                        options=colunas_data_options,
                        value=COLUNAS_DATA.get('Trânsito em julgado', colunas_data_options[1]["value"] if len(colunas_data_options) > 1 else (colunas_data_options[0]["value"] if colunas_data_options else None)),
                        id="estados-data-final-dropdown",
                        clearable=False
                        ),
                    ],
                    md=6, sm=12
                    ),
                ], className="mb-3"),
                dbc.Row([
                    dbc.Col(
                    dcc.Graph(id="estados-boxplot-inquerito"),
                    md=8, sm=12
                    ),
                    dbc.Col(
                    dash_table.DataTable(
                        id="estados-tabela-estatisticas",
                        columns=[{"name": "Estatística", "id": "estatistica"}, {"name": "Valor", "id": "valor"}],
                        data=[],
                        style_cell={
                            "textAlign": "center",
                            "fontSize": 15,
                            "minWidth": "60px",
                            "maxWidth": "90px",
                            "width": "70px",
                            "whiteSpace": "normal",
                            "height": "40px",         # aumenta a altura da célula
                            "lineHeight": "2",      # aumenta o espaçamento vertical do texto
                            "padding": "12px 4px",    # aumenta o padding vertical
                        },
                        style_header={
                            "backgroundColor": "#b8431f",
                            "color": "white",
                            "fontWeight": "bold"
                        },
                        style_data_conditional=[
                            {"if": {"row_index": "odd"}, "backgroundColor": "#fef9f9"},
                            {"if": {"row_index": "even"}, "backgroundColor": "#ffffff"},
                        ],
                        style_table={
                            "height": "500px",  # igual ao boxplot
                            "overflowY": "auto"
                        },
                        fill_width=True,
                    ),
                    md=4, sm=12
                    ),
                ], className="g-3"),
                ]),
            ),
            md=12, sm=12,
            ),
        ], className="g-3"),
        html.Hr(),
        dbc.Row(
            [
            dbc.Col(
                dbc.Card(
                dbc.CardBody([
                    html.H5("Distribuição - Atuação Policial/Pericial", className="mb-3"),
                    html.Label("Selecione a coluna:"),
                    dcc.Dropdown(
                    id="estados-coluna-multiescolha-dropdown",
                    options=[{"label": k, "value": v} for k, v in COLUNAS_DONUT.items()],
                    value=list(COLUNAS_DONUT.values())[0],
                    clearable=False,
                    style={"width": "100%"}
                    ),
                    dcc.Graph(id="estados-grafico-donut-multiescolha"),
                ])
                ),
                md=4, sm=12,
            ),
            dbc.Col(
                dbc.Card(
                dbc.CardBody([
                    html.H5("Distribuição - Atuação Ministério Público (MP)/Defesa", className="mb-3"),
                    html.Label("Selecione a coluna:"),
                    dcc.Dropdown(
                    id="estados-coluna-mp-dropdown",
                    options=[{"label": k, "value": v} for k, v in COLUNAS_DONUT_MP.items()],
                    value=list(COLUNAS_DONUT_MP.values())[0],
                    clearable=False,
                    style={"width": "100%"}
                    ),
                    dcc.Graph(id="estados-donut-mp"),
                ])
                ),
                md=4, sm=12,
            ),
            dbc.Col(
                dbc.Card(
                dbc.CardBody([
                    html.H5("Distribuição - Atuação Magistrados", className="mb-3"),
                    html.Label("Selecione a coluna:"),
                    dcc.Dropdown(
                    id="estados-coluna-juiz-dropdown",
                    options=[{"label": k, "value": v} for k, v in COLUNAS_DONUT_JUIZ.items()],
                    value=list(COLUNAS_DONUT_JUIZ.values())[0],
                    clearable=False,
                    style={"width": "100%"}
                    ),
                    dcc.Graph(id="estados-donut-juiz"),
                ])
                ),
                md=4, sm=12,
            ),
            ]
        ),
        html.Hr(), 
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Mudança de Motivação ao Longo do Processo", className="mb-3"),
                        dcc.Graph(id="grafico-sankey-motivacao"),
                    ])
                ),
                md=12, sm=12,
                className="d-none d-md-block", #esconde em telas pequenas 
            ),
            class_name="mb-4"
        ),
        html.Hr(),
        dbc.Row(
            [
            dbc.Col(
                dbc.Card(
                dbc.CardBody([
                    html.H5("Distribuição Geográfica do Local de Ocorrência do Crime", className="mb-3"),
                    html.Div(id="mapa-cidades-container", children=[
                        dcc.Graph(id="mapa-cidades"),
                    ]),
                ])
                ),
                md=12, sm=12,
            ),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
            dbc.Col(
                dbc.Card(
                dbc.CardBody([
                    html.H5("20 Cidades mais frequentes (Código IBGE)", className="mb-3"),
                    dcc.Graph(id="grafico-cidades"),  # gráfico de barras horizontal
                ])
                ),
                md=6, sm=12,
            ),
            dbc.Col(
                dbc.Card(
                dbc.CardBody([
                    html.H5("Tipos de Local do Crime", className="mb-3"),
                    dcc.Graph(id="grafico-local-crime"),  # gráfico de barras horizontal
                ])
                ),
                md=6, sm=12,
            ),
            ]
        )
      
    
    ]

# --- Callbacks ---

@callback(
    [
        Output("estados-numero-processos", "children"),
        Output("estados-numero-reus", "children"),
        Output("estados-linha-tempo", "figure"),
        Output("estados-boxplot-inquerito", "figure"),
        Output("estados-tabela-estatisticas", "data"),
    ],
    [
        Input("estado-dropdown-selection", "value"),
        Input("estados-metrica-linha-tempo", "value"),
        Input("estados-marcos-linha-tempo", "value"),
        Input("estados-data-inicial-dropdown", "value"),
        Input("estados-data-final-dropdown", "value"),
    ],
)

def update_estados_cards(estado, metrica_linha_tempo, marcos_linha_tempo, col_data_inicial, col_data_final):
    df = carregar_df_estado(estado)
    try:
        col_proc = next((col for col in df.columns if 'número do processo' in col.lower()), None)
        n_proc = df[col_proc].nunique() if col_proc else "-"
        col_reu = 'P0Q1. Número de controle (dado pela equipe)'
        n_reus = df[col_reu].nunique() if col_reu in df.columns else "-"

        # Linha do tempo geral
        colunas_data_filtradas = {k: COLUNAS_DATA[k] for k in marcos_linha_tempo if k in COLUNAS_DATA}
        eventos, dias_acumulados, metrica_utilizada = calcular_linha_tempo_acumulada(df, colunas_data_filtradas, metrica=metrica_linha_tempo)
        fig_linha_tempo = montar_linha_tempo(eventos, dias_acumulados, metrica_utilizada)


        # Boxplot e resumo
        fig_box = px.box()
        tabela_dados = []
        if col_data_inicial and col_data_final and col_data_inicial in df.columns and col_data_final in df.columns:
            df_validos, dados, n_proc_validos, n_reus_validos = calcular_diferenca_datas(df, col_data_inicial, col_data_final, col_proc, col_reu)
            if not dados.empty:
                media = dados.mean()
                mediana = dados.median()
                maximo = dados.max()
                minimo = dados.min()
                desvio_padrao = dados.std()
                fig_box = gerar_boxplot(df_validos, dados, col_data_inicial, col_data_final, media, mediana)
                tabela_dados = montar_tabela_resumo(n_proc_validos, n_reus_validos, media, mediana, maximo, minimo, desvio_padrao)
            else:
                fig_box.update_layout(title="Sem dados para boxplot", height=500)
        else:
            fig_box.update_layout(title="Selecione as colunas de data", height=500)

        return str(n_proc), str(n_reus), fig_linha_tempo, fig_box, tabela_dados
    except Exception as e:
        print("Erro no callback:", e)
        import plotly.graph_objects as go
        return "-", "-", go.Figure(), go.Figure(), []

@callback(
    [
        Output("estados-processo-individual-dropdown", "options"),
        Output("estados-processo-individual-dropdown", "value"),
    ],
    [Input("estado-dropdown-selection", "value")],
)
def atualizar_dropdown_processos(estado):
    df = carregar_df_estado(estado)
    col_proc = next((col for col in df.columns if 'número do processo' in col.lower()), None)
    if col_proc:
        processos = df[col_proc].dropna().unique()
        processos = sorted(processos, key=lambda x: str(x))
        #options = [{"label": str(p), "value": str(p)} for p in processos]
        options = [
            {"label": mascarar_numero_processo(str(p)), "value": str(p)}
            for p in processos
        ]
        value = options[0]["value"] if options else None
        return options, value
    return [], None

@callback(
    [
        Output("estados-reu-individual-dropdown", "options"),
        Output("estados-reu-individual-dropdown", "value"),
    ],
    [
        Input("estados-processo-individual-dropdown", "value"),
        Input("estado-dropdown-selection", "value")
    ],
)

def atualizar_dropdown_reus(processo, estado):
    df = carregar_df_estado(estado)
    col_proc = 'P0Q2. Número do Processo:'
    col_reu = 'P0Q1. Número de controle (dado pela equipe)'
    if col_proc and col_reu and processo:
        reus = df[df[col_proc].astype(str) == str(processo)][col_reu].dropna().unique()
        reus = sorted(reus, key=lambda x: str(x))
        options = [{"label": str(r), "value": str(r)} for r in reus]
        value = options[0]["value"] if options else None
        return options, value
    return [], None

@callback(
    Output("estados-linha-tempo-individual", "figure"),
    [
        Input("estados-processo-individual-dropdown", "value"),
        Input("estados-reu-individual-dropdown", "value"),
        Input("estados-marcos-individual-dropdown", "value"),
        Input("estado-dropdown-selection", "value"),
    ],
)

def atualizar_linha_tempo_individual(processo, reu, marcos, estado):
    df = carregar_df_estado(estado)
    col_proc = next((col for col in df.columns if 'número do processo' in col.lower()), None)
    col_reu = next((col for col in df.columns if 'número de controle' in col.lower() and 'equipe' in col.lower()), None)
    if not col_proc or not processo or not col_reu or not reu or not marcos:
        return go.Figure()
    df_proc = df[(df[col_proc].astype(str) == str(processo)) & (df[col_reu].astype(str) == str(reu))]
    if df_proc.empty:
        return go.Figure()
    eventos = [k for k in marcos if k in COLUNAS_DATA]
    datas = []
    for evento in eventos:
        col = COLUNAS_DATA[evento]
        if col in df_proc.columns:
            datas_validas = pd.to_datetime(df_proc[col], dayfirst=True, errors='coerce').dropna()
            valor = datas_validas.iloc[0] if not datas_validas.empty else pd.NaT
            datas.append(valor)
        else:
            datas.append(pd.NaT)
    if all(pd.isna(datas)):
        return go.Figure()
    idx_inicial = next((i for i, d in enumerate(datas) if not pd.isna(d)), 0)
    data_inicial = datas[idx_inicial]
    dias_acumulados = [(d - data_inicial).days if not pd.isna(d) and not pd.isna(data_inicial) else None for d in datas]
    import numpy as np
    eventos_validos = []
    dias_validos = []
    for evento, dias in zip(eventos, dias_acumulados):
        if dias is not None:
            eventos_validos.append(evento)
            dias_validos.append(dias)

    levels = np.tile([0.01, -0.01, 0.02, -0.02], int(np.ceil(len(eventos_validos)/6)))[:len(eventos_validos)]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dias_validos,
        y=[1]*len(dias_validos),
        mode="lines+markers",
        marker=dict(size=12, color="#d54d24", line=dict(width=2, color="#2c3e50")),
        line=dict(color="#d54d24", width=2),
        text=eventos_validos,
        hoverinfo="text+x"
    ))
    for idx, (x, evento, dias, level) in enumerate(zip(dias_validos, eventos_validos, dias_validos, levels)):
        texto_dias = "Marco Inicial" if idx == idx_inicial else (converter_dias_em_ymd(round(dias)) if dias is not None else "-")
        level_ajustado = 0.002 if idx == idx_inicial else level
        y_base = 1 + level_ajustado
        fig.add_shape(
            type="line",
            x0=x, x1=x,
            y0=1, y1=y_base,
            line=dict(color="darkgray", width=1),
            layer="below"
        )
        fig.add_annotation(x=x, y=y_base + (0.001 if level_ajustado > 0 else -0.001), text=evento, showarrow=False, font=dict(size=11))
        fig.add_annotation(x=x, y=y_base + (0.0028 if level_ajustado > 0 else -0.0028), text=texto_dias, showarrow=False, font=dict(size=10, color="gray"))

    # Nome do pesquisador responsável
    nome_pesquisador = None
    if 'P0Q0. Pesquisador responsável pelo preenchimento:' in df_proc.columns:
        nome_pesquisador = df_proc['P0Q0. Pesquisador responsável pelo preenchimento:'].dropna().astype(str).unique()
        nome_pesquisador = nome_pesquisador[0] if len(nome_pesquisador) > 0 else None
    nome_pesquisador_padrao = padronizar_nome(nome_pesquisador)
    agradecimento = f"Agradecimentos ao bolsista {nome_pesquisador_padrao} pela obtenção dos dados" if nome_pesquisador_padrao else ""
    fig.update_layout(
        title={
            'text': f"Linha do Tempo - Processo {mascarar_numero_processo(processo)} | Réu {reu}<br><span style='font-size:13px;color:#888'>{agradecimento}</span>",
            'y':0.92,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        yaxis=dict(visible=False),
        xaxis_title="Dias acumulados",
        margin=dict(l=40, r=40, t=80, b=40),
        height=350,
        plot_bgcolor="#fff",
        paper_bgcolor="#fff",
        font=dict(family="Arial", size=13),
    )
    return fig


@callback(
    Output("estados-grafico-donut-multiescolha", "figure"),
    [
        Input("estado-dropdown-selection", "value"),
        Input("estados-coluna-multiescolha-dropdown", "value"),
    ],
)

def atualizar_grafico_donut(estado, coluna_escolhida):
    df = carregar_df_estado(estado)
    
    if not coluna_escolhida or coluna_escolhida not in df.columns:
        return go.Figure()
    dados = df[coluna_escolhida].dropna()
    if dados.empty:
        return go.Figure()
    contagem = dados.value_counts()
    labels = contagem.index.tolist()
    valores = contagem.values.tolist()
    
    col_reu = 'P0Q1. Número de controle (dado pela equipe)'
    col_proc = 'P0Q2. Número do Processo:'
    # Cálculo de réus e processos únicos
    reus_validos = df.loc[dados.index, col_reu].unique()
    df_reus = df[df[col_reu].isin(reus_validos)]
    n_processos_unicos = df_reus[col_proc].nunique()
    n_reus = df_reus[col_reu].nunique()

    # Texto da legenda
    texto_legenda = (
        f"Processos únicos: {n_processos_unicos}<br>"
        f"Réus: {n_reus}"
    )

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=valores,
        hole=0.45,
        marker=dict(colors=['#950404FF', '#E04B28FF', '#C38961FF', '#9F5630FF', '#388F30FF', '#0F542FFF', '#007D82FF', '#004042FF']),
        textinfo='percent+value',
        insidetextorientation='radial',
        sort=False
    )])
    fig.update_traces(
        textfont_size=14,
        pull=[0.02]*len(labels),
        hovertemplate='%{label}: %{percent} (%{value})<extra></extra>'
    )
    # Se a coluna escolhida for um dos valores do dicionário COLUNAS_DONUT, use a chave como título
    titulo = next((k for k, v in COLUNAS_DONUT.items() if v == coluna_escolhida), coluna_escolhida)
    fig.update_layout(
        title=f"{titulo}",
        annotations=[
            dict(
                text=texto_legenda,
                x=0, y=0, showarrow=False,  # canto inferior esquerdo
                xref="paper", yref="paper",
                xanchor="left", yanchor="bottom",
                font=dict(size=13),
                align='right',
                bgcolor='white',
                bordercolor='gray',
                borderwidth=1,
                opacity=0.85
            )
        ],
        margin=dict(l=40, r=40, t=60, b=40),
        height=450,
        showlegend=True,
        legend_title_text="Resposta"
    )
    return fig



@callback(
    Output("estados-donut-mp", "figure"),
    [
        Input("estado-dropdown-selection", "value"),
        Input("estados-coluna-mp-dropdown", "value"),
    ],
)

def atualizar_grafico_donut_mp(estado, coluna_escolhida):
    df = carregar_df_estado(estado)
    # Encontre a chave correspondente ao value selecionado
    titulo = next((k for k, v in COLUNAS_DONUT_MP.items() if v == coluna_escolhida), coluna_escolhida)
    if not coluna_escolhida or coluna_escolhida not in df.columns:
        return go.Figure()
    dados = df[coluna_escolhida].dropna()
    if dados.empty:
        return go.Figure()
    contagem = dados.value_counts()
    labels = contagem.index.tolist()
    valores = contagem.values.tolist()

    col_reu = 'P0Q1. Número de controle (dado pela equipe)'
    col_proc = 'P0Q2. Número do Processo:'
    # Cálculo de réus e processos únicos
    reus_validos = df.loc[dados.index, col_reu].unique()
    df_reus = df[df[col_reu].isin(reus_validos)]
    n_processos_unicos = df_reus[col_proc].nunique()
    n_reus = df_reus[col_reu].nunique()

    # Texto da legenda
    texto_legenda = (
        f"Processos únicos: {n_processos_unicos}<br>"
        f"Réus: {n_reus}"
    )

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=valores,
        hole=0.45,
        marker=dict(colors=['#950404FF', '#E04B28FF', '#C38961FF', '#9F5630FF', '#388F30FF', '#0F542FFF', '#007D82FF', '#004042FF']),
        textinfo='percent+value',
        insidetextorientation='radial',
        sort=False
    )])
    fig.update_traces(
        textfont_size=14,
        pull=[0.02]*len(labels),
        hovertemplate='%{label}: %{percent} (%{value})<extra></extra>'
    )
    fig.update_layout(
        title=titulo,
        margin=dict(l=40, r=40, t=60, b=40),
        annotations=[
            dict(
                text=texto_legenda,
                x=0, y=0, showarrow=False,  # canto inferior esquerdo
                xref="paper", yref="paper",
                xanchor="left", yanchor="bottom",
                font=dict(size=13),
                align='right',
                bgcolor='white',
                bordercolor='gray',
                borderwidth=1,
                opacity=0.85
            )
        ],
        showlegend=True,
        height=450,
        legend_title_text="Resposta"
    )
    return fig


@callback(
    Output("estados-donut-juiz", "figure"),
    [
        Input("estado-dropdown-selection", "value"),
        Input("estados-coluna-juiz-dropdown", "value"),
    ],
)

def atualizar_grafico_donut_juiz(estado, coluna_escolhida):
    df = carregar_df_estado(estado)
    # Encontre a chave correspondente ao value selecionado
    titulo = next((k for k, v in COLUNAS_DONUT_JUIZ.items() if v == coluna_escolhida), coluna_escolhida)
    if not coluna_escolhida or coluna_escolhida not in df.columns:
        return go.Figure()
    dados = df[coluna_escolhida].dropna()
    if dados.empty:
        return go.Figure()
    contagem = dados.value_counts()
    labels = contagem.index.tolist()
    valores = contagem.values.tolist()

    col_reu = 'P0Q1. Número de controle (dado pela equipe)'
    col_proc = 'P0Q2. Número do Processo:'
    # Cálculo de réus e processos únicos
    reus_validos = df.loc[dados.index, col_reu].unique()
    df_reus = df[df[col_reu].isin(reus_validos)]
    n_processos_unicos = df_reus[col_proc].nunique()
    n_reus = df_reus[col_reu].nunique()

    # Texto da legenda
    texto_legenda = (
        f"Processos únicos: {n_processos_unicos}<br>"
        f"Réus: {n_reus}"
    )
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=valores,
        hole=0.45,
        marker=dict(colors=['#950404FF', '#E04B28FF', '#C38961FF', '#9F5630FF', '#388F30FF', '#0F542FFF', '#007D82FF', '#004042FF']),
        textinfo='percent+value',
        insidetextorientation='radial',
        sort=False
    )])
    fig.update_traces(
        textfont_size=14,
        pull=[0.02]*len(labels),
        hovertemplate='%{label}: %{percent} (%{value})<extra></extra>'
    )
    fig.update_layout(
        title=titulo,
        margin=dict(l=40, r=40, t=60, b=40),
        annotations=[
            dict(
                text=texto_legenda,
                x=0, y=0, showarrow=False,  # canto inferior esquerdo
                xref="paper", yref="paper",
                xanchor="left", yanchor="bottom",
                font=dict(size=13),
                align='right',
                bgcolor='white',
                bordercolor='gray',
                borderwidth=1,
                opacity=0.85
            )
        ],
        showlegend=True,
        height=430,
        legend_title_text="Resposta"
    )
    return fig

@callback(
    Output("mapa-cidades", "figure"),
    Input("estado-dropdown-selection", "value"),
)



def atualizar_mapa_cidades(estado):
    df = carregar_df_estado(estado)
    # Busca a sigla do estado no dicionário
    sigla = ESTADOS.get(estado)
    if not sigla:
        return go.Figure()


    # Filtrar o GeoDataFrame pelo estado selecionado
    gdf_estado = gdf_brasil[gdf_brasil["SIGLA_UF"] == sigla]
    
    # Converter para GeoJSON
    estado_geojson = gdf_estado.__geo_interface__

    # Crie colunas auxiliares com nomes amigáveis
    df["Número Processo"] = df["P0Q2. Número do Processo:"].apply(lambda x: mascarar_numero_processo(str(x)) if isinstance(x, str) else x)
    df["Nome Cidade"] = df["nome_cidade"]
    df["Comarca"] = df['P0Q5. Comarca responsável pelo processo:'].apply(lambda x: x.title() if isinstance(x, str) else x)

    fig = px.scatter_mapbox(
        df,
        lat='latitude',
        lon='longitude',
        hover_name='Nome Cidade',
        hover_data={
            'P0Q1. Número de controle (dado pela equipe)': False,
            "Número Processo": True,
            'Nome Cidade': True,
            'Comarca': True,
            'latitude': False,
            'longitude': False
        },
        color_discrete_sequence=['#b8431f'],
        zoom=4,  # ajuste o zoom conforme necessário
        height=700
    )

    # Adiciona o contorno do estado
    for feature in estado_geojson['features']:
        coords = feature['geometry']['coordinates']
        if feature['geometry']['type'] == 'Polygon':
            polygons = [coords]
        else:  # MultiPolygon
            polygons = coords
        for poly in polygons:
            lons, lats = zip(*poly[0])
            fig.add_trace(go.Scattermapbox(
                lon=lons,
                lat=lats,
                mode='lines',
                line=dict(width=2, color='black'),
                name='Contorno do Estado',
                showlegend=False
            ))
    
    lat_center = df['latitude'].mean()
    lon_center = df['longitude'].mean()


    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox=dict(
        center=dict(lat=lat_center, lon=lon_center),
        zoom=5.5  # Zoom
        ),
        margin={"r":0,"t":40,"l":0,"b":0},
        title=f"Cidades de ocorrência do crime - {sigla}"
    )

    return fig


@callback(
    Output("grafico-cidades", "figure"),
    Input("estado-dropdown-selection", "value"),
)

def atualizar_grafico_cidades(estado):
    df = carregar_df_estado(estado)
    top_cidades = (
        df['nome_cidade']
        .str.title()
        .value_counts()
        .head(20)
    )
    top_cidades = top_cidades.sort_values()

    # Parâmetros de cor (exemplo, ajuste conforme sua paleta)
    abbott_palette = ['#137136', '#d54d24']  


    # Gráfico de barras horizontal com Plotly
    fig_cidades = go.Figure(go.Bar(
        x=top_cidades.values,
        y=top_cidades.index,
        orientation='h',
        marker=dict(
            color=[abbott_palette[0] if i % 2 == 0 else abbott_palette[1] for i in range(len(top_cidades))]
        ),
        text=top_cidades.values,
        textposition='outside',
        insidetextanchor='start',
        hovertemplate='<b>%{y}</b><br>Ocorrências: %{x}<extra></extra>'
    ))

    fig_cidades.update_layout(
        #title='20 Cidades mais frequentes (Código IBGE)',
        xaxis_title='Número de Ocorrências',
        yaxis_title='',
        yaxis=dict(tickmode='array', tickvals=top_cidades.index, ticktext=top_cidades.index),
        margin=dict(l=10, r=10, t=50, b=10),
        height=500,
        plot_bgcolor='white',
        showlegend=False
    )
    fig_cidades.update_xaxes(showgrid=False)
    fig_cidades.update_yaxes(showgrid=False)

    return fig_cidades

@callback(
    Output("grafico-local-crime", "figure"),
    Input("estado-dropdown-selection", "value"),
)
def atualizar_grafico_local_crime(estado):
    df = carregar_df_estado(estado)
    # --- Lógica para contagem dos tipos de local do crime ---
    dict_colunas = {
        'P3Q8[SQ001]': 'Via pública/praça/parque',
        'P3Q8[SQ002]': 'Cena de uso de drogas',
        'P3Q8[SQ003]': 'Residência do Acusado',
        'P3Q8[SQ004]': 'Residência da Vítima',
        'P3Q8[SQ005]': 'Estabelecimento de Ensino',
        'P3Q8[SQ006]': 'Estabelecimento Hospitalar',
        'P3Q8[SQ007]': 'Estabelecimento Comercial',
        'P3Q8[SQ008]': 'Estabelecimento prisional',
        'P3Q8[SQ009]': 'Unidade para medida de segurança',
        'P3Q8[SQ010]': 'Sedes socio-culturais',
        'P3Q8[SQ011]': 'Serviços de reinserção social',
        'P3Q8[SQ012]': 'Local de trabalho',
        'P3Q8[SQ013]': 'Local para lazer',
        'P3Q8[SQ014]': 'Unidades Policiais',
        'P3Q8[SQ015]': 'Sem informação',
        'P3Q8[other]': 'Outros'
    }

    # Lógica para as residências
    resid_acusado = (df['P3Q8[SQ003]'] == 'Sim')
    resid_vitima = (df['P3Q8[SQ004]'] == 'Sim')
    residencia_comum = resid_acusado & resid_vitima
    residencia_acusado = resid_acusado & ~resid_vitima
    residencia_vitima = resid_vitima & ~resid_acusado

    contagem = {}
    for col, nome in dict_colunas.items():
        if col in ['P3Q8[SQ003]', 'P3Q8[SQ004]']:
            continue
        elif col == 'P3Q8[other]':
            contagem[nome] = df[col].notnull() & (df[col].astype(str).str.strip() != '')
            contagem[nome] = contagem[nome].sum()
        else:
            contagem[nome] = (df[col] == 'Sim').sum()

    contagem['Residência comum'] = residencia_comum.sum()
    contagem['Residência do Acusado'] = residencia_acusado.sum()
    contagem['Residência da Vítima'] = residencia_vitima.sum()

    contagem = {k: v for k, v in sorted(contagem.items(), key=lambda item: item[1], reverse=True)}
    contagem = {k: v for k, v in contagem.items() if v > 0}

    labels_local = list(contagem.keys())
    valores_local = list(contagem.values())
    abbott_palette = ['#137136', '#d54d24', '#c38961', '#9f5630', '#388f30', '#0f542f', '#007d82', '#004042']
    cores_local = abbott_palette[:len(labels_local)]

    fig_local = go.Figure(go.Bar(
        x=valores_local,
        y=labels_local,
        orientation='h',
        marker=dict(color=cores_local),
        text=valores_local,
        textposition='outside',
        insidetextanchor='start',
        hovertemplate='<b>%{y}</b><br>Ocorrências: %{x}<extra></extra>'
    ))

    fig_local.update_layout(
        xaxis_title='Ocorrências',
        yaxis_title='',
        margin=dict(l=10, r=10, t=50, b=10),
        height=500,
        plot_bgcolor='white',
        showlegend=False
    )
    fig_local.update_xaxes(showgrid=False)
    fig_local.update_yaxes(showgrid=False)

    return fig_local

@callback(
    Output("grafico-sankey-motivacao", "figure"),
    Input("estado-dropdown-selection", "value"),
)

def gerar_sankey_motivacao(estado):
    df = carregar_df_estado(estado)

    cols = [
        'P3Q27. Qual foi o motivo identificado para o homicídio ou tentativa de homicídio, segundo o relatório do delegado?',
        'P4Q11. Qual foi o motivo identificado para o homicídio ou tentativa de homicídio, segundo a denúncia?',
        'P7Q23. Qual foi o motivo identificado para o homicídio ou tentativa de homicídio, segundo a pronúncia?',
        'P8Q34. Qual foi o motivo identificado para o homicídio ou tentativa de homicídio, segundo a condenação?'
    ]
    alternativas = [
        "Violência doméstica, mas somente relação conjugal (parceiros; marido e mulher; amantes e ex-parceiros)",
        "Violência doméstica - outras situações (contra ascendentes, descendentes, e outros parentes)",
        "Briga entre amigos/conhecidos (com exceção de casos amorosos)",
        "Briga entre desconhecidos",
        "Envolvimento com o tráfico de drogas ou organizações criminosas",
        "Roubo ou tentativa de roubo",
        "Crimes motivados por discriminação (por exemplo, homofobia, racismo)",
        "Ato decorrente de intervenção policial",
        "Sem informação"
    ]
    def normaliza(s):
        if pd.isna(s):
            return ""
        s = str(s).strip().lower()
        s = " ".join(s.split())
        s = unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('ASCII')
        return s
    alternativas_norm = {normaliza(alt): alt for alt in alternativas}
    def padroniza_motivo(valor):
        if pd.isna(valor) or str(valor).strip() == "" or str(valor).strip() == "51":
            return "Sem informação"
        valor_norm = normaliza(valor)
        if valor_norm in alternativas_norm:
            return alternativas_norm[valor_norm]
        return "Outros"
    labels_curto_dict = {
        "Violência doméstica, mas somente relação conjugal (parceiros; marido e mulher; amantes e ex-parceiros)": "Doméstica (Conjugal)",
        "Violência doméstica - outras situações (contra ascendentes, descendentes, e outros parentes)": "Doméstica (Familiar)",
        "Briga entre amigos/conhecidos (com exceção de casos amorosos)": "Briga amigos/conhecidos",
        "Briga entre desconhecidos": "Briga desconhecidos",
        "Envolvimento com o tráfico de drogas ou organizações criminosas": "Tráfico/Org. Crim.",
        "Roubo ou tentativa de roubo": "Roubo/tent. roubo",
        "Crimes motivados por discriminação (por exemplo, homofobia, racismo)": "Discriminação",
        "Ato decorrente de intervenção policial": "Interv. policial",
        "Sem informação": "Sem informação",
        "Outros": "Outros"
    }
    df_sankey = df[cols].copy()
    for c in cols:
        df_sankey[c] = df_sankey[c].apply(padroniza_motivo)
    motivos = alternativas.copy()
    if any(df_sankey[c].eq("Outros").any() for c in cols):
        motivos.append("Outros")
    etapas = ['Polícia', 'Denúncia', 'Pronúncia', 'Condenação']
    node_labels = []
    for etapa in etapas:
        node_labels += [labels_curto_dict[m] for m in motivos]
    node_idx = {(motivo, etapa): i*len(motivos)+j for i, etapa in enumerate(etapas) for j, motivo in enumerate(motivos)}
    source, target, value = [], [], []
    for i in range(len(cols)-1):
        c1, c2 = cols[i], cols[i+1]
        fluxos = df_sankey.groupby([c1, c2]).size().reset_index(name='count')
        for _, row in fluxos.iterrows():
            source.append(node_idx[(row[c1], etapas[i])])
            target.append(node_idx[(row[c2], etapas[i+1])])
            value.append(row['count'])

    node_colors = (
        ['#d54d24', '#137136', '#c38961', '#9f5630', '#388f30', '#0f542f', '#007d82', '#004042', '#b8431f', '#888888'] * len(etapas)
    )[:len(node_labels)]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=node_labels,
            color=node_colors
        ),
        link=dict(
            source=source,
            target=target,
            value=value
        ))])
    fig.update_layout(
        title_text=" ",
        font_size=12,
        height=800,
        autosize=True,
        width=None,
        margin=dict(l=40, r=40, t=60, b=40)
    )

    # Adiciona o nome das etapas acima de cada grupo de barras, mais espaçados
    num_motivos = len(motivos)
    total_nodes = len(etapas) * num_motivos
    for i, etapa in enumerate(etapas):
        # Espaçamento proporcional ao número de etapas, com maior afastamento
        # Use um fator de espaçamento maior para separar mais
        x = (i + 0.005) / len(etapas)
        # Ajuste para afastar mais: use um fator de 1.2 no denominador
        x_espacado = (i) / (len(etapas) * 0.98) + (i / len(etapas)) * 0.34
        fig.add_annotation(
            x=x_espacado,
            y=1.07,
            text=f"{etapa}",
            showarrow=False,
            xref="paper",
            yref="paper",
            font=dict(size=14, color="#222"),
            align="center"
        )

    return fig
