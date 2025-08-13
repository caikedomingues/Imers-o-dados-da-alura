
# Import da biblioteca pandas que tem como objetivo acessar, carregar
# e manipular datasets.
import pandas as pd

# O streamlit é uma biblioteca python que serve para construir
# aplicações web interativas de forma muito rápida e simples, usando
# apenas códigos Python. Ela serve para mostrar as nossas
# análises para outras pessoas sem precisar compartilhar um
# notebook. O streamlit te permite transformar o seu código
# em um dashboard interativo ou em uma aplicação web.
# -> Nós podemos criar um dashboard que mostram seus gráficos (sebaorn,
# plotly, etc).
# -> Você pode adicionar widgets como sliders, botões e caixas de
# de seleção, para que o usuário possa interagir e alterar os dados
# que estão sendo visualizados.
# -> Tudo isso sem precisar de conhecimento em HTML, CSS ou JavaScript.
import streamlit as st

# Import da biblioteca plotly.express que tem como objetivo
# criar gráficos interativos. 
import plotly.express as px

# import do nosso arquivo defunções que irá
# carregar o dataset na memória ja higienizado
# e preparado.
import funcoes

# Serve para configurar a página web como um todo. Devemos pensar
# nisso como o "setup" inicial do seu dashboard. Ela deve ser a
# primeira chamada streamlit no script.
st.set_page_config(
    
    # Define o titulo que aparece na aba do navegador
    page_title="Dashboard de Salários ma Área de Dados",
    
    # Define o icone (favicon) que aparece na aba do navegador. Usar
    # emojis é uma forma simples e eficaz de fazer isso.
    page_icon="📊",

    # O layout padrão do streamlit é centralizado (centered), o que deixa
    # um espaço em branco nas laterais. Ao usar "wide", você faz com que 
    # o conteúdo do seu dashboard ocupe toda a largura disponivel da tela
    #, o que é ideal para exibir gráficos e tabelas grandes.
    layout="wide",

)

# Chamada da função que irá carregar e preparar o dataset na memória.
# O dataset ficara armazenado na variável 'base_de_dados'.
base_de_dados = funcoes.carregar_dados()

                        # Criação dos filtros do dashboard

# st.sidebar: É um comando que permite adicionar componentes a uma barra lateral na sua aplicação. Em vez de aparecerem no corpo principal da página, eles são colocados em um menu lateral recolhivel

# header(): Cria um cabeçalho (titulo de seção) na barra lateral. O
# texto "filtros" serve parav informar ao usuário qual a função daquela
# seção do seu dashborad.
st.sidebar.header("Filtros")

# Irá ordenar os valores unicos da coluna 'ano' em ordem
# crescente.
# sorted: Função do python que ordena os dados em ordem crescente/
# descrecente ou em ordem alfabética.
# unique: Função do pandas que tem como objetivo acessar os
# valores únicos de uma coluna.
anos_disponiveis = sorted(base_de_dados['ano'].unique())

# st.sidebar.multiselect: Cria um widget que permite ao usuário
# selecionar múltiplos itens a partir de uma lista. Ele é perfeito
# para o que precisamos fazer, que é filtrar dados por ano. A função
# recebe como argumento:
# Ano: rótulo que aparece ácima do widget na barra lateral. Ele 
# informa ao usuário o que ele está filtrando.
# anos_disponiveis: Esta é a lista de opções que o streamlit vai
# usar para preencher o widget. No seu caso, é a lista de anos que
# criamos.
anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)

# Acessando e organizando em ordem alfabética os valores únicos
# da coluna de senioridade.
senioridades_disponiveis = sorted(base_de_dados['senioridade'].unique())

# cria o widget que possibilita selecionar multiplos itens
# da coluna de senioridade com o objetivo de criar filtros de
# senioridade
senioridades_selecionadas = st.sidebar.multiselect('senioridade', senioridades_disponiveis, default=senioridades_disponiveis)

# # Acessando e organizando em ordem alfabética os valores únicos
# da coluna de contratos.
contratos_disponiveis = sorted(base_de_dados['Contrato'].unique())

