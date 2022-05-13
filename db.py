from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
Base = declarative_base()

DB_TYPE = "mysql+mysqlconnector"
DB_USER = "root"
DB_USER_PASS = "password"
DB_HOST = "localhost"
DB_PORT = 3306
DB_INSTANCE = "generated_db"

connection_string = f"{DB_TYPE}://{DB_USER}:{DB_USER_PASS}@{DB_HOST}:{DB_PORT}/{DB_INSTANCE}"

engine = create_engine(connection_string, echo=True, isolation_level="READ UNCOMMITTED")
Session = sessionmaker()