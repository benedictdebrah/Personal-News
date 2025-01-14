from sqlmodel import create_engine, SQLModel

DATABASE_URL = "sqlite:///info_data.db"
engine = create_engine(DATABASE_URL)

SQLModel.metadata.create_all(engine)
