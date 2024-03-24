# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from arrow import now
from sqlalchemy.orm import declarative_base
from main import session
from sqlalchemy import column,DateTime
from datetime import datetime
from sqlalchemy.sql import func


Model = declarative_base()
@pytest.fixture(scope='module')
def session():
    engine = create_engine('sqlite:///db')  # Use your actual database file
    Model.metadata.create_all(engine)  # Create the schema in the database
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session  # This is where the testing happens.
    session.close()
    Model.metadata.drop_all(engine)  # Clean up the database after the tests