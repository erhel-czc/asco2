from fastapi import FastAPI
from sqlmodel import create_engine, SQLModel, Field, Relationship

app = FastAPI(title="AsCO2 API", version="26.7.25")

####################
## Database setup ##
####################

DATABASE_URL = "sqlite:///./asco2.db"
engine = create_engine(DATABASE_URL, echo=True)

############
## Tables ##
############

class User(SQLModel, table=True):
    """
    User table for storing user information.
    """

    id: int = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
    associations: list["Association"] = Relationship(back_populates="users")

class Association(SQLModel, table=True):
    """
    Association table for storing association information.
    """

    id: int = Field(default=None, primary_key=True)
    users: list[User] = Relationship(back_populates="associations")
    association_name: str
    association_description: str
    admin_id: int = Field(foreign_key="user.id")

class Report(SQLModel, table=True):
    """
    Report table for storing report information.
    """

    id: int = Field(default=None, primary_key=True)
    association_id: int = Field(foreign_key="association.id")
    report_title: str

    food_carbon_footprint: float
    transport_carbon_footprint: float
    stuff_carbon_footprint: float

class Food(SQLModel, table=True):
    """
    Food table for storing food-related carbon footprint information.
    """

    id: int = Field(default=None, primary_key=True)
    report_id: int = Field(foreign_key="report.id")
    food_type: str
    quantity: float
    emission_factor: float
    carbon_footprint: float

class Transport(SQLModel, table=True):
    """
    Transport table for storing transport-related carbon footprint information.
    """

    id: int = Field(default=None, primary_key=True)
    report_id: int = Field(foreign_key="report.id")
    transport_type: str
    distance: float
    emission_factor: float
    carbon_footprint: float

class Stuff(SQLModel, table=True):
    """
    Stuff table for storing stuff-related carbon footprint information.
    """

    id: int = Field(default=None, primary_key=True)
    report_id: int = Field(foreign_key="report.id")
    stuff_type: str
    quantity: float
    emission_factor: float
    carbon_footprint: float

################################
## Create the database tables ##
################################

SQLModel.metadata.create_all(engine)