"""Database connection for Azure SQL Database (or MySQL as implied by errors)."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import bingefriend.shows.application.config as config

# 1. Get the connection string
SQLALCHEMY_DATABASE_URL = config.SQLALCHEMY_CONNECTION_STRING
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("SQLALCHEMY_CONNECTION_STRING is not set in the configuration.")

# 2. Create the SQLAlchemy engine with explicit pooling options
#    Adjust these values based on your expected load and database capacity.
#    The values here are examples.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=5,          # Number of connections to keep open in the pool
    max_overflow=10,      # Number of connections that can be opened beyond pool_size
    pool_recycle=1800,    # Recycle connections after 30 minutes (important for MySQL)
    pool_timeout=30,      # How long to wait for a connection from the pool
    pool_pre_ping=True    # Enable "pre-ping" to test connections before checkout
)

# 3. Create a SessionLocal class (session factory)
#    This remains the same. Each call to SessionLocal() will create a new Session
#    that uses a connection from the engine's pool.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create a Base class (even if models are elsewhere, it's standard)
#    This remains the same.
Base = declarative_base()

# Optional: Add a function to help with database initialization if needed,
# e.g., for creating tables (though typically run separately, not per function).
# def init_db():
#     Base.metadata.create_all(bind=engine)
