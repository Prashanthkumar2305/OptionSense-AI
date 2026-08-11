import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.engine import Engine

project_root = Path(__file__).resolve().parents[2]

load_dotenv(project_root / ".env")


def get_database_url() -> URL:
    """Build the MYSQL database URL from environment variables."""
    host = os.getenv("mysql_host", "localhost")
    port = int(os.getenv("mysql_port", "3306"))
    database = os.getenv("mysql_database", "optionsense")
    user = os.getenv("mysql_user", "root")
    password = os.getenv("mysql_password", "")

    return URL.create(
        drivername="mysql+pymysql",
        username=user,
        password=password,
        host=host,
        port=port,
        database=database,
    )


def get_engine() -> Engine:
    """Create the SQLAlchemy database engine."""
    return create_engine(
        get_database_url(),
        pool_pre_ping=True,
    )
