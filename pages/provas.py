import dash
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
from dash import Input, Output, callback, dcc, html
from caching import retrieve_data
import plotly.graph_objects as go
import plotly.express as px


from utils import TITLE

def carregar_df_estado(estado, tipo="provas"):
    print(f"Carregando dados para o estado: {estado}, tipo: {tipo}")
    if estado == "Minas Gerais":
        return pd.read_csv(f"data/TJMG/df_{tipo}_TJMG.csv")
    else:
        return pd.read_csv(f"data/TJSP/df_{tipo}_TJSP.csv")


PAGE_TITLE = "Provas"

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", order=2)

# Paleta de cores (ajuste se quiser)
CORES_GRAFICOS = ['#950404', '#E04B28', '#C38961', '#388F30', '#007D82']

ESTADOS = {"São Paulo": "SP",
        "Minas Gerais": "MG"}  # Adicione outros estados conforme necessário


EXAMES_PERICIAIS =  {
    'P1Q0[SQ025]': 'Exame de necropsia',
    'P1Q0[SQ001]': 'Exame em local de crime',
    'P1Q0[SQ002]': 'Exame em arma de fogo',
    'P1Q0[SQ003]': 'Exame em arma branca',
    'P1Q0[SQ004]': 'Exame em documentos (ex.: grafotécnico)',
    'P1Q0[57481]': 'Exame em poeiras, pós e cinzas',
    'P1Q0[SQ005]': 'Exame em peças \nde vestuários, acessórios e pertences',
    'P1Q0[SQ006]': 'Exame em outros tipos de vestígios físicos',
    'P1Q0[SQ007]': 'Exame em computadores ou tablets',
    'P1Q0[SQ008]': 'Exame em aparelhos celulares',
    'P1Q0[SQ009]': 'Exame em arquivos de vídeo/imagens/áudio',
    'P1Q0[SQ012]': 'Exame em outros tipos de dispositivos digitais',
    'P1Q0[SQ011]': 'Exame em marcas de \nmordidas ou impressões labiais',
    'P1Q0[SQ010]': 'Exame em impressões \npapiloscópicas (impressão digital)',
    'P1Q0[SQ013]': 'Exame em outros tipos \nde vestígios morfológicos',
    'P1Q0[SQ014]': 'Exame de corpo de delito do acusado',
    'P1Q0[SQ018]': 'Exame de corpo de delito da vítima',
    'P1Q0[79893]': 'Exame toxicológico do acusado',
    'P1Q0[SQ017]': 'Exame toxicológico da vítima',
    'P1Q0[SQ016]': 'Exame em sangue (outros tipos)',
    'P1Q0[SQ015]': 'Exame em sêmen',
    'P1Q0[SQ019]': 'Exame em dentes',
    'P1Q0[SQ023]': 'Exame psicológico/psiquiátrico do acusado',
    'P1Q0[SQ022]': 'Exame psicológico/psiquiátrico da vítima',
    'P1Q0[SQ021]': 'Exame em outros tipos de vestígios biológicos',
    'P1Q0[66635]': 'Exame em drogas lícitas',
    'P1Q0[SQ020]': 'Exame em drogas ilícitas',
    'P1Q0[SQ024]': 'Exame em outros tipos de vestígios químicos', # (ex.: líquidos, combustíveis, bebidas, metais, etc)',
    'P1Q0[SQ026]': 'Exame em fragmentos veiculares',
    'P1Q0[SQ027]': 'Exame em componentes veiculares'
}

