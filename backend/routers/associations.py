from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from backend.db import get_db
from backend.models import Association, AssociationMembership, User
from backend.schemas import (
    AssociationCreate,
    AssociationMemberCreate,
    AssociationMemberRead,
    AssociationRead,
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
