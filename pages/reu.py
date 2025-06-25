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
        return pd.read_csv("data/TJMG/df_reu_TJMG.csv")
    else:
        return pd.read_csv("data/TJSP/df_reu_TJSP.csv")


PAGE_TITLE = "Réu"

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", order=2)

# Paleta de cores (ajuste se quiser)
CORES_GRAFICOS = ['#950404', '#E04B28', '#C38961', '#388F30', '#007D82']

ESTADOS = {"São Paulo": "SP",
        "Minas Gerais": "MG"}  # Adicione outros estados conforme necessário


COLUNAS_DONUT = {
    "Sexo de nascimento": "P1Q7. Sexo de nascimento:",
    "Identificação como Minoria Sexual": "P1Q9. O réu é identificado no Boletim de Ocorrência/REDS como transexual, travesti, homossexual ou bissexual?",
    "Estado Civil": 'P1Q10. Qual a situação conjugal/estado civil do réu informado no auto de qualificação policial?', 
    "Cor/Raça": 'P1Q11. Qual é a cor/raça informada no Boletim de Ocorrência/REDS?', 
    "Nível de escolaridade": "P1Q12. Qual o nível de escolaridade do réu informado no auto de qualificação ou, caso não haja a informação no auto de qualificação, no interrogatório policial?",   
}
COLUNAS_DONUT_ANTECEDENTES = {
    "Antecedentes Criminais": "P1Q22. O réu possui antecedentes criminais/passagens (considerando registros de BOs, processos, condenações sem trânsito em julgado, atos infracionais, entre outros) pelo sistema de justiça e segurança pública?"
   
}

COLUNAS_DONUT_RELACAO = {
    "Relação entre Réu e Vítima": 'P1Q16. Há relação de parentesco/relação íntima entre réu e vítima?'
}

CAUSAS_RELACAO = {
    'P1Q17[SQ002]': 'Pai/Mãe',
    'P1Q17[SQ003]': 'Filho(a)',
    'P1Q17[SQ004]': 'Padrasto/madrasta/enteado(a)',
    'P1Q17[SQ005]': 'Casamento/União Estável',
    'P1Q17[SQ006]': 'Irmãos',
    'P1Q17[SQ007]': 'Relacionamento íntimo afetivo',
    'P1Q17[SQ008]': 'Primos',
    'P1Q17[SQ009]': 'Tio/Sobrinho',
    'P1Q17[SQ010]': 'Sogro/genro',
    'P1Q17[SQ011]': 'Cunhado',
    'P1Q17[SQ012]': 'Amigos',
    'P1Q17[SQ013]': 'Divorciados/ex-companheiros',
    'P1Q17[SQ014]': 'Outra relação de parentesco',
    'P1Q17[SQ015]': 'Sem informação'
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
        marker=dict(colors=CORES_GRAFICOS[:len(labels)]),
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
            dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.H5("Boxplot da Idade na Data do Crime", className="mb-3"),
                            dcc.Graph(id="reu-boxplot-idade"),
                        ])
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
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.H5("Antecedentes Criminais", className="mb-3"),
                            dcc.Graph(id="grafico-donut-antecedentes"),
                        ]),
                    ),
                    md=6, sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.H5("Legislações Penais Relacionadas aos Antecedentes", className="mb-3"),
                            dcc.Graph(id="grafico-bar-legislacoes-antecedentes"),
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
                            html.H5("Relação entre Réu e Vítima", className="mb-3"),
                            dcc.Graph(id="grafico-donut-relacao"),
                        ]),
                    ),
                    md=6, sm=12,
                ),
                dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Tipo de Relação entre Réu e Vítima", className="mb-3"),
                        dcc.Graph(id="grafico-bar-tipo-relacao"),
                    ]),
                ),
                md=6, sm=12,
                ),    
            ]
        ),
    ]