TEMPO_EXAMES_PERICIAIS =  {
    'P1Q0[SQ025]': ('Exame de necropsia', 'P1Q1[SQ026_SQ002]', 'P1Q1[SQ026_SQ003]'),
    'P1Q0[SQ001]': ('Exame em local de crime', 'P1Q1[SQ001_SQ002]', 'P1Q1[SQ001_SQ003]'),
    'P1Q0[SQ002]': ('Exame em arma de fogo', 'P1Q1[SQ002_SQ002]', 'P1Q1[SQ002_SQ003]'),
    'P1Q0[SQ003]': ('Exame em arma branca', 'P1Q1[SQ003_SQ002]', 'P1Q1[SQ003_SQ003]'),
    'P1Q0[SQ004]': ('Exame em documentos \n(ex.: grafotécnico)', 'P1Q1[SQ004_SQ002]', 'P1Q1[SQ004_SQ003]'),
    'P1Q0[57481]': ('Exame em poeiras, \npós e cinzas', 'P1Q1[SQ005_SQ002]', 'P1Q1[SQ005_SQ003]'),
    'P1Q0[SQ005]': ('Exame em peças \nde vestuários, \nacessórios e pertences', 'P1Q1[SQ006_SQ002]', 'P1Q1[SQ006_SQ003]'),
    'P1Q0[SQ006]': ('Exame em outros \ntipos de vestígios físicos', 'P1Q1[SQ007_SQ002]', 'P1Q1[SQ007_SQ003]'),
    'P1Q0[SQ007]': ('Exame em \ncomputadores ou tablets', 'P1Q1[SQ008_SQ002]', 'P1Q1[SQ008_SQ003]'),
    'P1Q0[SQ008]': ('Exame em \naparelhos celulares', 'P1Q1[SQ009_SQ002]', 'P1Q1[SQ009_SQ003]'),
    'P1Q0[SQ009]': ('Exame em arquivos \nde vídeo/imagens/áudio', 'P1Q1[SQ010_SQ002]', 'P1Q1[SQ010_SQ003]'),
    'P1Q0[SQ012]': ('Exame em outros \ntipos de dispositivos digitais', 'P1Q1[SQ011_SQ002]', 'P1Q1[SQ011_SQ003]' ),
    'P1Q0[SQ011]': ('Exame em marcas \nde mordidas ou \nimpressões labiais', 'P1Q1[SQ012_SQ002]', 'P1Q1[SQ012_SQ003]'),
    'P1Q0[SQ010]': ('Exame em \nimpressões papiloscópicas \n(impressão digital)', 'P1Q1[SQ013_SQ002]', 'P1Q1[SQ013_SQ003]'),
    'P1Q0[SQ013]': ('Exame em outros \ntipos de vestígios morfológicos', 'P1Q1[SQ014_SQ002]', 'P1Q1[SQ014_SQ003]'),
    'P1Q0[SQ014]': ('Exame de corpo \nde delito do acusado', 'P1Q1[SQ015_SQ002]', 'P1Q1[SQ015_SQ003]'),
    'P1Q0[SQ018]': ('Exame de corpo \nde delito da vítima', 'P1Q1[SQ016_SQ002]', 'P1Q1[SQ016_SQ003]'),
    'P1Q0[79893]': ('Exame toxicológico do acusado', 'P1Q1[SQ019_SQ002]', 'P1Q1[SQ019_SQ003]'),
    'P1Q0[SQ017]': ('Exame toxicológico da vítima','P1Q1[SQ018_SQ002]', 'P1Q1[SQ018_SQ003]'),
    'P1Q0[SQ016]': ('Exame em sangue (outros tipos)', 'P1Q1[SQ017_SQ002]', 'P1Q1[SQ017_SQ003]'),
    'P1Q0[SQ015]': ('Exame em sêmen', 'P1Q1[SQ020_SQ002]', 'P1Q1[SQ020_SQ003]'),
    'P1Q0[SQ019]': ('Exame em dentes','P1Q1[SQ024_SQ002]', 'P1Q1[SQ024_SQ003]'),
    'P1Q0[SQ023]': ('Exame psicológico/psiquiátrico \ndo acusado', 'P1Q1[SQ023_SQ002]', 'P1Q1[SQ023_SQ003]'),
    'P1Q0[SQ022]': ('Exame psicológico/psiquiátrico \nda vítima','P1Q1[SQ022_SQ002]', 'P1Q1[SQ022_SQ003]'),
    'P1Q0[SQ021]': ('Exame em outros \ntipos de vestígios biológicos', 'P1Q1[SQ021_SQ002]', 'P1Q1[SQ021_SQ003]'),
    'P1Q0[66635]': ('Exame em drogas lícitas', 'P1Q1[SQ025_SQ002]', 'P1Q1[SQ025_SQ003]'),
    'P1Q0[SQ020]': ('Exame em drogas ilícitas', 'P1Q1[SQ028_SQ002]', 'P1Q1[SQ028_SQ003]'),
    'P1Q0[SQ024]': ('Exame em outros \ntipos de vestígios químicos \n(ex.: líquidos, combustíveis, bebidas, metais, etc)', 'P1Q1[SQ027_SQ002]', 'P1Q1[SQ027_SQ003]'),
    'P1Q0[SQ026]': ('Exame em fragmentos veiculares', 'P1Q1[SQ029_SQ002]', 'P1Q1[SQ029_SQ003]'),
    'P1Q0[SQ027]': ('Exame em componentes veiculares', 'P1Q1[SQ030_SQ002]', 'P1Q1[SQ030_SQ003]')
}

