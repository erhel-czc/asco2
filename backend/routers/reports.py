from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from backend.db import get_db
from backend.models import Report
from backend.schemas import ReportCreate

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("")
def read_reports(session: Session = Depends(get_db)):
    """Endpoint to retrieve all reports."""
    reports = session.exec(select(Report)).all()
    return reports


@router.post("")
def create_report(report: ReportCreate, session: Session = Depends(get_db)):
    """Endpoint to create a new report."""
    db_report = Report(
        association_id=report.association_id,
        report_title=report.report_title,
        food_carbon_footprint=report.food_carbon_footprint,
        transport_carbon_footprint=report.transport_carbon_footprint,
        stuff_carbon_footprint=report.stuff_carbon_footprint,
    )

    session.add(db_report)
    session.commit()
    session.refresh(db_report)
    return db_report
