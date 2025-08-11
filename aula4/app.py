
import pandas as pd

import streamlit as st

import plotly.express as px

import funcoes


st.set_page_config(
    
    page_title="Dashboard de Salários ma Área de Dados",
    
    page_icon="📊",

    layout="wide",

)


base_de_dados = funcoes.carregar_dados()

st.sidebar.header("Filtros")

anos_disponiveis = sorted(base_de_dados['ano'].unique())

anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)

senioridades_disponiveis = sorted(base_de_dados['senioridade'].unique())

senioridades_selecionadas = st.sidebar.multiselect('senioridade', senioridades_disponiveis, default=senioridades_disponiveis)

contratos_disponiveis = sorted(base_de_dados['Contrato'].unique())

contratos_selecionados = st.sidebar.multiselect("Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis)

tamanhos_disponiveis = sorted(base_de_dados['tamanho_empresa'].unique())

tamanhos_selecionados = st.sidebar.multiselect("tamanho da empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)

base_de_dados_filtrado = base_de_dados[
    (base_de_dados['ano'].isin(anos_selecionados)) &
    (base_de_dados['senioridade'].isin(senioridades_selecionadas)) &
    (base_de_dados['Contrato'].isin(contratos_selecionados)) &
    (base_de_dados['tamanho_empresa'].isin(tamanhos_selecionados))
]

st.title("🎲 Dashboard de Análise de Salários na Área de Dados")

st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise.")

st.subheader("Métricas gerais (Salário anual em USD)")

if not base_de_dados_filtrado.empty:
    salario_medio = base_de_dados_filtrado['usd'].mean()
    salario_maximo = base_de_dados_filtrado['usd'].max()
    total_registros = base_de_dados_filtrado.shape[0]
    cargo_mais_frequente = base_de_dados_filtrado["cargo"].mode()[0]
else:
    salario_medio, salario_mediano, salario_maximo, total_registros, cargo_mais_comum = 0, 0, 0, ""

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário médio", f"${salario_medio:,.0f}")
col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de registros", f"{total_registros:,}")
col4.metric("Cargo mais frequente", cargo_mais_frequente)

st.markdown("---")


st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not base_de_dados_filtrado.empty:
        top_cargos = base_de_dados_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(
            top_cargos,
            x='usd',
            y='cargo',
            orientation='h',
            title="Top 10 cargos por salário médio",
            labels={'usd': 'Média salarial anual (USD)', 'cargo': ''}
        )
        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de cargos.")

with col_graf2:
    if not base_de_dados_filtrado.empty:
        grafico_hist = px.histogram(
            base_de_dados_filtrado,
            x='usd',
            nbins=30,
            title="Distribuição de salários anuais",
            labels={'usd': 'Faixa salarial (USD)', 'count': ''}
        )
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de distribuição.")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not base_de_dados_filtrado.empty:
        remoto_contagem = base_de_dados_filtrado['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
        grafico_remoto = px.pie(
            remoto_contagem,
            names='tipo_trabalho',
            values='quantidade',
            title='Proporção dos tipos de trabalho',
            hole=0.5  
        )
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")


df = pd.read_csv('dados-imersao-final.csv')

import pycountry

import plotly.express as px

def iso2_to_iso3(code):
    
    try:
        
        return pycountry.countries.get(alpha_2=code).alpha_3

    except:
        
        return None

df['residencia_iso_3'] = df['residencia'].apply(iso2_to_iso3)

df_ds = df[df['cargo'] == 'Data Scientist']

media_ds_pais = df_ds.groupby('residencia_iso_3')['usd'].mean().reset_index()

fig = px.choropleth(
    
    media_ds_pais,
    
    locations = 'residencia_iso_3',
    
    color = 'usd',
    
    color_continuous_scale='rdylgn',
    
    title = 'Salário Médio de Cientista de Dados por Pais',
    
    
    labels = {'usd': 'Salário Médio (USD)', 'residencia_iso_3': 'Pais'}
    
)


fig.show()



with col_graf4:
    if not df.empty:
        df_ds = df[df['cargo'] == 'Data Scientist']
        media_ds_pais = df_ds.groupby('residencia_iso_3')['usd'].mean().reset_index()
        grafico_paises = px.choropleth(media_ds_pais,
            locations='residencia_iso_3',
            color='usd',
            color_continuous_scale='rdylgn',
            title='Salário médio de Cientista de Dados por país',
            labels={'usd': 'Salário médio (USD)', 'residencia_iso_3': 'País'})
        grafico_paises.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.") 

# --- Tabela de Dados Detalhados ---
st.subheader("Dados Detalhados")
st.dataframe(base_de_dados_filtrado)