DILIGENCIAS_IP = {
 'P3Q21[SQ001]': 'Busca e apreensão de armas de fogo',
 'P3Q21[SQ002]': 'Busca e apreensão de drogas',
 'P3Q21[SQ003]': 'Busca e apreensão de\n outras substâncias ou objetos',
 'P3Q21[SQ004]': 'Fotografias/vídeos da prisão em flagrante\n e/ou busca domiciliar',
 'P3Q21[SQ005]': 'Mídias de substâncias ou objetos apreendidos',
 'P3Q21[SQ006]': 'Mídias extraídas de redes sociais',
 'P3Q21[SQ007]': 'Imagens de câmeras de segurança',
 'P3Q21[SQ008]': 'Fotografias/vídeos de outros tipos',
 'P3Q21[SQ009]': 'Depoimentos de testemunhas',
 'P3Q21[SQ010]': 'Depoimentos de agentes de segurança',
 'P3Q21[SQ011]': 'Interrogatório dos réus',
 'P3Q21[SQ012]': 'Interceptação telefônica',
 'P3Q21[SQ013]': 'Quebra de sigilo bancário',
 'P3Q21[SQ014]': 'Quebra de sigilo de dados telefônicos',
 'P3Q21[SQ015]': 'Reconhecimento de pessoas',
 'P3Q21[SQ016]': 'Reconhecimento de coisas',
 'P3Q21[SQ017]': 'Reconstituição de crime',
 'P3Q21[SQ018]': 'Sequestro de bens'
}

