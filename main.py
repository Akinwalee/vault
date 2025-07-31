import atexit
from cli.cli import cli
from storage.database import Database


@atexit.register
def shutdown_db():
    db = Database()
    db.close_connections()
    print("Database connections closed successfully")


if __name__ == "__main__":
    db = Database()
    mongo = db.get_mongo_db("vault")
    fd = db.fs
    redis = db.get_redis_db()
    cli()