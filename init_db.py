from app.core.database import engine
from app.models.database_models import Base

Base.metadata.create_all(bind=engine)

print("Database initialized successfully.")