def layout():
    estados = list(ESTADOS.keys())
    exames_options = [
        {"label": descricao, "value": coluna}
        for coluna, descricao in EXAMES_PERICIAIS.items()
    ]
    exames_padrao = list(EXAMES_PERICIAIS.keys())[:10]  # Exiba os 10 primeiros como padrão (ajuste se quiser)

    return [
        html.H3("Provas", className="mb-3"),
        html.P(
            """
            Essa página fornece uma visão geral das provas do processo. 
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
        dbc.Card(
            dbc.CardBody([
                dbc.Row(
                    dbc.Col(
                        dcc.Dropdown(
                            options=[{"label": v, "value": k} for k, v in DILIGENCIAS_IP.items()],
                            value=list(DILIGENCIAS_IP.keys())[:5],
                            multi=True,
                            id="diligencias-policiais-dropdown",
                            placeholder="Selecione as diligências policiais para exibir",
                        ),
                        md=12,
                        sm=12,
                    ),
                ),
                html.Div(style={"height": "16px"}),  # Espaçamento entre o dropdown e o gráfico
                html.H5("Diligências Policiais juntadas no IP", className="mb-3"),
                dcc.Graph(id="grafico-diligencias-policiais"),
            ])
        ),
        html.Hr(),
        dbc.Card(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(
                    dbc.Card(
                            dbc.CardBody([
                                html.H5("Preservação do Local do Crime", className="mb-3"),
                                dcc.Graph(id="grafico-donut-preservacao"),
                            ]),
                        ),
                        md=6, sm=12,
                    ),
                    dbc.Col(
                    dbc.Card(
                            dbc.CardBody([
                                html.H5("Isolamento do Local do Crime", className="mb-3"),
                                dcc.Graph(id="grafico-donut-isolamento"),
                            ]),
                        ),
                        md=6, sm=12,
                    ),
                ]),
            ]),
        ),
        html.Hr(),
        dbc.Card(
            dbc.CardBody([
                dbc.Row(
                    dbc.Col(
                        dcc.Dropdown(
                            options=exames_options,
                            value=exames_padrao,
                            multi=True,
                            id="exames-periciais-dropdown",
                            placeholder="Selecione os exames para exibir",
                        ),
                        md=12,
                        sm=12,
                    ),
                ),
                html.Div(style={"height": "16px"}),  # Espaçamento entre o dropdown e o gráfico
                html.H5("Exames Periciais juntados no IP", className="mb-3"),
                dcc.Graph(id="grafico-exames-periciais"),
            ])
        ),
        html.Hr(),
        dbc.Card(
            dbc.CardBody([
                html.H5("Quadro Resumo dos Tempos dos Exames", className="mb-3"),
                dash_table.DataTable(
                    id="tabela-quadro-resumo-tempo",
                    columns=[],
                    data=[],
                    style_cell={"textAlign": "center", "fontSize": 13},
                    style_header={"backgroundColor": "#b8431f", "color": "white", "fontWeight": "bold"},
                    style_data_conditional=[
                        {"if": {"row_index": "odd"}, "backgroundColor": "#fef9f9"},
                        {"if": {"row_index": "even"}, "backgroundColor": "#ffffff"},
                    ],
                    style_table={"overflowX": "auto"},
                ),
            ])
        ),

    ]

@callback(
    Output("grafico-diligencias-policiais", "figure"),
    [
        Input("estado-dropdown-selection", "value"),
        Input("diligencias-policiais-dropdown", "value"),
    ],
)
def atualizar_grafico_diligencias_policiais(estado, diligencias_selecionadas):
    df = carregar_df_estado(estado, "processo")
    print(df.head())
    labels = []
    nao = []
    sim = []

    if not diligencias_selecionadas:
        diligencias_selecionadas = []

    for coluna in diligencias_selecionadas:
        descricao = DILIGENCIAS_IP.get(coluna, coluna)
        if coluna in df.columns:
            dados = df[coluna].dropna()
            contagem = dados.value_counts()
            labels.append(descricao)
            nao.append(contagem.get('Não', 0))
            sim.append(contagem.get('Sim', 0))
        else:
            labels.append(descricao)
            nao.append(0)
            sim.append(0)

    cores = {
        'Não': CORES_GRAFICOS[0] if len(CORES_GRAFICOS) > 3 else '#1f77b4',
        'Sim': CORES_GRAFICOS[3] if len(CORES_GRAFICOS) > 1 else '#ff7f0e'
    }

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=labels,
        x=nao,
        name='Não',
        orientation='h',
        marker_color=cores['Não'],
        customdata=[(n, s) for n, s in zip(nao, sim)],
        hovertemplate='Não: %{x}<br>Sim: %{customdata[1]}<extra></extra>',
    ))
    fig.add_trace(go.Bar(
        y=labels,
        x=sim,
        name='Sim',
        orientation='h',
        marker_color=cores['Sim'],
        customdata=[(n, s) for n, s in zip(nao, sim)],
        hovertemplate='Sim: %{x}<br>Não: %{customdata[0]}<extra></extra>',
    ))

    fig.update_layout(
    barmode='stack',
    title="Diligências Policiais juntadas no IP",
    xaxis_title=None,
    yaxis_title=None,
    height=60 + 40 * len(labels),
    legend_title="Legenda",
    margin=dict(l=40, r=10, t=60, b=40),  # r=10 reduz a margem direita
    showlegend=True,
    template="plotly_white",
    )

    fig.update_xaxes(
    showticklabels=False,
    showgrid=False,
    zeroline=False,
    title=None,
    fixedrange=True,
    range=[0, max([n + s for n, s in zip(nao, sim)]) * 1.05] if labels else [0, 1]
    )

    return fig

@callback(
    Output("grafico-donut-preservacao", "figure"),
    Input("estado-dropdown-selection", "value"),
)

def atualizar_grafico_donut_preservacao(estado):
    df = carregar_df_estado(estado, "vitima")
    # Pegue a coluna diretamente do dicionário
    coluna_escolhida = "P2Q7. De acordo com o laudo do exame do local, o local do crime estava preservado no momento de chegada do profissional que atestou o crime?"
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
        title="Preservação do Local do Crime",
        margin=dict(l=40, r=40, t=60, b=40),
        showlegend=True,
        height=430,
        legend_title_text="Resposta"
    )
    return fig

@callback(
    Output("grafico-donut-isolamento", "figure"),
    Input("estado-dropdown-selection", "value"),
)

def atualizar_grafico_donut_isolamento(estado):
    df = carregar_df_estado(estado, "vitima")
    # Pegue a coluna diretamente do dicionário
    coluna_escolhida = "P2Q6B. De acordo com o laudo do exame do local, o local estava isolado no momento de chegada do profissional que atestou o crime?"
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
        title="Isolamento do Local do Crime",
        margin=dict(l=40, r=40, t=60, b=40),
        showlegend=True,
        height=430,
        legend_title_text="Resposta"
    )
    return fig


@callback(
    Output("grafico-exames-periciais", "figure"),
    [
        Input("estado-dropdown-selection", "value"),
        Input("exames-periciais-dropdown", "value"),
    ],
)
def atualizar_grafico_exames_periciais(estado, exames_selecionados):
    df = carregar_df_estado(estado)
    labels = []
    nao = []
    sim = []

    if not exames_selecionados:
        exames_selecionados = []

    for coluna in exames_selecionados:
        descricao = EXAMES_PERICIAIS.get(coluna, coluna)
        if coluna in df.columns:
            dados = df[coluna].dropna()
            contagem = dados.value_counts()
            labels.append(descricao)
            nao.append(contagem.get('Não', 0))
            sim.append(contagem.get('Sim', 0))
        else:
            labels.append(descricao)
            nao.append(0)
            sim.append(0)

    cores = {
        'Não': CORES_GRAFICOS[0] if len(CORES_GRAFICOS) > 3 else '#1f77b4',
        'Sim': CORES_GRAFICOS[3] if len(CORES_GRAFICOS) > 1 else '#ff7f0e'
    }

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=labels,
        x=nao,
        name='Não',
        orientation='h',
        marker_color=cores['Não'],
        customdata=[(n, s) for n, s in zip(nao, sim)],
        hovertemplate='Não: %{x}<br>Sim: %{customdata[1]}<extra></extra>',
    ))
    fig.add_trace(go.Bar(
        y=labels,
        x=sim,
        name='Sim',
        orientation='h',
        marker_color=cores['Sim'],
        customdata=[(n, s) for n, s in zip(nao, sim)],
        hovertemplate='Sim: %{x}<br>Não: %{customdata[0]}<extra></extra>',
    ))

    fig.update_layout(
    barmode='stack',
    title="Exames Periciais juntados no IP",
    xaxis_title=None,
    yaxis_title=None,
    height=60 + 40 * len(labels),
    legend_title="Legenda",
    margin=dict(l=40, r=10, t=60, b=40),  # r=10 reduz a margem direita
    showlegend=True,
    template="plotly_white",
    )

    fig.update_xaxes(
    showticklabels=False,
    showgrid=False,
    zeroline=False,
    title=None,
    fixedrange=True,
    range=[0, max([n + s for n, s in zip(nao, sim)]) * 1.05] if labels else [0, 1]
    )

    return fig

@callback(
    Output("tabela-quadro-resumo-tempo", "data"),
    Output("tabela-quadro-resumo-tempo", "columns"),
    [
        Input("estado-dropdown-selection", "value"),
        Input("exames-periciais-dropdown", "value"),
    ],
)
def atualizar_quadro_resumo_tempo(estado, exames_selecionados):
    df = carregar_df_estado(estado)
    quadro_resumo = {}

    if not exames_selecionados:
        exames_selecionados = []

    for coluna in exames_selecionados:
        if coluna in TEMPO_EXAMES_PERICIAIS:
            nome_exame, col_inicio, col_fim = TEMPO_EXAMES_PERICIAIS[coluna]
            # Converte para datetime
            df[col_inicio] = pd.to_datetime(df[col_inicio], dayfirst=True, errors='coerce')
            df[col_fim] = pd.to_datetime(df[col_fim], dayfirst=True, errors='coerce')
            # Calcula duração
            df_valid = df[[col_inicio, col_fim, 'P0Q2. Número do Processo (Formato: 0000000-00.0000.0.00.0000):']].dropna()
            df_valid['duracao'] = (df_valid[col_fim] - df_valid[col_inicio]).dt.days

            if df_valid.empty:
                media = mediana = desvio = n_processos = '-'
            else:
                media = round(df_valid['duracao'].mean(), 1)
                mediana = int(df_valid['duracao'].median())
                desvio = round(df_valid['duracao'].std(), 1)
                n_processos = df_valid['P0Q2. Número do Processo (Formato: 0000000-00.0000.0.00.0000):'].nunique()

            quadro_resumo[nome_exame] = [media, mediana, desvio, n_processos]

    df_quadro = pd.DataFrame.from_dict(quadro_resumo, orient='index')
    df_quadro.columns = ['Tempo Médio (dias)', 'Mediana (dias)', 'Desvio Padrão', 'Nº de Processos']
    df_quadro.reset_index(inplace=True)
    df_quadro.rename(columns={'index': 'Exame'}, inplace=True)

    columns = [{"name": col, "id": col} for col in df_quadro.columns]
    data = df_quadro.to_dict("records")
    return data, columns