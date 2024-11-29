from peewee import MySQLDatabase, PostgresqlDatabase
from solargs.api.apps.db.request.request import DatabaseRequest

class DatabaseService:
    """DatabaseService
    """
    def __init__(self):
        pass

    def test_db_connect(self, request: DatabaseRequest):
        """test_db_connect
        Args:
           - request: DatabaseRequest
        """

        if request.db_type in ["mysql", "mariadb"]:
            db = MySQLDatabase(request.database, user=request.username, host=request.host, port=request.port,
                               password=request.password)
        elif request.db_type == 'postgresql':
            db = PostgresqlDatabase(request.database, user=request.username, host=request.host, port=request.port,
                               password=request.password)
        db.connect()
        db.close()