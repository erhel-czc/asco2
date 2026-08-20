from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel


class AssociationMembership(SQLModel, table=True):
    """Link table between users and associations with role information."""

    user_id: int = Field(foreign_key="user.id", primary_key=True)
    association_id: int = Field(foreign_key="association.id", primary_key=True)
    is_admin: bool = Field(default=False)


class User(SQLModel, table=True):
    """User table for storing user information."""

    id: int = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
    associations: list["Association"] = Relationship(
        back_populates="users",
        link_model=AssociationMembership,
    )


class UserSession(SQLModel, table=True):
    """Server-side login session stored in the database."""

    token: str = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    expires_at: datetime


class Association(SQLModel, table=True):
    """Association table for storing association information."""

    id: int = Field(default=None, primary_key=True)
    users: list[User] = Relationship(
        back_populates="associations",
        link_model=AssociationMembership,
    )
    association_name: str
    association_description: str


class Report(SQLModel, table=True):
    """Report table for storing report information."""

    id: int = Field(default=None, primary_key=True)
    association_id: int = Field(foreign_key="association.id")
    report_title: str
    report_description: str
    food_carbon_footprint: float
    transport_carbon_footprint: float
    stuff_carbon_footprint: float


class Food(SQLModel, table=True):
    """Food table for storing food-related carbon footprint information."""

    id: int = Field(default=None, primary_key=True)
    report_id: int = Field(foreign_key="report.id")
    food_type: str
    quantity: float
    emission_factor: float
    carbon_footprint: float


class Transport(SQLModel, table=True):
    """Transport table for storing transport-related carbon footprint information."""

    id: int = Field(default=None, primary_key=True)
    report_id: int = Field(foreign_key="report.id")
    transport_type: str
    distance: float
    emission_factor: float
    carbon_footprint: float


class Stuff(SQLModel, table=True):
    """Stuff table for storing stuff-related carbon footprint information."""

    id: int = Field(default=None, primary_key=True)
    report_id: int = Field(foreign_key="report.id")
    stuff_type: str
    quantity: float
    emission_factor: float
    carbon_footprint: float


class Digital(SQLModel, table=True):
    """Digital table for storing digital-related carbon footprint information."""

    id: int = Field(default=None, primary_key=True)
    report_id: int = Field(foreign_key="report.id")
    digital_type: str
    amount: float
    emission_factor: float
    carbon_footprint: float