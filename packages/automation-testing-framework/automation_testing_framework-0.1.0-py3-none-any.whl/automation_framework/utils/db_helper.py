import logging
from typing import Dict, List, Any, Optional, Union, Tuple

logger = logging.getLogger(__name__)

class DBHelper:
    """
    Helper class for database operations that provides a unified interface for different database types.
    Currently supports PostgreSQL and ClickHouse.
    """
    
    def __init__(self, db_type: str = 'postgres', 
                 host: Optional[str] = None, 
                 port: Optional[int] = None,
                 database: Optional[str] = None,
                 user: Optional[str] = None,
                 password: Optional[str] = None,
                 **kwargs):
        """
        Initialize the database helper.
        
        Args:
            db_type: The type of database ('postgres' or 'clickhouse')
            host: The database host
            port: The database port
            database: The database name
            user: The database user
            password: The database password
            **kwargs: Additional connection parameters
        """
        self.db_type = db_type.lower()
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.kwargs = kwargs
        self.connection = None
        
        # Initialize the appropriate database client
        if self.db_type == 'postgres':
            self._init_postgres()
        elif self.db_type == 'clickhouse':
            self._init_clickhouse()
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
    
    def _init_postgres(self) -> None:
        """
        Initialize a PostgreSQL connection.
        """
        try:
            import psycopg2
            import psycopg2.extras
            self._db_module = psycopg2
            self._extras_module = psycopg2.extras
        except ImportError:
            logger.error("psycopg2 library not found. Please install it with 'pip install psycopg2-binary'")
            raise ImportError("psycopg2 library not found. Please install it with 'pip install psycopg2-binary'")
        
        # Connection will be established when needed
    
    def _init_clickhouse(self) -> None:
        """
        Initialize a ClickHouse connection.
        """
        try:
            from clickhouse_driver import Client
            self._db_module = Client
        except ImportError:
            logger.error("clickhouse-driver library not found. Please install it with 'pip install clickhouse-driver'")
            raise ImportError("clickhouse-driver library not found. Please install it with 'pip install clickhouse-driver'")
        
        # Connection will be established when needed
    
    def connect(self) -> None:
        """
        Establish a connection to the database.
        """
        if self.connection:
            return
            
        try:
            if self.db_type == 'postgres':
                logger.info(f"Connecting to PostgreSQL database at {self.host}:{self.port}/{self.database}")
                self.connection = self._db_module.connect(
                    host=self.host,
                    port=self.port,
                    dbname=self.database,
                    user=self.user,
                    password=self.password,
                    **self.kwargs
                )
            elif self.db_type == 'clickhouse':
                logger.info(f"Connecting to ClickHouse database at {self.host}:{self.port}/{self.database}")
                self.connection = self._db_module(
                    host=self.host,
                    port=self.port,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    **self.kwargs
                )
        except Exception as e:
            logger.error(f"Failed to connect to {self.db_type} database: {str(e)}")
            raise
    
    def execute_query(self, query: str, params: Optional[Union[Tuple, Dict[str, Any], List[Any]]] = None) -> List[Dict[str, Any]]:
        """
        Execute a query and return the results.
        
        Args:
            query: The SQL query to execute
            params: The query parameters
            
        Returns:
            A list of dictionaries representing the query results
        """
        # Connect if not already connected
        if not self.connection:
            self.connect()
            
        try:
            logger.info(f"Executing query: {query}")
            logger.debug(f"Query parameters: {params}")
            
            if self.db_type == 'postgres':
                with self.connection.cursor(cursor_factory=self._extras_module.RealDictCursor) as cursor:
                    cursor.execute(query, params)
                    
                    # If the query is a SELECT, return the results
                    if cursor.description:
                        results = cursor.fetchall()
                        return [dict(row) for row in results]
                    
                    self.connection.commit()
                    return []
                    
            elif self.db_type == 'clickhouse':
                # For ClickHouse, the client returns results directly
                results = self.connection.execute(query, params or {})
                
                # Convert tuple results to dictionaries
                if results and cursor.description:
                    column_names = [col[0] for col in cursor.description]
                    return [dict(zip(column_names, row)) for row in results]
                    
                return []
                
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            if self.db_type == 'postgres':
                self.connection.rollback()
            raise
    
    def execute_many(self, query: str, params_list: List[Union[Tuple, Dict[str, Any], List[Any]]]) -> None:
        """
        Execute a query many times with different parameters.
        
        Args:
            query: The SQL query to execute
            params_list: A list of parameter sets
        """
        # Connect if not already connected
        if not self.connection:
            self.connect()
            
        try:
            logger.info(f"Executing query multiple times: {query}")
            
            if self.db_type == 'postgres':
                with self.connection.cursor() as cursor:
                    cursor.executemany(query, params_list)
                    self.connection.commit()
                    
            elif self.db_type == 'clickhouse':
                for params in params_list:
                    self.connection.execute(query, params)
                    
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            if self.db_type == 'postgres':
                self.connection.rollback()
            raise
    
    def close(self) -> None:
        """
        Close the database connection.
        """
        if self.connection:
            try:
                if self.db_type == 'postgres':
                    self.connection.close()
                # ClickHouse client doesn't need explicit closing
                logger.info(f"Closed connection to {self.db_type} database")
                
            except Exception as e:
                logger.error(f"Failed to close connection: {str(e)}")
                
            finally:
                self.connection = None
                
    def __enter__(self):
        """
        Support for with statement.
        """
        self.connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Support for with statement.
        """
        self.close()
