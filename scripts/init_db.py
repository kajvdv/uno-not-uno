
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(".env")

from app.database import Base, engine, get_db
from app.auth import register_user
import app.main # Make sure all the orm models are imported

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

for db in get_db():
    register_user('admin', 'admin', db)
