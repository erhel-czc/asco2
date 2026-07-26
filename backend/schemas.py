from sqlmodel import SQLModel


class UserCreate(SQLModel):
    """Schema for creating a new user."""

    username: str
    email: str
    hashed_password: str


class UserRead(SQLModel):
    """Public schema for user responses."""

    id: int
    username: str
    email: str


class AssociationCreate(SQLModel):
    """Schema for creating a new association."""

    association_name: str
    association_description: str
    initial_admin_id: int | None = None


class AssociationMemberCreate(SQLModel):
    """Schema for adding a member to an association."""

    user_id: int
    is_admin: bool = False


class AssociationMemberRead(SQLModel):
    """Public schema for association membership."""

    user_id: int
    association_id: int
    is_admin: bool


class AssociationRead(SQLModel):
    """Public schema for association responses."""

    id: int
    association_name: str
    association_description: str


class ReportCreate(SQLModel):
    """Schema for creating a new report."""

    association_id: int
    report_title: str
    food_carbon_footprint: float
    transport_carbon_footprint: float
    stuff_carbon_footprint: float
