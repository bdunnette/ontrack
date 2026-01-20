"""Database models for the roller derby attendance tracker."""

from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class Skater(SQLModel, table=True):
    """Represents a roller derby skater."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    derby_name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)

    # Guardian information (for junior derby)
    guardian_name: Optional[str] = Field(default=None)
    guardian_email: Optional[str] = Field(default=None)
    guardian_phone: Optional[str] = Field(default=None)

    # Coach flag
    is_coach: bool = Field(default=False)

    active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    attendances: list["Attendance"] = Relationship(back_populates="skater")


class Practice(SQLModel, table=True):
    """Represents a practice session."""

    id: Optional[int] = Field(default=None, primary_key=True)
    date: str = Field(index=True)  # Store as ISO format string (YYYY-MM-DD)
    start_time: Optional[str] = Field(default=None)  # HH:MM format
    end_time: Optional[str] = Field(default=None)  # HH:MM format
    location: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    attendances: list["Attendance"] = Relationship(back_populates="practice")


class Attendance(SQLModel, table=True):
    """Represents attendance record for a skater at a practice."""

    id: Optional[int] = Field(default=None, primary_key=True)
    skater_id: int = Field(foreign_key="skater.id", index=True)
    practice_id: int = Field(foreign_key="practice.id", index=True)
    status: str = Field(default="absent")  # present, absent, excused
    notes: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    skater: Optional[Skater] = Relationship(back_populates="attendances")
    practice: Optional[Practice] = Relationship(back_populates="attendances")
