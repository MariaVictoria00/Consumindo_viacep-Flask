from flask import  Blueprint, render_template, request, flash, redirect, url_for,abort
import json
import requests
import pandas as pd
import numpy as np

views = Blueprint('views', __name__)

## -- PÁGINA INICIAL --
@views.route('/')
def home():
    """
    Rota inicial.
    Não é necessário modificar nada nessa função
    """
    return render_template('home.html')


@views.route('/clientes')
def clientes():
    """
    Rota para aba de clientes. Mostra na tela uma representação do csv de clientes
    Não é necessário modificar nada nessa função
    """
    df = pd.read_csv('data/clientes.csv', dtype=object, sep=';')
    df = df.replace(np.nan, '', regex=True)
    return render_template('clientes.html', df=df, titles=df.columns.values)


## -- CADASTRO --
@views.route('/cadastro', methods=['GET','POST'])
def cadastro():
    """
    Função para cadastro de novos clientes. Deverá pegar as informações do forms e salvar numa nova linha no csv.
    Necessário também salvar as informações de endereço provindas da API de CEP
    """
    ## TODO pegar informações do forms
    nome=request.form.get('nome')
    sobrenome=request.form.get('sobrenome')
    email=request.form.get('email')
    cep=request.form.get('cep')
    
    try:
           ## TODO buscar informações de endereço da API do ViaCEP (https://viacep.com.br/)
            r= requests.get('https://viacep.com.br/ws//{}/json/'.format(cep))
            dados_json=r.json()

            logradouro=dados_json['logradouro']
            complemento=dados_json['complemento']
            bairro=dados_json['bairro']
            localidade=dados_json['localidade']
            uf=dados_json['uf']
            ibge=dados_json['ibge']
            gia=dados_json['gia']
            ddd=dados_json['ddd']
            siafi=dados_json['siafi']

            ## TODO criar nova linha no arquivo csv
            data=(nome,sobrenome,email,cep,logradouro,complemento,bairro,localidade,
            uf,ibge,gia,ddd,siafi)
            dataframe = pd.DataFrame(data)
            dataframe.to_csv("data/clientes.csv",index=False, mode='a',header=False)

    except:
            return render_template('cadastro.html')

        
    return render_template('cadastro.html')


## -- CONSULTA CEP --
@views.route('/consulta-cep', methods=['GET','POST'])
def consulta_cep():
    ## TODO pegar CEP do forms
    cep=request.form.get('cep')

    ## TODO buscar informações de endereço da API do ViaCEP (https://viacep.com.br/
    try:
            r= requests.get('https://viacep.com.br/ws//{}/json/'.format(cep))
            dados_json=r.json()

            ## TODO mostrar no html as informações obtidas
            cep_result=dados_json['cep']
            logradouro_result=dados_json['logradouro']
            complemento_result=dados_json['complemento']
            bairro_result=dados_json['bairro']
            uf_result=dados_json['uf']
            ibge_result=dados_json['ibge']
            gia_result=dados_json['gia']
            ddd_result=dados_json['ddd']
            siafi_result=dados_json['siafi']

    except:
                return render_template('consulta_cep.html')

    return render_template('consulta_cep.html',cep=cep_result,logradouro=logradouro_result,
        complemento=complemento_result, bairro=bairro_result,uf=uf_result,ibge=ibge_result,
        gia=gia_result,ddd=ddd_result,siafi=siafi_result)
