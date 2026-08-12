from backend.database.connection import get_engine
from backend.database.models import Base


def create_tables() -> None:
    """Create all database tables."""
    engine = get_engine()
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_tables()
