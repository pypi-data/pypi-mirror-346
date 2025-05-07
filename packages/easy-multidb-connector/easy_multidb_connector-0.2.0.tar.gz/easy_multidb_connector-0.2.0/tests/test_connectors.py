import unittest
import sqlite3
import tempfile
from dbconnector import (
    MySQLConnector,
    PostgreSQLConnector,
    SQLiteConnector,
    OracleConnector,
    MSSQLConnector,
    DatabaseConnectionError
)

class TestConnectors(unittest.TestCase):
    """Testes unitários para os conectores"""
    
    def setUp(self):
        # Configura um banco SQLite em memória para testes
        self.sqlite_db = tempfile.NamedTemporaryFile(suffix='.db').name
    
    def test_sqlite_connector_success(self):
        """Testa conexão bem-sucedida com SQLite"""
        conn = SQLiteConnector(database=self.sqlite_db)
        self.assertIsInstance(conn.connection, sqlite3.Connection)
        conn.close()
    
    def test_sqlite_connector_failure(self):
        """Testa falha na conexão com SQLite"""
        with self.assertRaises(DatabaseConnectionError):
            SQLiteConnector(database="/caminho/inexistente/test.db")
    
    def test_mysql_connector_invalid_credentials(self):
        """Testa credenciais inválidas para MySQL"""
        with self.assertRaises(DatabaseConnectionError):
            MySQLConnector(
                host="localhost",
                user="usuario_inexistente",
                password="senha_errada",
                database="banco_inexistente"
            )
    
    def test_postgresql_connector_invalid_credentials(self):
        """Testa credenciais inválidas para PostgreSQL"""
        with self.assertRaises(DatabaseConnectionError):
            PostgreSQLConnector(
                host="localhost",
                user="usuario_inexistente",
                password="senha_errada",
                database="banco_inexistente"
            )
    
    def test_connector_context_manager(self):
        """Testa o uso do conector como context manager"""
        with SQLiteConnector(database=self.sqlite_db) as conn:
            self.assertIsInstance(conn.connection, sqlite3.Connection)
        
        # Verifica se a conexão foi fechada
        with self.assertRaises(sqlite3.ProgrammingError):
            conn.connection.cursor()

if __name__ == '__main__':
    unittest.main()