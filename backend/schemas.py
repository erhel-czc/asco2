from sqlmodel import SQLModel


class UserCreate(SQLModel):
    """Schema for creating a new user. Accepts the raw plaintext password;
    hashing is performed server-side before persistence."""

    username: str
    email: str
    password: str


class UserLogin(SQLModel):
    """Schema for logging in with an email and password."""

    email: str
    password: str


class UserRead(SQLModel):
    """Public schema for user responses."""

    id: int
    username: str
    email: str


class SessionRead(SQLModel):
    """Public schema for a session response."""

    token: str
    user_id: int


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


class UserAssociationRead(SQLModel):
    """Association item displayed in a user's dashboard."""

    id: int
    association_name: str
    association_description: str
    is_admin: bool


class AssociationReportRead(SQLModel):
    """Report item displayed in an association reports page."""

    id: int
    report_title: str
    food_carbon_footprint: float = 0.0
    transport_carbon_footprint: float = 0.0
    stuff_carbon_footprint: float = 0.0
