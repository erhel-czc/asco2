from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from backend.db import get_db
from backend.models import Association, AssociationMembership, Report, User
from backend.routers.auth import get_current_user
from backend.schemas import (
    AssociationCreate,
    AssociationReportRead,
    AssociationMemberCreate,
    AssociationMemberRead,
    AssociationRead,
    UserAssociationRead,
)

router = APIRouter(prefix="/associations", tags=["associations"])


@router.get("", response_model=list[AssociationRead])
def read_associations(session: Session = Depends(get_db)):
    """Endpoint to retrieve all associations."""
    associations = session.exec(select(Association)).all()
    return associations


@router.post("", response_model=AssociationRead)
def create_association(
    association: AssociationCreate,
    session: Session = Depends(get_db),
):
    """Endpoint to create a new association."""
    if association.initial_admin_id is not None:
        db_user = session.get(User, association.initial_admin_id)

        if db_user is None:
            raise HTTPException(
                status_code=404, detail="Initial admin user not found")

    db_association = Association(
        association_name=association.association_name,
        association_description=association.association_description,
    )

    session.add(db_association)
    session.commit()
    session.refresh(db_association)

    if association.initial_admin_id is not None:
        membership = AssociationMembership(
            user_id=association.initial_admin_id,
            association_id=db_association.id,
            is_admin=True,
        )

        session.add(membership)
        session.commit()

    return db_association


@router.post("/{association_id}/members", response_model=AssociationMemberRead)
def add_association_member(
    association_id: int,
    payload: AssociationMemberCreate,
    session: Session = Depends(get_db),
):
    """Endpoint to add a user as association member (admin or non-admin)."""
    db_association = session.get(Association, association_id)

    if db_association is None:
        raise HTTPException(status_code=404, detail="Association not found")

    db_user = session.get(User, payload.user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    existing_membership = session.exec(
        select(AssociationMembership).where(
            AssociationMembership.association_id == association_id,
            AssociationMembership.user_id == payload.user_id,
        )
    ).first()

    if existing_membership is not None:
        raise HTTPException(
            status_code=409,
            detail="User is already a member of this association",
        )

    membership = AssociationMembership(
        association_id=association_id,
        user_id=payload.user_id,
        is_admin=payload.is_admin,
    )

    session.add(membership)
    session.commit()
    session.refresh(membership)
    return membership


@router.get("/mine", response_model=list[UserAssociationRead])
def read_my_associations(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    """Endpoint to retrieve associations for the authenticated user."""
    memberships = session.exec(
        select(Association, AssociationMembership.is_admin)
        .join(AssociationMembership)
        .where(AssociationMembership.user_id == current_user.id)
    ).all()

    return [
        UserAssociationRead(
            id=association.id,
            association_name=association.association_name,
            association_description=association.association_description,
            is_admin=is_admin,
        )
        for association, is_admin in memberships
    ]


@router.post("/{association_id}/reports", response_model=AssociationReportRead)
def create_association_report(
    association_id: int,
    report: AssociationReportRead,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    """Endpoint to create a new report for an association."""
    membership = session.exec(
        select(AssociationMembership).where(
            AssociationMembership.association_id == association_id,
            AssociationMembership.user_id == current_user.id,
        )
    ).first()

    if membership is None:
        raise HTTPException(status_code=403, detail="Forbidden")

    db_report = Report(
        association_id=association_id,
        report_title=report.report_title,
        food_carbon_footprint=report.food_carbon_footprint,
        transport_carbon_footprint=report.transport_carbon_footprint,
        stuff_carbon_footprint=report.stuff_carbon_footprint,
    )

    session.add(db_report)
    session.commit()
    session.refresh(db_report)

    return db_report


@router.get("/{association_id}/reports", response_model=list[AssociationReportRead])
def read_association_reports(
    association_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    """Endpoint to retrieve reports (bilans) for one association membership."""
    membership = session.exec(
        select(AssociationMembership).where(
            AssociationMembership.association_id == association_id,
            AssociationMembership.user_id == current_user.id,
        )
    ).first()

    if membership is None:
        raise HTTPException(status_code=403, detail="Forbidden")

    reports = session.exec(
        select(Report).where(Report.association_id == association_id)
    ).all()

    return [
        AssociationReportRead(
            id=report.id,
            report_title=report.report_title,
            food_carbon_footprint=report.food_carbon_footprint,
            transport_carbon_footprint=report.transport_carbon_footprint,
            stuff_carbon_footprint=report.stuff_carbon_footprint,
        )
        for report in reports
    ]
