from __future__ import annotations
from typing import Type, Dict, Any, Optional, Union, List
import sqlite3
import mysql.connector
import psycopg2
import cx_Oracle
import pyodbc
import logging
from abc import ABC, abstractmethod
from typing_extensions import Self
from .utils import validate_connection_params, timing_decorator
from .exceptions import DatabaseConnectionError


logger = logging.getLogger(__name__)


class BaseConnector(ABC):
    """Classe base abstrata para todos os conectores"""
    
    def __init__(self, **kwargs):
        self.connection: Any = None
        self.connect(**kwargs)
    
    @abstractmethod
    def connect(self, **kwargs) -> None:
        """Estabelece a conexão com o banco de dados"""
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Fecha a conexão com o banco de dados"""
        pass
    
    def __enter__(self) -> Self:
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
    
    def __del__(self) -> None:
        self.close()

# Bancos SQL
class MySQLConnector(BaseConnector):
    """Conector para MySQL"""
    
    def connect(self, **kwargs) -> None:
        try:
            import mysql.connector
            required = ['host', 'user', 'password']
            validate_connection_params(kwargs, required)
            self.connection = mysql.connector.connect(**kwargs)
        except ImportError:
            raise ImportError("mysql-connector-python is required. Install with: pip install mysql-connector-python")
        except Exception as e:
            raise DatabaseConnectionError(f"MySQL connection error: {str(e)}")
    
    def close(self) -> None:
        if self.connection and self.connection.is_connected():
            self.connection.close()

class AsyncMySQLConnector(BaseConnector):
    """Conector assíncrono para MySQL"""
    
    async def connect(self, **kwargs) -> None:
        try:
            import aiomysql
            required = ['host', 'user', 'password']
            validate_connection_params(kwargs, required)
            self.connection = await aiomysql.connect(**kwargs)
        except ImportError:
            raise ImportError("aiomysql is required. Install with: pip install aiomysql")
        except Exception as e:
            raise DatabaseConnectionError(f"Async MySQL connection error: {str(e)}")
    
    async def close(self) -> None:
        if self.connection:
            self.connection.close()
            await self.connection.wait_closed()
            
                        

class PostgreSQLConnector(BaseConnector):
    """Conector para PostgreSQL"""
    
    def connect(self, **kwargs) -> None:
        try:
            import psycopg2
            required = ['host', 'user', 'password', 'database']
            validate_connection_params(kwargs, required)
            self.connection = psycopg2.connect(**kwargs)
        except ImportError:
            raise ImportError("psycopg2 is required. Install with: pip install psycopg2")
        except Exception as e:
            raise DatabaseConnectionError(f"PostgreSQL connection error: {str(e)}")
    
    def close(self) -> None:
        if self.connection and not self.connection.closed:
            self.connection.close()

class AsyncPostgreSQLConnector(BaseConnector):
    """Conector assíncrono para PostgreSQL"""
    
    async def connect(self, **kwargs) -> None:
        try:
            import asyncpg
            required = ['host', 'user', 'password', 'database']
            validate_connection_params(kwargs, required)
            self.connection = await asyncpg.connect(**kwargs)
        except ImportError:
            raise ImportError("asyncpg is required. Install with: pip install asyncpg")
        except Exception as e:
            raise DatabaseConnectionError(f"Async PostgreSQL connection error: {str(e)}")
    
    async def close(self) -> None:
        if self.connection:
            await self.connection.close()            
                                                
class SQLiteConnector(BaseConnector):
    # Conector para SQLite
    
    def connect(self, **kwargs):
        try:
            if 'database' not in kwargs:
                raise ValueError("SQLite requires 'database' parameter")         
            self.connection = sqlite3.connect(kwargs['database'])
        except Exception as e:
            raise DatabaseConnectionError(f"SQLite connection error: {str(e)}")

class OracleConnector(BaseConnector):
    "conector para Oracle"
    
    def connect(self, **kwargs):
        try:
            self.connection = cx_Oracle.connect(**kwargs)
        except Exception as e:
            raise DatabaseConnectionError(f"Oracle connection error: {str(e)}")

class MSSQLConnector(BaseConnector):
    # Conector para Microsoft SQL Server
    
    def connect(self, **kwargs):
        try:
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={kwargs.get('host')};"
                f"DATABASE={kwargs.get('database')};"
                f"UID={kwargs.get('user')};"
                f"PWD={kwargs.get('password')}"
            )            
            self.connection = pyodbc.connect(conn_str)
        except Exception as e:
            raise DatabaseConnectionError(f"MSSQL connection error: {str(e)}")

# Bancos NoSQL
class MongoDBConnector(BaseConnector):
    """Conector para MongoDB"""
    
    def connect(self, **kwargs) -> None:
        try:
            from pymongo import MongoClient
            self.connection = MongoClient(**kwargs)
            # Testa a conexão
            self.connection.admin.command('ismaster')
        except ImportError:
            raise ImportError("pymongo is required. Install with: pip install pymongo")
        except Exception as e:
            raise DatabaseConnectionError(f"MongoDB connection error: {str(e)}")
    
    def close(self) -> None:
        if self.connection:
            self.connection.close()

class CassandraConnector(BaseConnector):
    """Conector para Apache Cassandra"""
    
    def connect(self, **kwargs) -> None:
        try:
            from cassandra.cluster import Cluster
            contact_points = kwargs.pop('hosts', ['localhost'])
            if isinstance(contact_points, str):
                contact_points = [contact_points]
            
            self.cluster = Cluster(contact_points, **kwargs)
            self.connection = self.cluster.connect()
            
            # Testa a conexão
            self.connection.execute("SELECT release_version FROM system.local")
        except ImportError:
            raise ImportError("cassandra-driver is required. Install with: pip install cassandra-driver")
        except Exception as e:
            raise DatabaseConnectionError(f"Cassandra connection error: {str(e)}")
    
    def close(self) -> None:
        if hasattr(self, 'cluster'):
            self.cluster.shutdown()
                        
class ElasticsearchConnector(BaseConnector):
    """Conector para Elasticsearch"""
    
    def connect(self, **kwargs) -> None:
        try:
            from elasticsearch import Elasticsearch
            self.connection = Elasticsearch(**kwargs)
            # Testa a conexão
            if not self.connection.ping():
                raise DatabaseConnectionError("Could not connect to Elasticsearch")
        except ImportError:
            raise ImportError("elasticsearch is required. Install with: pip install elasticsearch")
        except Exception as e:
            raise DatabaseConnectionError(f"Elasticsearch connection error: {str(e)}")
    
    def close(self) -> None:
        if self.connection:
            self.connection.close()

class AsyncElasticsearchConnector(BaseConnector):
    """Conector assíncrono para Elasticsearch"""
    
    async def connect(self, **kwargs) -> None:
        try:
            from aioelasticsearch import Elasticsearch
            self.connection = Elasticsearch(**kwargs)
            # Testa a conexão
            if not await self.connection.ping():
                raise DatabaseConnectionError("Could not connect to Elasticsearch")
        except ImportError:
            raise ImportError("aioelasticsearch is required. Install with: pip install aioelasticsearch")
        except Exception as e:
            raise DatabaseConnectionError(f"Async Elasticsearch connection error: {str(e)}")
    
    async def close(self) -> None:
        if self.connection:
            await self.connection.close()         

# ORM Básico
class DatabaseModel:
    """Classe base para modelos de banco de dados"""
    
    @classmethod
    def get_table_name(cls) -> str:
        return getattr(cls, '__tablename__', cls.__name__.lower() + 's')
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        return cls(**data)
    
    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
 
class RedisConnector(BaseConnector):
    """Conector para Redis"""
    
    def connect(self, **kwargs):
        try:
            import redis
            self.connection = redis.Redis(**kwargs)
            # Testa a conexão
            self.connection.ping()
        except Exception as e:
            raise DatabaseConnectionError(f"Redis connection error: {str(e)}")
    
    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None        
            
class AsyncRedisConnector(BaseConnector):
    """Conector assíncrono para Redis"""
    
    async def connect(self, **kwargs) -> None:
        try:
            import aioredis
            self.connection = await aioredis.from_url(
                f"redis://{kwargs.get('host', 'localhost')}:{kwargs.get('port', 6379)}",
                db=kwargs.get('db', 0),
                password=kwargs.get('password')
            )
            # Testa a conexão
            await self.connection.ping()
        except ImportError:
            raise ImportError("aioredis is required. Install with: pip install aioredis")
        except Exception as e:
            raise DatabaseConnectionError(f"Async Redis connection error: {str(e)}")
    
    async def close(self) -> None:
        if self.connection:
            await self.connection.close()            
        

class SQLModel(DatabaseModel):
    """Modelo para bancos SQL"""
    
    @classmethod
    @timing_decorator
    def create_table(cls, connector: BaseConnector) -> None:
        """Cria a tabela no banco de dados"""
        if not hasattr(cls, '__fields__'):
            raise AttributeError("Model must define __fields__")
        
        fields_sql = ", ".join(
            f"{name} {type_def}" for name, type_def in cls.__fields__.items()
        )
        sql = f"CREATE TABLE IF NOT EXISTS {cls.get_table_name()} ({fields_sql})"
        
        cursor = connector.connection.cursor()
        cursor.execute(sql)
        connector.connection.commit()
    
    @classmethod
    @timing_decorator
    def insert(cls, connector: BaseConnector, data: Union[Self, Dict[str, Any]]) -> Any:
        """Insere um registro no banco de dados"""
        if isinstance(data, cls):
            data = data.to_dict()
        
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        sql = f"INSERT INTO {cls.get_table_name()} ({columns}) VALUES ({placeholders})"
        
        cursor = connector.connection.cursor()
        cursor.execute(sql, list(data.values()))
        connector.connection.commit()
        return cursor.lastrowid        


def connect(db_type: str, async_conn: bool = False, **kwargs) -> BaseConnector:
    """
    Factory method para criar conexões com diferentes bancos de dados
    
    Args:
        db_type: Tipo de banco de dados (mysql, postgresql, sqlite, oracle, mssql, 
                 mongodb, redis, cassandra, elasticsearch)
        async_conn: Se True, retorna um conector assíncrono (quando disponível)
        **kwargs: Parâmetros de conexão específicos para cada banco de dados
    
    Returns:
        Instância do conector apropriado
    
    Raises:
        DatabaseConnectionError: Se a conexão falhar
        ValueError: Se o tipo de banco de dados não for suportado
    """
    connector_map = {
        'mysql': AsyncMySQLConnector if async_conn else MySQLConnector,
        'postgresql': AsyncPostgreSQLConnector if async_conn else PostgreSQLConnector,
        'sqlite': SQLiteConnector,
        'oracle': OracleConnector,
        'mssql': MSSQLConnector,
        'mongodb': MongoDBConnector,
        'redis': AsyncRedisConnector if async_conn else RedisConnector,
        'cassandra': CassandraConnector,
        'elasticsearch': AsyncElasticsearchConnector if async_conn else ElasticsearchConnector
    }
    
    db_type = db_type.lower()
    if db_type not in connector_map:
        raise ValueError(f"Unsupported database type: {db_type}. Supported types: {list(connector_map.keys())}")
    
    return connector_map[db_type](**kwargs)                         