#call back para donuts multiescolha
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
        marker=dict(colors=CORES_GRAFICOS[:len(labels)]),
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
        height=450,
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

    fig = go.Figure(go.Bar(
        x=valores,
        y=labels,
        orientation='h',
        marker_color=CORES_GRAFICOS[:len(labels)],
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

# Callback para o  gráfico donut existência de antecedente

@callback(
    Output("grafico-donut-antecedentes", "figure"),
    Input("estado-dropdown-selection", "value"),
)

def atualizar_grafico_donut_antecedentes(estado):
    df = carregar_df_estado(estado)
    # Pegue a coluna diretamente do dicionário
    coluna_escolhida = list(COLUNAS_DONUT_ANTECEDENTES.values())[0]
    if not coluna_escolhida or coluna_escolhida not in df.columns:
        return go.Figure()
    dados = df[coluna_escolhida].dropna()
    if dados.empty:
        return go.Figure()
    contagem = dados.value_counts()
    labels = contagem.index.tolist()
    valores = contagem.values.tolist()

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=valores,
        hole=0.45,
        marker=dict(colors=CORES_GRAFICOS[:len(labels)]),
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
        title="Antecedentes Criminais do Réu",
        margin=dict(l=40, r=40, t=60, b=40),
        showlegend=True,
        height=430,
        legend_title_text="Resposta"
    )
    return fig

# Callback para o gráfico de legislações penais relacionadas aos antecedentes
@callback(
    Output("grafico-bar-legislacoes-antecedentes", "figure"),
    Input("estado-dropdown-selection", "value"),
)
def atualizar_grafico_legislacoes_antecedentes(estado):
    df = carregar_df_estado(estado)
    dict_colunas = {
        'P1Q23[SQ001]': 'Lei de Drogas',
        'P1Q23[SQ002]': 'Código Penal Militar',
        'P1Q23[SQ003]': 'Código Penal',
        'P1Q23[SQ004]': 'Lei de Org. Criminos',
        'P1Q23[SQ005]': 'Lei Sis. Nacional de Armas',
        'P1Q23[SQ006]': 'Cód. de Trânsito Brasileiro',
        'P1Q23[SQ007]': 'Estatuto da Criança e Adolescente (ECA)',
        'P1Q23[SQ008]': 'Estatuto do Idoso',
        'P1Q23[SQ009]': 'Lei de abuso de Autoridade',
        'P1Q23[SQ010]': 'Contravenções Penais',
        'P1Q23[SQ011]': 'Crime contra o Meio Ambiente',
        'P1Q23[SQ012]': 'Crimes contra o sistema financeiro Nacional',
        'P1Q23[SQ013]': 'Lei Maria da Penha',
        'P1Q23[SQ014]': 'Lei de Terrorismo',
        'P1Q23[SQ015]': 'Estatuto da Pessoa com Deficiência',
        'P1Q23[SQ016]': 'Sem informação',
    }
    contagem = {}
    for col, nome in dict_colunas.items():
        if col in df.columns:
            contagem[nome] = (df[col] == 'Sim').sum()
        else:
            contagem[nome] = 0

    # Remove categorias com 0 ocorrências
    contagem = {k: v for k, v in contagem.items() if v > 0}
    # Ordena para visualização
    contagem = {k: v for k, v in sorted(contagem.items(), key=lambda item: item[1], reverse=True)}

    labels = list(contagem.keys())
    valores = list(contagem.values())
    total = sum(valores)
    cores = CORES_GRAFICOS * (len(labels) // len(CORES_GRAFICOS) + 1)

    fig = go.Figure(go.Bar(
        x=valores,
        y=labels,
        orientation='h',
        marker_color=cores[:len(labels)],
        text=[f"{v} ({(v/total*100):.1f}%)" if total > 0 else "0 (0%)" for v in valores],
        textposition='outside',
    ))
    fig.update_layout(
        title=f'Legislações Penais relacionadas aos Antecedentes Penais do Réu<br>{estado} - Formulário de Réu',
        xaxis_title='Ocorrências',
        yaxis_title='',
        margin=dict(l=40, r=40, t=60, b=40),
        height=430,
        plot_bgcolor='white',
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(200,200,200,0.15)')
    fig.update_yaxes(showgrid=False)
    return fig

#Callback para o boxplot da idade na data do crime

@callback(
    Output("reu-boxplot-idade", "figure"),
    Input("estado-dropdown-selection", "value"),
)
def atualizar_boxplot_idade(estado):
    df = carregar_df_estado(estado)
    col = 'Idade na data do crime'
    if col not in df.columns:
        return go.Figure()
    # Remove valores nulos e não numéricos
    df_valida = df[pd.to_numeric(df[col], errors='coerce').notnull()]
    if df_valida.empty:
        return go.Figure()
    
    y = df_valida[col].astype(float)

    media = y.mean()
    mediana = y.median()
    minimo = y.min()
    maximo = y.max()


    fig = go.Figure()
    fig.add_trace(go.Box(
        y=df_valida[col],
        boxpoints='all',
        jitter=0.3,
        pointpos=-1.8,
        marker_color='#388F30',
        line_color='#950404',
        name='Idade'
    ))

    # Anotações
    fig.add_annotation(
        x=0.35, y=media,
        text=f"Média: {media:.1f}",
        showarrow=True,
        arrowhead=2,
        #ax=400,
        ay=0,
        font=dict(color="black"),
        bgcolor="rgba(255,200,200,0.2)"
    )
    fig.add_annotation(
        x=0.35, y=mediana,
        text=f"Mediana: {mediana:.1f}",
        showarrow=True,
        arrowhead=2,
        #ax=400,
        ay=0,
        font=dict(color="black"),
        bgcolor="rgba(255,200,200,0.2)"
    )
    fig.add_annotation(
        x=0.35, y=minimo,
        text=f"Mínimo: {minimo:.1f}",
        showarrow=True,
        arrowhead=2,
        #ax=400,
        ay=0,
        font=dict(color="black"),
        bgcolor="rgba(255,200,200,0.2)"
    )
    fig.add_annotation(
        x=0.35, y=maximo,
        text=f"Máximo: {maximo:.1f}",
        showarrow=True,
        arrowhead=2,
        #ax=400,
        ay=0,
        font=dict(color="black"),
        bgcolor="rgba(255,200,200,0.2)"
    )
    fig.update_layout(
        title=f"Boxplot da Idade na Data do Crime - {estado}",
        yaxis_title="Idade (anos)",
        xaxis_title="",
        showlegend=False,
        height=515,
        margin=dict(l=40, r=40, t=60, b=40),
        plot_bgcolor='white',
    )
    return fig

@callback(
    Output("grafico-donut-relacao", "figure"),
    Input("estado-dropdown-selection", "value"),
)

def atualizar_grafico_donut_relacao(estado):
    df = carregar_df_estado(estado)
    # Pegue a coluna diretamente do dicionário
    coluna_escolhida = list(COLUNAS_DONUT_RELACAO.values())[0]
    if not coluna_escolhida or coluna_escolhida not in df.columns:
        return go.Figure()
    dados = df[coluna_escolhida].dropna()
    if dados.empty:
        return go.Figure()
    contagem = dados.value_counts()
    labels = contagem.index.tolist()
    valores = contagem.values.tolist()

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=valores,
        hole=0.45,
        marker=dict(colors=CORES_GRAFICOS[:len(labels)]),
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
        title="Relação entre Réu e Vítima",
        margin=dict(l=40, r=40, t=60, b=40),
        showlegend=True,
        height=430,
        legend_title_text="Resposta"
    )
    return fig

# Callback para o gráfico de barras de tipo de relação
@callback(
    Output("grafico-bar-tipo-relacao", "figure"),
    Input("estado-dropdown-selection", "value"),
)
def atualizar_grafico_tipo_relacao(estado):
    df = carregar_df_estado(estado)
    cols_tipo = list(CAUSAS_RELACAO.keys())
    df_rel = df[cols_tipo].copy() if all(col in df.columns for col in cols_tipo) else df[[col for col in cols_tipo if col in df.columns]].copy()
    if df_rel.empty:
        return go.Figure()
    contagem = (df_rel == "Sim").sum().rename(index=CAUSAS_RELACAO)
    contagem = contagem[contagem.index != "Sem informação"]
    contagem = contagem.sort_values(ascending=True)
    total = contagem.sum()
    cores = CORES_GRAFICOS * (len(contagem) // len(CORES_GRAFICOS) + 1)

    fig = go.Figure(go.Bar(
        x=contagem.values,
        y=contagem.index,
        orientation='h',
        marker_color=cores[:len(contagem)],
        text=[f"{v} ({(v/total*100):.1f}%)" if total > 0 else "0 (0%)" for v in contagem.values],
        textposition='outside',
    ))
    fig.update_layout(
        title="Tipos de relação entre réu e vítima",
        xaxis_title="Quantidade de casos",
        yaxis_title="Tipo de relação",
        margin=dict(l=40, r=40, t=60, b=40),
        height=430,
        plot_bgcolor='white',
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(200,200,200,0.15)')
    fig.update_yaxes(showgrid=False)
    return fig