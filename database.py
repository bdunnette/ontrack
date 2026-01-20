"""Database initialization and utilities."""

from sqlmodel import SQLModel, create_engine, Session, select
from models import Skater, Practice, Attendance

# Create SQLite database
DATABASE_URL = "sqlite:///./attendance.db"
engine = create_engine(DATABASE_URL, echo=False)


def init_db():
    """Initialize the database by creating all tables."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get a database session."""
    return Session(engine)


# Data access functions
def get_all_skaters(session: Session, active_only: bool = False):
    """Get all skaters, optionally filtering by active status."""
    query = select(Skater)
    if active_only:
        query = query.where(Skater.active)
    return session.exec(query.order_by(Skater.name)).all()


def get_skater(session: Session, skater_id: int):
    """Get a skater by ID."""
    return session.get(Skater, skater_id)


def create_skater(
    session: Session,
    name: str,
    derby_name: str = None,
    email: str = None,
    phone: str = None,
    guardian_name: str = None,
    guardian_email: str = None,
    guardian_phone: str = None,
    is_coach: bool = False,
):
    """Create a new skater."""
    skater = Skater(
        name=name,
        derby_name=derby_name,
        email=email,
        phone=phone,
        guardian_name=guardian_name,
        guardian_email=guardian_email,
        guardian_phone=guardian_phone,
        is_coach=is_coach,
    )
    session.add(skater)
    session.commit()
    session.refresh(skater)
    return skater


def update_skater(session: Session, skater_id: int, **kwargs):
    """Update a skater's information."""
    skater = session.get(Skater, skater_id)
    if skater:
        for key, value in kwargs.items():
            if hasattr(skater, key):
                setattr(skater, key, value)
        session.add(skater)
        session.commit()
        session.refresh(skater)
    return skater


def delete_skater(session: Session, skater_id: int):
    """Delete a skater (soft delete by setting active=False)."""
    skater = session.get(Skater, skater_id)
    if skater:
        skater.active = False
        session.add(skater)
        session.commit()


def get_all_practices(session: Session, limit: int = None):
    """Get all practices, ordered by date descending."""
    query = select(Practice).order_by(Practice.date.desc())
    if limit:
        query = query.limit(limit)
    return session.exec(query).all()


def get_practice(session: Session, practice_id: int):
    """Get a practice by ID."""
    return session.get(Practice, practice_id)


def create_practice(
    session: Session,
    date: str,
    start_time: str = None,
    end_time: str = None,
    location: str = None,
    notes: str = None,
):
    """Create a new practice session."""
    practice = Practice(
        date=date,
        start_time=start_time,
        end_time=end_time,
        location=location,
        notes=notes,
    )
    session.add(practice)
    session.commit()
    session.refresh(practice)
    return practice


def delete_practice(session: Session, practice_id: int):
    """Delete a practice and all associated attendance records."""
    practice = session.get(Practice, practice_id)
    if practice:
        session.delete(practice)
        session.commit()


def get_attendance(session: Session, practice_id: int, skater_id: int = None):
    """Get attendance records for a practice, optionally for a specific skater."""
    query = select(Attendance).where(Attendance.practice_id == practice_id)
    if skater_id:
        query = query.where(Attendance.skater_id == skater_id)
    return session.exec(query).all()


def set_attendance(
    session: Session, practice_id: int, skater_id: int, status: str, notes: str = None
):
    """Set or update attendance for a skater at a practice."""
    # Check if attendance record exists
    query = select(Attendance).where(
        Attendance.practice_id == practice_id, Attendance.skater_id == skater_id
    )
    attendance = session.exec(query).first()

    if attendance:
        # Update existing record
        attendance.status = status
        if notes is not None:
            attendance.notes = notes
    else:
        # Create new record
        attendance = Attendance(
            practice_id=practice_id, skater_id=skater_id, status=status, notes=notes
        )

    session.add(attendance)
    session.commit()
    session.refresh(attendance)
    return attendance


def get_skater_attendance_stats(session: Session, skater_id: int):
    """Get attendance statistics for a skater."""
    query = select(Attendance).where(Attendance.skater_id == skater_id)
    records = session.exec(query).all()

    total = len(records)
    present = sum(1 for r in records if r.status == "present")
    absent = sum(1 for r in records if r.status == "absent")
    excused = sum(1 for r in records if r.status == "excused")

    return {
        "total": total,
        "present": present,
        "absent": absent,
        "excused": excused,
        "attendance_rate": (present / total * 100) if total > 0 else 0,
    }
