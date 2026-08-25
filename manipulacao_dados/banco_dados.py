import os

import mysql.connector
from dotenv import load_dotenv

from adm_logger.loggin import logger


class BancoDados: 
    def __init__(self):
        self.logger = logger
        self.conexao = None
        self.cursor = None

    
    def conectar_banco(self):

        load_dotenv()

        SENHA_DB = os.getenv('DB_SENHA')
        DB_HOST = os.getenv('HOST_DB')
        DB_NOME = os.getenv('DATABASE')
        PORT_DB = os.getenv('PORT')

        try:

            self.conexao = mysql.connector.connect(
                user = "root",
                password =SENHA_DB,
                host = DB_HOST,
                database = DB_NOME,
                port=PORT_DB
            )
            
            self.cursor = self.conexao.cursor()
            self.logger.info('O banco de dados foi conectado!!!')
            return self.conexao

        except AttributeError as erro:
            self.logger.error(f'Houve um erro de atributo: {erro}')

        except ValueError as erro:
            self.logger.exception(f'Erro ao adicionar constante: {erro}')  # noqa: TRY401

        except Exception as erro:
            self.logger.exception(f'Houve um erro inesperado ao tentar se conectar ao banco de dados: {erro}')  # noqa: TRY401




    def desconectar_banco(self):
        try:

            self.cursor.close()
            self.conexao.close()
            self.logger.info('Banco de dados desconectado')

        except Exception as erro:
            self.logger.exception(f'Houve um erro inesperado ao tentar fechar conexão com o banco: {erro}')  # noqa: TRY401



    def clientes_pendentes(self):
        try:
            self.cursor.execute(

                """ 
                SELECT * FROM faturas WHERE status = "PENDENTE"
                """
            )

            return self.cursor.fetchall()
            

        except Exception as erro:
            self.logger.exception(f'Aconteceu um erro inesperado ao tentar consultar dados do banco de dados: {erro}')  # noqa: TRY401



if __name__ == "__main__":
    conect = BancoDados()

    conect.conectar_banco()
    print(conect.clientes_pendentes())
    conect.desconectar_banco()
