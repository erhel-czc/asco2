from sqlmodel import Session, select

from backend.models import Association, AssociationMembership, Report, User


def test_root_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_api_root_endpoint(client):
    response = client.get("/api")

    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the AsCO2 API!"}


def test_template_routes(client):
    for path in ("/", "/login", "/signup", "/methodologie"):
        response = client.get(path)
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


def test_users_endpoints(client, engine):
    create_response = client.post(
        "/users",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "hashed_password": "hashed-secret",
        },
    )

    assert create_response.status_code == 200
    assert create_response.json()["username"] == "alice"
    assert create_response.json()["email"] == "alice@example.com"
    assert "id" in create_response.json()

    list_response = client.get("/users")

    assert list_response.status_code == 200
    assert list_response.json() == [create_response.json()]

    with Session(engine) as session:
        user = session.exec(select(User)).first()
        assert user is not None
        assert user.hashed_password == "hashed-secret"


def test_association_creation_and_initial_admin(client, engine):
    user_response = client.post(
        "/users",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "hashed_password": "hashed-password",
        },
    )

    association_response = client.post(
        "/associations",
        json={
            "association_name": "Green Club",
            "association_description": "Local climate action group",
            "initial_admin_id": user_response.json()["id"],
        },
    )

    assert association_response.status_code == 200
    assert association_response.json()["association_name"] == "Green Club"
    assert association_response.json()["association_description"] == "Local climate action group"
    assert association_response.json()["id"] is not None

    with Session(engine) as session:
        association = session.exec(select(Association)).first()
        membership = session.exec(select(AssociationMembership)).first()

    assert association is not None
    assert membership is not None
    assert membership.user_id == user_response.json()["id"]
    assert membership.association_id == association.id
    assert membership.is_admin is True


def test_add_association_member(client):
    user_response = client.post(
        "/users",
        json={
            "username": "charlie",
            "email": "charlie@example.com",
            "hashed_password": "hashed-password",
        },
    )
    association_response = client.post(
        "/associations",
        json={
            "association_name": "Bike Coop",
            "association_description": "Community cycling association",
        },
    )

    member_response = client.post(
        f"/associations/{association_response.json()['id']}/members",
        json={
            "user_id": user_response.json()["id"],
            "is_admin": True,
        },
    )

    assert member_response.status_code == 200
    assert member_response.json() == {
        "user_id": user_response.json()["id"],
        "association_id": association_response.json()["id"],
        "is_admin": True,
    }


def test_add_association_member_errors(client):
    missing_association = client.post(
        "/associations/999/members",
        json={"user_id": 1, "is_admin": False},
    )
    assert missing_association.status_code == 404
    assert missing_association.json()["detail"] == "Association not found"

    association_response = client.post(
        "/associations",
        json={
            "association_name": "Garden Group",
            "association_description": "Neighborhood gardening",
        },
    )

    missing_user = client.post(
        f"/associations/{association_response.json()['id']}/members",
        json={"user_id": 999, "is_admin": False},
    )
    assert missing_user.status_code == 404
    assert missing_user.json()["detail"] == "User not found"

    user_response = client.post(
        "/users",
        json={
            "username": "dana",
            "email": "dana@example.com",
            "hashed_password": "hashed-password",
        },
    )

    first_add = client.post(
        f"/associations/{association_response.json()['id']}/members",
        json={"user_id": user_response.json()["id"], "is_admin": False},
    )
    assert first_add.status_code == 200

    duplicate_add = client.post(
        f"/associations/{association_response.json()['id']}/members",
        json={"user_id": user_response.json()["id"], "is_admin": False},
    )
    assert duplicate_add.status_code == 409
    assert duplicate_add.json()["detail"] == (
        "User is already a member of this association"
    )


def test_reports_and_public_routes(client):
    assert client.get("/food").json() == []
    assert client.get("/transport").json() == []
    assert client.get("/stuff").json() == []

    association_response = client.post(
        "/associations",
        json={
            "association_name": "Reports Club",
            "association_description": "Tracks carbon reports",
        },
    )

    report_response = client.post(
        "/reports",
        json={
            "association_id": association_response.json()["id"],
            "report_title": "Annual report",
            "food_carbon_footprint": 12.5,
            "transport_carbon_footprint": 34.0,
            "stuff_carbon_footprint": 7.25,
        },
    )

    assert report_response.status_code == 200
    assert report_response.json()["report_title"] == "Annual report"

    reports_response = client.get("/reports")
    assert reports_response.status_code == 200
    assert reports_response.json() == [report_response.json()]
