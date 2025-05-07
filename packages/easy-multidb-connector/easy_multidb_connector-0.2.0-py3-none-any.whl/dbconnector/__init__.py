from .connectors import (
    # Conectores SQL
    connect,
    MySQLConnector,
    PostgreSQLConnector,
    SQLiteConnector,
    OracleConnector,
    MSSQLConnector,
    
    # Conectores NoSQL
    MongoDBConnector,
    RedisConnector,
    CassandraConnector,
    ElasticsearchConnector,
    
    # Conectores Assíncronos
    AsyncMySQLConnector,
    AsyncPostgreSQLConnector,
    AsyncRedisConnector,
    AsyncElasticsearchConnector,
    
    # ORM
    SQLModel,
    DatabaseModel,
    
    # Exceções
    DatabaseConnectionError
)

from .utils import ConnectionPool  # Importação correta do ConnectionPool

__all__ = [
    # Função principal
    'connect',
    
    # SQL
    'MySQLConnector',
    'PostgreSQLConnector',
    'SQLiteConnector',
    'OracleConnector',
    'MSSQLConnector',
    
    # NoSQL
    'MongoDBConnector',
    'RedisConnector',
    'CassandraConnector',
    'ElasticsearchConnector',
    
    # Assíncrono
    'AsyncMySQLConnector',
    'AsyncPostgreSQLConnector',
    'AsyncRedisConnector',
    'AsyncElasticsearchConnector',
    
    # ORM
    'SQLModel',
    'DatabaseModel',
    
    # Utilitários
    'ConnectionPool',  # Agora corretamente importado de utils.py
    
    # Exceções
    'DatabaseConnectionError'
]

__version__ = '0.2.0'  # Atualizado para 0.2.0 devido às novas funcionalidades