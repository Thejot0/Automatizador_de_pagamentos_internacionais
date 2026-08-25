import requests

from adm_logger.loggin import logger
from manipulacao_dados.banco_dados import BancoDados


class Api:
    def __init__(self, banco_dados):
        self.banco_dados = banco_dados
        self.lista_valores = []
        self.logger = logger
        

    def cotacao_moeda(self):
        try:

            self.banco_dados.cursor.execute(
                
                """
                SELECT moeda FROM faturas WHERE status = "PENDENTE"
                """
                )



            for moedas in self.banco_dados.cursor.fetchall():
                for moeda in moedas:
                    
                    cotacao = requests.get(
                        f'https://economia.awesomeapi.com.br/json/last/USD-{moeda}'
                        )
                    
                    valor_cota = cotacao.json()
                    

                    self.lista_valores.append(
                        {
                            "moeda": moeda,
                            "valor_cotacao": round(float(valor_cota[f'USD{moeda}']['bid']), 2)
                        }
                    )
            return self.lista_valores
        
        
        except requests.ConnectionError as erro:
            self.logger.error(f"Erro ao tentar se conectar a API: {erro}")
            raise
        
        except requests.ConnectTimeout as erro:
            self.logger.error(f"A API está demorando de responder: {erro}")
            raise

        except requests.RequestException as erro:
            self.logger.error(f"Houve um erro inesperado ao tentar se conectar com a API: {erro}")
            raise

        except Exception as erro:
            self.logger.exception(f"Houve um erro inesperado no codigo: {erro}")
            raise 


if __name__ == "__main__":
    b = BancoDados()
    a = Api(b)
    a.banco_dados.conectar_banco()
    a.cotacao_moeda()

    a.banco_dados.desconectar_banco()
    