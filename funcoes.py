

# Resolvi criar esse arquivo com o objetivo de facilitar o carregamento e a renomeação do dataset nas próximas aulas. Vou usar a mesma lógica
# da aula anterior, porém em uma única função que irá carregar e
# renomear todo o dataset

# import da biblioteca pandas que irá carregar o dataset na memória 
# e manipulará os dados.
import pandas as pd

# Criação da função que irá carregar o dataset na mémória
# e renomear as colunas. Como eu acredito que usaremos sempre
# o mesmo arquivo, eu decidi não passar argumentos para a função
def carregar_dados():
    
    # Função di pandas que carrega o dataset na memória
    dados = pd.read_csv("https://raw.githubusercontent.com/guilhermeonrails/data-jobs/refs/heads/main/salaries.csv")
    
    # Função do pandas que renomeia as colunas do dataset. A função
    # recebe como parametro um dicionário contendo o nome original
    # da coluna e o nova nomenclatura (o novo nome que você quer colocar na coluna).
    dados.rename(columns={
    
    'work_year': 'ano',
    'experience_level': 'senioridade',
    'employment_type': 'Contrato',
    'job_title': 'cargo',
    'salary': 'salario',
    'salary_currency': 'moeda',
    'salary_in_usd': 'usd',
    'employee_residence': 'residencia',
    'remote_ratio': 'remoto',
    'company_location': 'empresa',
    'company_size': 'tamanho_empresa'
    }, inplace=True)

    
    # Renomeação das categorias das colunas: Basicamente, vamos criar
    # dicionários contendo o nome original de cada categoria e o seun
    # novo nome. Esses dicionários serão utilizados como argumento da função replace do pandas que tem como objetivo renomear valores
    # categóricos.
    renomear_senioridade = {
    
    'SE': 'Sênior',
    'MI': 'Pleno',
    'EN': 'Junior',
    'EX': 'Executivo'
    }
    
    dados['senioridade'] = dados['senioridade'].replace(renomear_senioridade)
    
    renomear_contrato = {
    
    'FT': 'Tempo Integral',
    'PT': 'Tempo Parcial',
    'FL': 'Freela',
    'CT': 'Contrato'
    }
    
    dados['Contrato'] = dados['Contrato'].replace(renomear_contrato)
    
    renomear_tamanho_empresa = {
    
    'M':'Médio Porte',
    'L': 'Grande Porte',
    'S': 'Pequeno Porte'
    }
    
    dados['tamanho_empresa'] = dados['tamanho_empresa'].replace(renomear_tamanho_empresa)
    
    renomear_remoto = {
    
    0:'Presencial',
    100: 'Remoto',
    50: 'Hibrido'
    }
    
    dados['remoto'] = dados['remoto'].replace(renomear_remoto)
    
    
    # Retorno da base de dados carregada e renomeada.
    return dados

