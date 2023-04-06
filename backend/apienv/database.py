import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql://root:123456@127.0.0.1:3306/socialnetwork"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Créez un objet sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Instanciez une session à partir de l'objet sessionmaker
session = SessionLocal()

# Maintenant, vous pouvez appeler add() sur l'objet session
sys.setrecursionlimit(15000)
print(sys.getrecursionlimit())
