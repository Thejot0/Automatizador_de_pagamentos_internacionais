import os

import pandas as pd

from adm_logger.loggin import logger
from manipulacao_dados.banco_dados import BancoDados


class DadosPlanilha:
    def __init__(self):
        self.dados_db = BancoDados()
        self.planilha_completa = None
        self.logger = logger


    def print_planilha_clientes(self):
        try:

            print(pd.read_excel('faturas_clientes.ods'))

        except FileNotFoundError as erro:
            self.logger.error(f"Erro ao tentar abrir planilha de faturas: {erro}")

        except Exception as erro:
            self.logger.exception(f"Houve um erro inesperado ao tentar abrir a planilha de fatura: {erro}")



    def juncao_dados(self):

        try:
            
            dados_db = pd.read_sql(

                """
                SELECT * FROM faturas
                WHERE status = 'PENDENTE' AND id > 0
                """,
                self.dados_db.conexao
            )
                


            planilha_faturas = pd.read_excel('faturas_clientes.ods')
            
        
            juncao = pd.merge(
                dados_db,
                planilha_faturas.drop(columns=['id']),
                on='Proprietario',
                how='left'
            )

            juncao.to_excel(
                'tabela_completa_faturas.xlsx',
                index=False,
                header=True,
                na_rep="SEM VALOR",
        
            )
        
        except FileNotFoundError as erro:
            self.logger.error(f"Erro ao tentar abrir planilha: {erro}")
            raise
            
        except Exception as erro:
            self.logger.exception(f"Houve um erro inesperado ao tentar juntar dados: {erro}")
            raise


    def planilha_de_faturas(self):
           print(pd.read_excel('tabela_completa_faturas.xlsx'))
        

if __name__  == "__main__":
    banco = DadosPlanilha()
    banco.dados_db.conectar_banco()
    banco.juncao_dados()
    banco.planilha_de_faturas()
    banco.dados_db.desconectar_banco()