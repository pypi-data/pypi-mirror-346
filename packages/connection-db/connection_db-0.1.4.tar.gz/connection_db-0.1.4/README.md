# Connection DB

Uma biblioteca Python flexível e fácil de usar para gerenciar conexões com diferentes tipos de bancos de dados usando SQLAlchemy.

## Características

- Suporte para múltiplos bancos de dados:
  - SQL Server
  - MySQL
  - PostgreSQL
  - MongoDB (em breve)
- Gerenciamento automático de conexões usando context manager
- Integração com SQLAlchemy ORM
- Tratamento de erros robusto
- Interface consistente para diferentes bancos de dados

## Instalação

```bash
pip install connection-db
```

## Requisitos

- Python >= 3.7
- SQLAlchemy >= 1.4.0
- Drivers específicos para cada banco de dados:
  - SQL Server: pymssql >= 2.2.0
  - PostgreSQL: psycopg2-binary >= 2.9.0
  - MySQL: pymysql >= 1.0.0

## Uso Básico

### Conexão Simples

```python
from connection_db import DBConnection

# Usando com SQL Server
with DBConnection(
    sql_server=True,
    connection_string="mssql+pymssql://user:password@server/database"
) as db:
    db.session.execute(text("SELECT * FROM users"))
    db.session.commit()
```

### Uso com ORM

```python
from connection_db import DBConnection
from sqlalchemy import select
from your_models import User

with DBConnection(
    sql_server=True,
    connection_string="mssql+pymssql://user:password@server/database",
    orm_mapped=User
) as db:
    query = select(db.table).where(db.table.name == "John")
    result = db.session.execute(query)
    db.session.commit()
```

### Padrão Repository

```python
from connection_db import DBConnection

class BaseRepository:
    def __init__(self):
        self.connection_string = "mssql+pymssql://user:password@server/database"
        self.db_type = "sql_server"

    def get_connection(self, orm_model=None):
        return DBConnection(
            connection_string=self.connection_string,
            sql_server=(self.db_type == "sql_server"),
            orm_mapped=orm_model
        )
```

## Strings de Conexão

### SQL Server

```bash
mssql+pymssql://username:password@hostname:port/database_name
mssql+pyodbc://username:password@hostname:port/database_name?driver=ODBC+Driver+17+for+SQL+Server
```

### MySQL

```bash
mysql+pymysql://username:password@hostname:port/database_name
mysql://username:password@hostname:port/database_name
```

### PostgreSQL

```bash
postgresql://username:password@hostname:port/database_name
postgresql+psycopg2://username:password@hostname:port/database_name
```

## Tratamento de Erros

A biblioteca inclui classes de exceção personalizadas para melhor tratamento de erros:

- `DatabaseConnectionError`: Erros de conexão com o banco
- `SessionError`: Problemas com a sessão do banco

## Contribuindo

Contribuições são bem-vindas! Por favor, sinta-se à vontade para submeter pull requests.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.

## Autor

Miguel Tenorio
