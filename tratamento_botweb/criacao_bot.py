import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from adm_logger.loggin import logger
from manipulacao_dados.banco_dados import BancoDados


class WebBot:
    def __init__(self):
        self.banco_dados = BancoDados()
        self.bot = None
        self.logger = logger




    def atualizar_status(self, id_fatura):

        self.banco_dados.conectar_banco()
        try:
            
            sql = """
                UPDATE faturas
                SET status = %s
                WHERE id = %s
                """

            self.banco_dados.cursor.execute(sql, 
                                            ('PAGO', id_fatura)
                                            )

            self.banco_dados.conexao.commit()

            self.logger.info(
                f"Status da fatura {id_fatura} atualizado para PAGO"
                )

            self.banco_dados.desconectar_banco()
            return True
    
        except Exception as erro:
            self.logger.exception(f'Houve um erro inesperado ao tentar atualizar status do banco de dados {erro}')
            raise


    def cadastro_clientes(self):

        dados = pd.read_excel("tabela_final.xlsx")

        for _, dados_clientes in dados.iterrows():
            try:
                if dados_clientes['status'] == 'PENDENTE':

                    self.bot.get("https://forms.gle/DY7RzsjNxfdcZQM4A")
                    self.bot = webdriver.Chrome()

                    nome_cliente = WebDriverWait(self.bot, 30).until(
                                    EC.presence_of_element_located((
                                        By.CSS_SELECTOR, 'input[aria-labelledby="i1 i4"]'
                                    ))
                                        )
                    nome_cliente.send_keys(dados_clientes['Proprietario'])

                    

                    fatura_dolar =  WebDriverWait(self.bot, 30).until(
                                    EC.presence_of_element_located((
                                        By.CSS_SELECTOR, 'input[aria-labelledby="i6 i9"]'
                                    ))
                                        )
                    fatura_dolar.send_keys(dados_clientes['valor_dolar'])



                    valor_convertido =  WebDriverWait(self.bot, 30).until(
                                    EC.presence_of_element_located((
                                        By.CSS_SELECTOR, 'input[aria-labelledby="i11 i14"]'
                                    ))
                    )
                    valor_convertido.send_keys(dados_clientes['valor_convertido'])



                    nome_banco = WebDriverWait(self.bot, 30).until(
                                    EC.presence_of_element_located((
                                        By.CSS_SELECTOR, 'input[aria-labelledby="i16 i19"]'
                                    ))
                    )
                    nome_banco.send_keys(dados_clientes['Banco'])



                    nome_agencia =  WebDriverWait(self.bot, 30).until(
                                        EC.presence_of_element_located((
                                            By.CSS_SELECTOR, 'input[aria-labelledby="i21 i24"]'
                                        ))
                    )

                    nome_agencia.send_keys(dados_clientes['Agencia'])


                    numero_conta = WebDriverWait(self.bot, 30).until(
                                        EC.presence_of_element_located((
                                            By.CSS_SELECTOR, 'input[aria-labelledby="i26 i29"]'
                                        ))
                    )
                    numero_conta.send_keys(dados_clientes['Conta'])



                    forma_pagamento = WebDriverWait(self.bot, 30).until(
                                        EC.presence_of_element_located((
                                                        By.CSS_SELECTOR, 'input[aria-labelledby="i31 i34"]'
                                        ))
                    )    
                    forma_pagamento.send_keys(dados_clientes['Metodo'])
                    self.logger.info(f"Processando cadastro do proprietario: {dados_clientes['id']} | {dados_clientes['Proprietario']}")


                else:
                    self.logger.info('Nenhum status pendente. Nenhum cliente foi cadastrado')
                    print('Nenhum status pendente. Nenhum cliente foi cadastrado')
                    return
                

            except TimeoutError:
                self.logger.exception(f'Elemento do proprietario: {dados_clientes['id']} | {dados_clientes["Proprietario"]} não encontrado')
                raise 

            except ConnectionError:
                self.logger.error('Erro de conexão.\n',
                                f'Não foi possivel cadastrar cliente: {dados_clientes["id"]} | {dados_clientes["Proprietario"]}')
                raise 

            except Exception as erro:
                self.logger.exception(f'Houve um erro desconhecido ao tentar cadastrar {dados_clientes["id"]} | {dados_clientes["Proprietario"]}. Erro: {erro}')  # noqa: TRY401
                raise


            try:
                WebDriverWait(self.bot, 30).until(
                                EC.element_to_be_clickable((
                                    By.CSS_SELECTOR, 'span[class="l4V7wb Fxmcue"]'
                                    ))
                                ).click()

                self.atualizar_status(dados_clientes['id'])
                self.logger.info(f'Status do cliente {dados_clientes["id"]} | {dados_clientes["Proprietario"]} atualizado com successo!!')
                self.logger.info(f'Cliente {dados_clientes["id"]} | {dados_clientes["Proprietario"]} cadastrado com sucesso!!')

                dados.loc[_, "status"] = "PAGO"
                dados.to_excel("tabela_final.xlsx", index=False, header=True)
                self.logger.info(f'Status do cliente {dados_clientes["id"]} | {dados_clientes["Proprietario"]} Atualizada com sucesso!!')


                WebDriverWait(self.bot, 30).until(
                    EC.element_to_be_clickable((
                        By.LINK_TEXT, 'Enviar outra resposta'
                        ))
                    ).click()

            except TimeoutError as erro:
                self.logger.error(f'Elemento não encontrado {erro}')
                raise

            except ConnectionError:
                self.logger.error('Erro ao tentar finalizar cadastro de cliente\n',
                                'Conexão caiu')


if __name__ == "__main__":
    site = WebBot()
    site.cadastro_clientes()