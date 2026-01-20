"""Tests for database models."""

from datetime import datetime

from models import Attendance, Practice, Skater


class TestSkaterModel:
    """Tests for the Skater model."""

    def test_create_basic_skater(self, session):
        """Test creating a basic skater with minimal fields."""
        skater = Skater(name="Test Skater")
        session.add(skater)
        session.commit()
        session.refresh(skater)

        assert skater.id is not None
        assert skater.name == "Test Skater"
        assert skater.active is True
        assert skater.is_coach is False
        assert isinstance(skater.created_at, datetime)

    def test_create_skater_with_derby_name(self, session):
        """Test creating a skater with a derby name."""
        skater = Skater(name="Jane Doe", derby_name="Thunder Thighs")
        session.add(skater)
        session.commit()

        assert skater.derby_name == "Thunder Thighs"

    def test_create_skater_with_guardian_info(self, session):
        """Test creating a skater with guardian information."""
        skater = Skater(
            name="Emma Junior",
            guardian_name="Mary Smith",
            guardian_email="mary@example.com",
            guardian_phone="555-1234",
        )
        session.add(skater)
        session.commit()

        assert skater.guardian_name == "Mary Smith"
        assert skater.guardian_email == "mary@example.com"
        assert skater.guardian_phone == "555-1234"

    def test_create_coach(self, session):
        """Test creating a skater marked as a coach."""
        coach = Skater(name="Coach Sarah", is_coach=True)
        session.add(coach)
        session.commit()

        assert coach.is_coach is True

    def test_skater_defaults(self, session):
        """Test that skater fields have correct defaults."""
        skater = Skater(name="Test")
        session.add(skater)
        session.commit()

        assert skater.derby_name is None
        assert skater.email is None
        assert skater.phone is None
        assert skater.guardian_name is None
        assert skater.guardian_email is None
        assert skater.guardian_phone is None
        assert skater.is_coach is False
        assert skater.active is True


class TestPracticeModel:
    """Tests for the Practice model."""

    def test_create_basic_practice(self, session):
        """Test creating a basic practice session."""
        practice = Practice(date="2026-01-25")
        session.add(practice)
        session.commit()
        session.refresh(practice)

        assert practice.id is not None
        assert practice.date == "2026-01-25"
        assert isinstance(practice.created_at, datetime)

    def test_create_practice_with_details(self, session):
        """Test creating a practice with full details."""
        practice = Practice(
            date="2026-01-25",
            start_time="19:00",
            end_time="21:00",
            location="Main Rink",
            notes="Regular practice",
        )
        session.add(practice)
        session.commit()

        assert practice.start_time == "19:00"
        assert practice.end_time == "21:00"
        assert practice.location == "Main Rink"
        assert practice.notes == "Regular practice"

    def test_practice_defaults(self, session):
        """Test that practice fields have correct defaults."""
        practice = Practice(date="2026-01-25")
        session.add(practice)
        session.commit()

        assert practice.start_time is None
        assert practice.end_time is None
        assert practice.location is None
        assert practice.notes is None


class TestAttendanceModel:
    """Tests for the Attendance model."""

    def test_create_attendance_record(self, session):
        """Test creating an attendance record."""
        skater = Skater(name="Test Skater")
        practice = Practice(date="2026-01-25")
        session.add(skater)
        session.add(practice)
        session.commit()

        attendance = Attendance(
            skater_id=skater.id, practice_id=practice.id, status="present"
        )
        session.add(attendance)
        session.commit()
        session.refresh(attendance)

        assert attendance.id is not None
        assert attendance.skater_id == skater.id
        assert attendance.practice_id == practice.id
        assert attendance.status == "present"
        assert isinstance(attendance.created_at, datetime)

    def test_attendance_default_status(self, session):
        """Test that attendance defaults to absent."""
        skater = Skater(name="Test Skater")
        practice = Practice(date="2026-01-25")
        session.add(skater)
        session.add(practice)
        session.commit()

        attendance = Attendance(skater_id=skater.id, practice_id=practice.id)
        session.add(attendance)
        session.commit()

        assert attendance.status == "absent"

    def test_attendance_with_notes(self, session):
        """Test creating attendance with notes."""
        skater = Skater(name="Test Skater")
        practice = Practice(date="2026-01-25")
        session.add(skater)
        session.add(practice)
        session.commit()

        attendance = Attendance(
            skater_id=skater.id,
            practice_id=practice.id,
            status="excused",
            notes="Doctor appointment",
        )
        session.add(attendance)
        session.commit()

        assert attendance.status == "excused"
        assert attendance.notes == "Doctor appointment"

    def test_attendance_relationships(self, session):
        """Test that attendance relationships work correctly."""
        skater = Skater(name="Test Skater")
        practice = Practice(date="2026-01-25")
        session.add(skater)
        session.add(practice)
        session.commit()

        attendance = Attendance(
            skater_id=skater.id, practice_id=practice.id, status="present"
        )
        session.add(attendance)
        session.commit()
        session.refresh(attendance)

        # Test relationships
        assert attendance.skater.name == "Test Skater"
        assert attendance.practice.date == "2026-01-25"
