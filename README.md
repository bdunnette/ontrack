# 🛼 OnTrack - Roller Derby Attendance Tracker

A modern web application for tracking roller derby skater attendance at practices. Built with NiceGUI and SQLModel.

## Features

- **Skater Management**: Add, edit, and manage skater profiles with derby names and contact information
- **Practice Scheduling**: Create and manage practice sessions with dates, times, and locations
- **Attendance Tracking**: Mark skaters as present, absent, or excused for each practice
- **Statistics Dashboard**: View attendance rates and team statistics at a glance
- **Modern UI**: Beautiful, responsive interface with smooth animations and premium design

## Setup

1. **Install dependencies** (using uv):
   ```bash
   uv sync
   ```

2. **Run the application**:
   ```bash
   uv run python main.py
   ```

3. **Access the app**: Open your browser to `http://localhost:8080`

## Development Setup

To set up the development environment with code quality tools:

1. **Install development dependencies**:
   ```bash
   uv sync --all-groups
   ```

2. **Install pre-commit hooks**:
   ```bash
   uv run pre-commit install
   ```

3. **Run pre-commit manually** (optional):
   ```bash
   uv run pre-commit run --all-files
   ```

The pre-commit hooks will automatically run on every commit to ensure code quality, formatting, and type checking.

## Usage

### Managing Skaters

1. Navigate to the **Skaters** page
2. Click **Add Skater** to create a new skater profile
3. Fill in their name, derby name (optional), email, and phone
4. Edit or deactivate skaters as needed

### Scheduling Practices

1. Go to the **Practices** page
2. Click **Add Practice** to create a new session
3. Enter the date, time, location, and any notes
4. Delete practices if needed (this will also remove attendance records)

### Tracking Attendance

1. Visit the **Attendance** page
2. Select a practice from the dropdown
3. Mark each skater as Present, Absent, or Excused
4. View the attendance summary at the bottom

### Dashboard

The dashboard shows:
- Total active skaters
- Total practices scheduled
- Average attendance rate
- Recent practice history

## Database

The app uses SQLite for data storage. The database file (`attendance.db`) is created automatically in the project directory on first run.

## Tech Stack

- **NiceGUI**: Modern Python web framework
- **SQLModel**: SQL database ORM with Pydantic models
- **SQLite**: Lightweight database engine
- **Python 3.13+**: Modern Python features
