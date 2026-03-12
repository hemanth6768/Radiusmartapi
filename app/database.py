from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = ( 
#     "mssql+pyodbc://ghr:8888@localhost/Radiusmart"
#     "?driver=ODBC+Driver+17+for+SQL+Server"
# )

DATABASE_URL = (
    "mssql+pyodbc://hemanth:Br3Zf6kcf1!P@radiusmart.database.windows.net:1433/Radiusmart"
     "?driver=ODBC+Driver+18+for+SQL+Server"
    "&Encrypt=yes"
    "&TrustServerCertificate=no"
)

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()
