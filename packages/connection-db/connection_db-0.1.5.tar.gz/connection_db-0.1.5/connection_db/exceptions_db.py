class DatabaseConnectionError(Exception):
    """Erro lançado quando há falha na conexão com o banco de dados."""
    pass

class DatabaseTypeError(ValueError):
    """Erro lançado quando o tipo de banco de dados não é suportado."""
    pass

class SessionError(Exception):
    """Erro lançado quando há problemas com a sessão do banco de dados."""
    pass

class QueryError(Exception):
    """Erro lançado quando há problemas na execução de queries."""
    pass
