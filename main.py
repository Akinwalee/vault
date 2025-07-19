import atexit
from cli.cli import cli
from storage.database import Database


@atexit.register
def shutdown_db():
    db = Database()
    db.close_connections()
    print("Database connections closed successfully")


if __name__ == "__main__":
    cli()