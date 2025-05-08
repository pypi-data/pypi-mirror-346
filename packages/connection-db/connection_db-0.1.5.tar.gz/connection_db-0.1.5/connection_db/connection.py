from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional, Type, Any

from exceptions_db import DatabaseConnectionError, SessionError


class DBConnection:
    """Database connection manager supporting multiple database types.
    
    Example connection strings:
    -------------------------
    SQL Server:
        mssql+pymssql://username:password@hostname:port/database_name
        mssql+pyodbc://username:password@hostname:port/database_name?driver=ODBC+Driver+17+for+SQL+Server
    
    MySQL:
        mysql+pymysql://username:password@hostname:port/database_name
        mysql://username:password@hostname:port/database_name
    
    PostgreSQL:
        postgresql://username:password@hostname:port/database_name
        postgresql+psycopg2://username:password@hostname:port/database_name
    
    MongoDB (coming soon):
        mongodb://username:password@hostname:port/database_name
    """
    def __init__(
        self,
        connection_string: str,
        sql_server: bool = False,
        mysql: bool = False,
        postgres: bool = False,
        mongodb: bool = False,
        orm_mapped: Optional[Type] = None
    ):
        self.connection_string = connection_string
        self.engine = None
        self.session: Optional[Session] = None
        self.table = orm_mapped

        if any([sql_server, mysql, postgres]):
            try:
                self.engine = create_engine(
                    self.connection_string,
                    echo=False
                )
                # Test the connection
                with self.engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
            except Exception as e:
                error_msg = str(e).lower()
                if "login failed" in error_msg or "authentication failed" in error_msg:
                    raise DatabaseConnectionError("Authentication failed. Check your credentials.")
                elif "timeout" in error_msg:
                    raise DatabaseConnectionError("Connection timed out. Check if the server is reachable.")
                elif "database" in error_msg and "not exist" in error_msg:
                    raise DatabaseConnectionError("Database does not exist.")
                else:
                    raise DatabaseConnectionError(f"Failed to connect to database: {str(e)}")
        elif mongodb:
            raise NotImplementedError("MongoDB support coming soon")
        else:
            raise ValueError("Database type not specified")

    def get_engine(self):
        return self.engine

    def __enter__(self):
        try:
            local_session = sessionmaker(bind=self.engine)
            self.session = local_session()
            return self
        except Exception as e:
            raise SessionError(f"Failed to create session: {str(e)}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()