# cria o widget que possibilita selecionar multiplos itens
# da coluna de senioridade com o objetivo de criar filtros de
# contratos
contratos_selecionados = st.sidebar.multiselect("Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis)

# Acessando e organizando em ordem alfabética os valores únicos
# da coluna de tamanhos de empresa.
tamanhos_disponiveis = sorted(base_de_dados['tamanho_empresa'].unique())

# cria o widget que possibilita selecionar multiplos itens
# da coluna de senioridade com o objetivo de criar filtros de
# tamanhos de empresa
tamanhos_selecionados = st.sidebar.multiselect("tamanho da empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)

# Trecho responsável por filtrar o DataFrame de acordo com as seleções
# que o usuário faz nos widgets da barra lateral.
# base_de_dados[...]: Forma padrão do pandas de filtrar DataFrame.
# O que está dentro dos colchetes é uma mascara booleana, ou seja,
# uma série de valores True ou False que define quais linhas serao
# mantidas e quais serão descartadas.
# isin: Tem como objetivo verificar se os valores selecionados
# pelos usuários estão presentes na lista de opçoes. Ela retorna
# True se o valor estiver na lista e False caso contrário.
base_de_dados_filtrado = base_de_dados[
    (base_de_dados['ano'].isin(anos_selecionados)) &
    (base_de_dados['senioridade'].isin(senioridades_selecionadas)) &
    (base_de_dados['Contrato'].isin(contratos_selecionados)) &
    (base_de_dados['tamanho_empresa'].isin(tamanhos_selecionados))
]

# Define o titulo do aplicação web
st.title("🎲 Dashboard de Análise de Salários na Área de Dados")

# Função que tem como objetivo renderizar textos usando a sintaxe
# markdown (linha que fica em baixo do texto). Markdown é uma 
# linguagem simpls para formatação de texto que é muito usado
# na web. No nosso caso, o texto que colocamos serve como 
# introdução clara para o nosso dashboard, explicando rapidamente
# o que ele faz e, mais importante, instruindo o usuário a utilizar
# os filtros na barra lateral.
st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise.")

# Serve para criar um subtitulo no cabeçalho
st.subheader("Métricas gerais (Salário anual em USD)")

# Bloco que serve para garantir que a aplicação nao quebre caso o usuário
# faça uma combinação de filtros que não retorne nenhum dado.

# if not base_de_dados_filtrado.empty: Caso a condição seja
# verdadeira, ou seja, se o DataFrame não estiver vázio, iremos 
# apresentar os valores apresentados.
# empty: Função do pandas que retorna True se o DataFrame estiver
# vázio (ou seja, não tiver linhas).
# not: O not inverte a lógica. Então, a condição completa significa: "se o DataFrame filtrado não estiver vazio."
# mean: Retorna a média dos salários.
# max: Retorna o maior salário do DataFrame.
# shape[0]: Retorna o número de linhas do DataFrame.
# mode: Retorna a moda da coluna de cargos, ou seja, o 
# cargo mais frequente (o que mais aparece) no DataFrame.
# else: Caso a condição seja verdadeira (se o DataFrame
# estiver vázio), vamos atribuir o valor 0 a variáveis numéricas
# e vázio para variáveis categóricas
if not base_de_dados_filtrado.empty:
    salario_medio = base_de_dados_filtrado['usd'].mean()
    salario_maximo = base_de_dados_filtrado['usd'].max()
    total_registros = base_de_dados_filtrado.shape[0]
    cargo_mais_frequente = base_de_dados_filtrado["cargo"].mode()[0]
else:
    
    salario_medio, salario_mediano, salario_maximo, total_registros, cargo_mais_comum = 0, 0, 0, ""

# st.columns(4): Ira organizar o espaço principal da aplicação
# em quatro colunas, e armazenamos cada uma delas nas variaveis
# col1, col2, col3 e col4. Isso nos dá controle total sobre onde
# colocar o seu conteúdo na tela.
# metric: Tem como objetivo criar um widget visualmente destacado
# com um rótulo, um valor e (opcionalmente) uma diferença
# salário médio: Rótulo do widget.
# salario_medio: variável que contém o valor do widget
col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário médio", f"${salario_medio:,.0f}")
col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de registros", f"{total_registros:,}")
col4.metric("Cargo mais frequente", cargo_mais_frequente)

st.markdown("---")


st.subheader("Gráficos")

# Ira dividir o espaço das variáveis col1 e col2
# em 2 colunas
col_graf1, col_graf2 = st.columns(2)

# with col_graf1: É um context manager do streamlit que te permite
# colocar todo o conteúdo que você escrever dentro dele, na coluna 
# que você definiu. É a forma mais limpa de organizar o layout.  
with col_graf1:
    
    # Novamente, estamos usando a verificação de segurança que evita
    # que o código quebre quando o usuário seleciona filtros que 
    # não retornam nenhum dado.
    if not base_de_dados_filtrado.empty:
        
        # groupby('cargo')['usd'].mean(): Primeiro, vamos agrupar os
        # dados por cargo e calcular médias dos sala´rios de cada cargo
        
        # nlargest(10): Irá selecionar os 10 maiores salários médios.
        
        # sort_values(ascending=True): Irá organizar os dados em forma
        # decrescente.
        
        # reset_index: Irá criar uma coluna que irá conter os indices
        # dos cargos 
        top_cargos = base_de_dados_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        
        # Irá construir o gráfico de barras interátivo
        grafico_cargos = px.bar(
            top_cargos,
            x='usd',
            y='cargo',
            orientation='h',
            title="Top 10 cargos por salário médio",
            labels={'usd': 'Média salarial anual (USD)', 'cargo': ''}
        )
        
        # Ira ajustar a posição do titulo e, mais importante, garantindo
        # que a ordem das categorias no eixo Y (yaxis) respeite a ordem
        # que você já definiu com o  Pandasm o que é fundamental para a
        # visualização dos dados.
        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        
        # Esta é a função que pega a sua figura do plotly e a renderiza na coluna do streamlit
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        
        # Ira apresentar uma mensagem de erro caso a construção do gráfico não dê certo.
        st.warning("Nenhum dado para exibir no gráfico de cargos.")
# Conteúdo da coluna 2
with col_graf2:
    
    # Verificando se o DataFrane está vázio.
    if not base_de_dados_filtrado.empty:
        
        # Se ele não estiver vázio vamos criar o gráfico de pizza
        # interativo utilizando a biblioteca plotly
        grafico_hist = px.histogram(
            base_de_dados_filtrado,
            x='usd',
            nbins=30,
            title="Distribuição de salários anuais",
            labels={'usd': 'Faixa salarial (USD)', 'count': ''}
        )
        
        # Ira ajustar o titulo do gráfico.
        grafico_hist.update_layout(title_x=0.1)
        
        # Irá renderizar a coluna na aplicação
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        
        # Mensagem de erro que irá ser exibida caso a construção do
        # gráfico falhe.
        st.warning("Nenhum dado para exibir no gráfico de distribuição.")

# Ira dividir o espaço das variáveis col3 e col4
# em 2 colunas
col_graf3, col_graf4 = st.columns(2)

# Conteúdo da coluna 3
with col_graf3:
    
    # Ira verificar se o DataFrame não está vázio
    if not base_de_dados_filtrado.empty:
        
        # Ira contar a frequência de cada valorúnico da coluna e
        # criara uma coluna que ira conter um indice dos valores
        # da coluna
        remoto_contagem = base_de_dados_filtrado['remoto'].value_counts().reset_index()
        
        # Ira renomear os valores das colunas.
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
        
        # Irá construir um gráfico de pizza interativo 
        grafico_remoto = px.pie(
            remoto_contagem,
            names='tipo_trabalho',
            values='quantidade',
            title='Proporção dos tipos de trabalho',
            hole=0.5  
        )
        # Irá mostrar no gr´fico de piza o percentual dos dados 
        # e os seus rótulos
        grafico_remoto.update_traces(textinfo='percent+label')
        
        # Ira ajustar a posição do titulo do gráfico.
        grafico_remoto.update_layout(title_x=0.1)
        
        # Irá renderizar a coluna na aplicação
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        
        # Mensagem que será exibida caso a construção do gráfico falhe
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")


# Agora vamos usar essa outra base de dados que iremos modificar um pouco
# para aprender outras técnicas e métodos.

# Acessando e carregando o dataset usando o pandas
df = pd.read_csv('dados-imersao-final.csv')

# biblioteca de Python que serve como uma fonte de dados padronizada sobre países.

# Pense nele como um grande dicionário ou banco de dados que contém informações oficiais e padronizadas sobre todos os países do mundo.
import pycountry

# Define uma função chamada iso2_to_iso3 que tem um objetivo claro: converter um código de país de duas letras (Alpha-2) para um código de três letras (Alpha-3), que é um padrão frequentemente usado em bibliotecas de visualização como o Plotly.
def iso2_to_iso3(code):
    
    try:
        # Dentro do bloco de tratamento de erros usamos a a biblioteca pycountry para encontrar o país com base no código de duas letras (alpha_2) e, se encontrar, retorna o código de três letras (alpha_3).
        return pycountry.countries.get(alpha_2=code).alpha_3

    except:
        # Se o pycountry não encontrar um país para o código que você forneceu (por exemplo, se o código for inválido), a execução do try falha. O programa, em vez de gerar um erro e parar, "pula" para o bloco except e executa o código que está lá, retornando o valor None de forma segura.
        return None

# Vamos criar uma nova coluna que irá conter as siglas de 3 digitos
# de cada pais:
# df['residencia_iso_3']: Criação da nova coluna que irá receber
# os valores
# df['residencia']: Valores que irão compor a nova coluna
# apply: Função do pandas que tem como objetivo aplicar
# funções em cada linha de uma determinada coluna. A
# função recebe como argumento a função que será aplicada
# nas linhas.
# iso2_to_iso3: Função que será aplicada nas linhas da coluna
df['residencia_iso_3'] = df['residencia'].apply(iso2_to_iso3)

# Variável que irá conter um filtro que irá pegar apenas os dados
# do cargo de 'Data Scientist'
df_ds = df[df['cargo'] == 'Data Scientist']

# Vamoa agora agrupar os dados filtrados e calcular a média 
# do salário de pessoas que ocupam o cargo de Data Scientist.
# Após realizar o agrupamento e o cálculo da média, vamos criar
# uma coluna que irá conter o indice das linhas da coluna cargo
media_ds_pais = df_ds.groupby('residencia_iso_3')['usd'].mean().reset_index()

# Função que cria um mapa coroplético: Mapas cloropéticos são mapas
# onde as áreas geográficas (no nosso caso, os paises) são coloridas
# com base no valor de uma varoável estatistica (no seu caso, o salário
# médio). É a forma ideal de visualizar a distribuição de dados por região
fig = px.choropleth(
    
    # Dados que serão mapeados
    media_ds_pais,
    
    # Diz ao plotly qual coluna do dataframe contém os códigos de 
    # pais para identificar cada área.
    locations = 'residencia_iso_3',
    
    # Define qual coluna numérica será usada para determinar a cor do pais.
    color = 'usd',
    
    # Define a escala de cores.No nosso caso escolhemos a rdylgn (Red-Yellow-Green)
    color_continuous_scale='rdylgn',
    
    title = 'Salário Médio de Cientista de Dados por Pais',
    
    
    labels = {'usd': 'Salário Médio (USD)', 'residencia_iso_3': 'Pais'}
    
)


fig.show()


# Irá conter o conteúdo da coluna 4
with col_graf4:
    # Ura verificar se o dataset não está vázio
    if not df.empty:
        #  Irá filtrar o cargo de 'Data Scientist' do dataframe
        df_ds = df[df['cargo'] == 'Data Scientist']
        # Ira agrupar os dados por residencia, calcular a média
        # dos salarios em cada pais e criará uma coluna para os 
        # indices de cada pais
        media_ds_pais = df_ds.groupby('residencia_iso_3')['usd'].mean().reset_index()
        
        # Variável que irá conter a construção do mapa coroplético
        grafico_paises = px.choropleth(media_ds_pais,
            locations='residencia_iso_3',
            color='usd',
            color_continuous_scale='rdylgn',
            title='Salário médio de Cientista de Dados por país',
            labels={'usd': 'Salário médio (USD)', 'residencia_iso_3': 'País'})
        # Irá ajustar o texto do gráfico
        grafico_paises.update_layout(title_x=0.1)
        
        # Irá renderizar a coluna
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        
        # Mensagem que será exibida caso a construção do gráfico dê errado.
        st.warning("Nenhum dado para exibir no gráfico de países.") 

# --- Tabela de Dados Detalhados ---
st.subheader("Dados Detalhados")

# Ira exibir o dataframe no dashboard
st.dataframe(base_de_dados_filtrado)