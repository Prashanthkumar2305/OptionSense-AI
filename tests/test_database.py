import os
import pytest 
from sqlalchemy import text 
from backend.database.connection import get_engine

@pytest.mark.skipif(
    not os.getenv("mysql_password"),
    reason= "mysql credentials are not configured",
    )

def test_database_connection() ->None:
    engine = get_engine()

    with engine.connect() as connection:
        result = connection.execute(text("select 1"))
        assert result.scalar() ==1 
        
