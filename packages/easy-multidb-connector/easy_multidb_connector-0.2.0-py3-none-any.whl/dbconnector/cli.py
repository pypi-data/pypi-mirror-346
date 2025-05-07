import click
from typing import Optional
from dbconnector import connect
from dbconnector.exceptions import DatabaseConnectionError

@click.group()
def cli():
    """DBConnector CLI - Ferramenta para testar conexões com bancos de dados"""
    pass

@cli.command()
@click.option('--type', required=True, help='Tipo de banco de dados (mysql, postgresql, etc.)')
@click.option('--host', help='Host do banco de dados')
@click.option('--port', type=int, help='Porta do banco de dados')
@click.option('--user', help='Usuário do banco de dados')
@click.option('--password', help='Senha do banco de dados')
@click.option('--database', help='Nome do banco de dados')
@click.option('--async', is_flag=True, help='Usar conexão assíncrona')
def test(type: str, host: Optional[str], port: Optional[int], 
         user: Optional[str], password: Optional[str], 
         database: Optional[str], async_: bool):
    """Testa uma conexão com o banco de dados"""
    params = {
        'host': host,
        'port': port,
        'user': user,
        'password': password,
        'database': database
    }
    # Remove parâmetros None
    params = {k: v for k, v in params.items() if v is not None}
    
    try:
        click.echo(f"Conectando ao banco {type}...")
        conn = connect(type, async_conn=async_, **params)
        click.echo("✅ Conexão estabelecida com sucesso!")
        
        if type in ['mysql', 'postgresql', 'sqlite', 'oracle', 'mssql']:
            cursor = conn.connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            click.echo(f"Teste de consulta retornou: {result[0]}")
        
        conn.close()
    except DatabaseConnectionError as e:
        click.echo(f"❌ Falha na conexão: {str(e)}", err=True)
    except Exception as e:
        click.echo(f"❌ Erro inesperado: {str(e)}", err=True)

def main():
    cli()

if __name__ == '__main__':
    main()