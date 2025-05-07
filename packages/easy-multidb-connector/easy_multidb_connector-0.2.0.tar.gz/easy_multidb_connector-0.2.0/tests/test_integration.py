import unittest
import tempfile
from dbconnector import connect, DatabaseConnectionError
from dbconnector.utils import ConnectionPool

class TestIntegration(unittest.TestCase):
    """Testes de integração para o DBConnector"""
    
    def setUp(self):
        self.sqlite_db = tempfile.NamedTemporaryFile(suffix='.db').name
    
    def test_connect_factory_method(self):
        """Testa o método factory connect()"""
        with connect('sqlite', database=self.sqlite_db) as conn:
            cursor = conn.connection.cursor()
            cursor.execute("SELECT 1")
            self.assertEqual(cursor.fetchone()[0], 1)
    
    def test_unsupported_database_type(self):
        """Testa o tratamento de tipo de banco não suportado"""
        with self.assertRaises(ValueError):
            connect('unsupported_db', database='test')
    
    def test_connection_pool(self):
        """Testa o funcionamento básico do pool de conexões"""
        pool = ConnectionPool(
            type('TestConnector', (), {
                'connection': type('DummyConnection', (), {'is_connected': lambda self: True})
            }),
            max_connections=2
        )
        
        conn1 = pool.get_connection()
        conn2 = pool.get_connection()
        
        with self.assertRaises(DatabaseConnectionError):
            pool.get_connection()  # Deve falhar pois o pool está cheio
        
        pool.release_connection(conn1)
        conn3 = pool.get_connection()  # Deve funcionar após liberar uma conexão
        
        pool.close_all()

if __name__ == '__main__':
    unittest.main()