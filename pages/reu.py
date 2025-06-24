import dash
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
from dash import Input, Output, callback, dcc, html
from caching import retrieve_data
import plotly.graph_objects as go
import plotly.express as px


from utils import TITLE

def carregar_df_estado(estado):
    if estado == "Minas Gerais":
        return pd.read_csv("data/TJMG/df_reu_22.06.2025_TJMG.csv")
    else:
        return pd.read_csv("data/TJSP/df_reu_17.06.2025_TJSP.csv")


PAGE_TITLE = "Réu"

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", order=2)

ESTADOS = {"São Paulo": "SP",
        "Minas Gerais": "MG"}  # Adicione outros estados conforme necessário


COLUNAS_DONUT = {
    "Sexo de nascimento": "P1Q7. Sexo de nascimento:",
    "Identificação como Minoria Sexual": "P1Q9. O réu é identificado no Boletim de Ocorrência/REDS como transexual, travesti, homossexual ou bissexual?",
    "Estado Civil": 'P1Q10. Qual a situação conjugal/estado civil do réu informado no auto de qualificação policial?', 
    "Cor/Raça": 'P1Q11. Qual é a cor/raça informada no Boletim de Ocorrência/REDS?', 
    "Nível de escolaridade": "P1Q12. Qual o nível de escolaridade do réu informado no auto de qualificação ou, caso não haja a informação no auto de qualificação, no interrogatório policial?",   
}

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
    col_proc = 'P0Q2. Número do Processo (Formato: 0000000-00.0000.0.00.0000):'
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
        showlegend=True,
        legend_title_text="Resposta"
    )

def layout():
    estados = list(ESTADOS.keys())
    return [
        html.H3("Réu", className="mb-3"),
        html.P(
            """
            Essa página fornece uma visão geral do réu, destacando informações relevantes sobre seu perfil e histórico.
            """
        ),
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
        dbc.Row(
            [
            dbc.Col(
                dbc.Card(
                dbc.CardBody([
                    html.H5("Informações Gerais sobre o Réu", className="mb-3"),
                    html.Label("Selecione a coluna:"),
                    dcc.Dropdown(
                    id="reu-coluna-multiescolha-dropdown",
                    options=[{"label": k, "value": v} for k, v in COLUNAS_DONUT.items()],
                    value=list(COLUNAS_DONUT.values())[0],
                    clearable=False,
                    style={"width": "100%"}
                    ),
                    dcc.Graph(id="reu-grafico-donut-multiescolha"),
                    ]),
                    ),
                md=6, sm=12,
                 ), 
            
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.H5("Profissões do Réu", className="mb-3"),
                            dcc.Graph(id="reu-grafico-profissoes"),
                        ]),
                    ),
                    md=6, sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.H5("Faixa de Renda do Réu", className="mb-3"),
                            dcc.Graph(id="reu-grafico-faixa-renda"),
                        ]),
                    ),
                    md=6, sm=12,
                ),
            ],
            class_name="mt-4",
        ),
    ]

@callback(
    Output("reu-grafico-donut-multiescolha", "figure"),
    [
        Input("estado-dropdown-selection", "value"),
        Input("reu-coluna-multiescolha-dropdown", "value"),
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
    col_proc = 'P0Q2. Número do Processo (Formato: 0000000-00.0000.0.00.0000):'
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
        showlegend=True,
        legend_title_text="Resposta"
    )
    return fig

# Callback para o gráfico de profissões
@callback(
    Output("reu-grafico-profissoes", "figure"),
    Input("estado-dropdown-selection", "value"),
)
def atualizar_grafico_profissoes(estado):
    df = carregar_df_estado(estado)
    dict_colunas = {
        'P1Q13[SQ001]': 'Desempregado',
        'P1Q13[SQ002]': 'Estudante',
        'P1Q13[SQ003]': 'Trabalho Formal',
        'P1Q13[SQ004]': 'Aposentado',
        'P1Q13[SQ005]': 'Sem informação'
    }
    contagem = {}
    for col, nome in dict_colunas.items():
        if col in df.columns:
            contagem[nome] = (df[col] == 'Sim').sum()
        else:
            contagem[nome] = 0

    contagem = {k: v for k, v in sorted(contagem.items(), key=lambda item: item[1], reverse=True)}
    labels = list(contagem.keys())
    valores = list(contagem.values())
    total = sum(valores)
    # Paleta de cores (ajuste se quiser)
    cores = ['#950404', '#E04B28', '#C38961', '#388F30', '#007D82']

    fig = go.Figure(go.Bar(
        x=valores,
        y=labels,
        orientation='h',
        marker_color=cores[:len(labels)],
        text=[f"{v} ({(v/total*100):.1f}%)" if total > 0 else "0 (0%)" for v in valores],
        textposition='outside',
    ))
    fig.update_layout(
        title=f"Profissões do Réu - {estado} - Formulário de Réu",
        xaxis_title="Ocorrências",
        yaxis_title="",
        margin=dict(l=40, r=40, t=60, b=40),
        height=430,
        plot_bgcolor='white',
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(200,200,200,0.15)')
    fig.update_yaxes(showgrid=False)
    return fig

# Callback para faixa de renda 

@callback(
    Output("reu-grafico-faixa-renda", "figure"),
    Input("estado-dropdown-selection", "value"),
)
def atualizar_grafico_faixa_renda(estado):
    df = carregar_df_estado(estado)
    col = 'P1Q14. Qual é a renda/salário/remuneração/rendimentos mensais do réu, informada no auto de qualificação/interrogatório policial?'

    def classificar_faixa_renda(valor):
        if pd.isna(valor) or valor == 'NI':
            return 'NI'
        try:
            v = float(str(valor).replace('.', '').replace(',', '.'))
        except:
            return 'Outro'
        if v <= 1000:
            return 'Até 1 mil'
        elif 1000 < v <= 2000:
            return 'Entre 1 e 2 mil'
        elif 2000 < v <= 5000:
            return 'Entre 2 e 5 mil'
        elif 5000 < v <= 10000:
            return 'Acima de 5 mil'
        elif 10000 < v <= 20000:
            return 'Acima de 10 mil'
        elif v > 20000:
            return 'Acima de 20 mil'
        else:
            return 'Outro'

    if col not in df.columns:
        return go.Figure()
    df['faixa_renda'] = df[col].apply(classificar_faixa_renda)
    ordem = ['NI', 'Até 1 mil', 'Entre 1 e 2 mil', 'Entre 2 e 5 mil', 'Acima de 5 mil', 'Acima de 10 mil', 'Acima de 20 mil', 'Outro']
    contagem = df['faixa_renda'].value_counts().reindex(ordem, fill_value=0)
    total = contagem.sum()

    fig = go.Figure(go.Bar(
        x=contagem.index,
        y=contagem.values,
        marker_color=['#950404', '#E04B28', '#C38961', '#388F30', '#007D82'][:len(contagem)],
        text=[f"{v} ({(v/total*100):.1f}%)" if total > 0 else "0 (0%)" for v in contagem.values],
        textposition='outside',
    ))
    fig.update_layout(
        title=f"Faixas de renda mensal do réu - {estado}",
        xaxis_title="Faixa de renda",
        yaxis_title="Número de réus",
        margin=dict(l=40, r=40, t=60, b=40),
        height=430,
        plot_bgcolor='white',
    )
    fig.update_xaxes(tickangle=30)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(200,200,200,0.15)')
    return fig