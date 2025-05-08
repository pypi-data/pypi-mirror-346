import logging
from typing import Dict, Any
from functools import wraps
from time import time
from .exceptions import DatabaseConnectionError
import threading
import asyncio

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_connection_params(params: Dict[str, Any], required: list) -> None:
    """Valida se os parâmetros obrigatórios estão presentes
    
    Args:
        params: Dicionário com parâmetros de conexão
        required: Lista de parâmetros obrigatórios
    
    Raises:
        ValueError: Se algum parâmetro obrigatório estiver faltando
    """
    missing = [param for param in required if param not in params]
    if missing:
        raise ValueError(f"Missing required parameters: {', '.join(missing)}")

def timing_decorator(func):
    """Decorador para medir o tempo de execução de métodos"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        logger.info(f"{func.__name__} executed in {end - start:.4f} seconds")
        return result
    return wrapper

def handle_database_errors(func):
    """Decorador para tratamento genérico de erros de banco de dados"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DatabaseConnectionError:
            raise
        except Exception as e:
            logger.error(f"Database operation failed: {str(e)}")
            raise DatabaseConnectionError(f"Operation failed: {str(e)}")
    return wrapper

class ConnectionPool:
    """Pool de conexões com suporte a operações assíncronas"""
    
    def __init__(self, connector_class, max_connections=5, async_conn=False, **kwargs):
        """
        Args:
            connector_class: Classe do conector (ex: MySQLConnector)
            max_connections: Número máximo de conexões no pool
            async_conn: Se True, gerencia conexões assíncronas
            **kwargs: Parâmetros de conexão
        """
        self.connector_class = connector_class
        self.max_connections = max_connections
        self.async_conn = async_conn
        self._pool = []
        self._in_use = {}
        self._kwargs = kwargs
        self._lock = threading.Lock()
        self._async_lock = asyncio.Lock() if async_conn else None

    def get_connection(self):
        """Obtém uma conexão do pool (síncrono)"""
        if self.async_conn:
            raise RuntimeError("Use get_async_connection() para conexões assíncronas")
        
        with self._lock:
            # Tenta reutilizar conexão fechada
            for conn_id, conn in list(self._in_use.items()):
                if not self._is_connection_active(conn):
                    self._in_use.pop(conn_id)
                    return self._get_or_create_connection(conn_id)
            
            # Cria nova conexão se possível
            if len(self._in_use) < self.max_connections:
                conn_id = len(self._pool)
                return self._get_or_create_connection(conn_id)
            
            raise DatabaseConnectionError("Maximum connections reached")

    async def get_async_connection(self):
        """Obtém uma conexão assíncrona do pool"""
        if not self.async_conn:
            raise RuntimeError("Pool não configurado para conexões assíncronas")
        
        async with self._async_lock:
            # Verifica conexões inativas
            for conn_id, conn in list(self._in_use.items()):
                if not await self._is_async_connection_active(conn):
                    self._in_use.pop(conn_id)
                    return await self._get_or_create_async_connection(conn_id)
            
            # Cria nova conexão
            if len(self._in_use) < self.max_connections:
                conn_id = len(self._pool)
                return await self._get_or_create_async_connection(conn_id)
            
            raise DatabaseConnectionError("Maximum connections reached")

    def _get_or_create_connection(self, conn_id):
        """Obtém ou cria uma conexão síncrona"""
        if conn_id < len(self._pool):
            conn = self._pool[conn_id]
        else:
            conn = self.connector_class(**self._kwargs)
            self._pool.append(conn)
        
        self._in_use[conn_id] = conn
        return conn

    async def _get_or_create_async_connection(self, conn_id):
        """Obtém ou cria uma conexão assíncrona"""
        if conn_id < len(self._pool):
            conn = self._pool[conn_id]
        else:
            conn = self.connector_class(**self._kwargs)
            await conn.connect(**self._kwargs)
            self._pool.append(conn)
        
        self._in_use[conn_id] = conn
        return conn

    def _is_connection_active(self, conn):
        """Verifica se uma conexão síncrona está ativa"""
        if hasattr(conn.connection, 'is_connected'):
            return conn.connection.is_connected()
        return True  # Assume ativa se não puder verificar

    async def _is_async_connection_active(self, conn):
        """Verifica se uma conexão assíncrona está ativa"""
        try:
            if hasattr(conn.connection, 'ping'):
                await conn.connection.ping()
                return True
            return True
        except:
            return False

    def release_connection(self, conn):
        """Libera uma conexão síncrona"""
        with self._lock:
            for conn_id, pooled_conn in list(self._in_use.items()):
                if pooled_conn == conn:
                    self._in_use.pop(conn_id)
                    break

    async def release_async_connection(self, conn):
        """Libera uma conexão assíncrona"""
        async with self._async_lock:
            for conn_id, pooled_conn in list(self._in_use.items()):
                if pooled_conn == conn:
                    self._in_use.pop(conn_id)
                    break

    def close_all(self):
        """Fecha todas as conexões síncronas"""
        with self._lock:
            for conn in self._pool:
                conn.close()
            self._pool = []
            self._in_use = {}

    async def close_all_async(self):
        """Fecha todas as conexões assíncronas"""
        async with self._async_lock:
            for conn in self._pool:
                await conn.close()
            self._pool = []
            self._in_use = {}