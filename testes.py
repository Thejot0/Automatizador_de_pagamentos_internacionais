from adm_logger.loggin import logger
from conversor_moeda.total_pagar import FaturaV
from manipulacao_dados.banco_dados import BancoDados
from manipulacao_planilha.dados_planilha import DadosPlanilha
from tratamento_api.busca_api import Api


def test_bot():
    dados = BancoDados()
    dados.conectar_banco()
    
    try:
        planilha = DadosPlanilha()
        planilha.juncao_dados()

    
        api = Api(dados)
        api.cotacao_moeda()

        conversor = FaturaV()
        conversor.soma_valor_cota()
        conversor.adicionar_nova_tabela()

    finally:
        dados.desconectar_banco()



if __name__ == "__main__":
   s

