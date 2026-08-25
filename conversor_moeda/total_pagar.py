import pandas as pd

from adm_logger.loggin import logger
from manipulacao_dados.banco_dados import BancoDados
from tratamento_api.busca_api import Api


class FaturaV:
    def __init__(self):
        self.banco_dados = BancoDados()
        self.api_cotacao = Api(self.banco_dados)
        self.logger = logger
        

    def soma_valor_cota(self):
        try:

            valores = self.api_cotacao.cotacao_moeda()

            df_cota = pd.DataFrame(valores)
            planilha = pd.read_excel('tabela_completa_faturas.xlsx')

            planilha = planilha.drop(columns=["valor_cotacao"], errors="ignore")
            df_cota = df_cota.drop_duplicates(subset='moeda')

            juncao = pd.merge(
                planilha,
                df_cota,
                on="moeda",
                how="left"
            )

            juncao.insert(
                8,
                "valor_cotacao",
                juncao.pop("valor_cotacao")
            )

            juncao.to_excel(
                'tabela_completa_com_cotacao.xlsx',
                index=False,
                header=True
                )

            return 
            
        except TypeError as erro:
            self.logger.error(f"Houve um erro de tipo ao tentar somar valores: {erro}")
            raise

        except FileNotFoundError as erro:
            self.logger.error(f"Erro ao tentar abrir um arquivo ou diretório inexistente: {erro}")
            raise
        
        except Exception as erro:
            self.logger.exception(f"Houve um erro inesperado ao tentar juntar tabela no soma valores: {erro}")
            raise


    def adicionar_nova_tabela(self):
        try:
            tabela = pd.read_excel('tabela_completa_com_cotacao.xlsx')

            valor = tabela['valor_dolar']
            cota = tabela['valor_cotacao']

            soma = valor * cota

            tabela['valor_convertido'] = soma

            tabela.insert(
                        10,
                        "valor_convertido",
                        tabela.pop("valor_convertido")
                        )

            return tabela.to_excel(
                'tabela_final.xlsx',
                index=False,
                header=True,
                na_rep='SEM VALOR',
                
                )

        except KeyError as erro:
            self.logger.error(f"Erro de chave na def de somar valor: {erro}")
            raise

        except FileNotFoundError as erro:
            self.logger.error(f"Erro ao tentar abrir um arquivo ou diretório inexistente: {erro}")
            raise

        except Exception as erro:
            self.logger.exception(f"Houve um erro inesperado ao tentar juntar tabela no soma valores: {erro}")
            raise



if __name__ == "__main__":
    a = FaturaV()
    a.banco_dados.conectar_banco()
    a.soma_valor_cota()
    a.adicionar_nova_tabela()
    a.banco_dados.desconectar_banco()
    