"""Roller Derby Attendance Tracker - Main Application"""

from nicegui import ui
from datetime import date
from database import (
    init_db,
    get_session,
    get_all_skaters,
    create_skater,
    update_skater,
    delete_skater,
    get_all_practices,
    create_practice,
    delete_practice,
    get_attendance,
    set_attendance,
    get_skater_attendance_stats,
)

# Initialize database on startup
init_db()

# Global state for UI refresh
refresh_callbacks = {}


def register_refresh(page_name, callback):
    """Register a callback to refresh a page."""
    refresh_callbacks[page_name] = callback


def trigger_refresh(page_name):
    """Trigger a refresh for a specific page."""
    if page_name in refresh_callbacks:
        refresh_callbacks[page_name]()


# ==================== STYLING ====================
def apply_custom_styles():
    """Apply custom CSS for premium look and feel."""
    ui.add_head_html("""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            * {
                font-family: 'Inter', sans-serif;
            }

            body {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                background-attachment: fixed;
            }

            .main-container {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                padding: 2rem;
                margin: 2rem auto;
                max-width: 1400px;
            }

            .stat-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 15px;
                padding: 1.5rem;
                color: white;
                box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }

            .stat-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 30px rgba(102, 126, 234, 0.4);
            }

            .stat-number {
                font-size: 2.5rem;
                font-weight: 700;
                margin: 0.5rem 0;
            }

            .stat-label {
                font-size: 0.9rem;
                opacity: 0.9;
                text-transform: uppercase;
                letter-spacing: 1px;
            }

            .page-title {
                font-size: 2.5rem;
                font-weight: 700;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 1.5rem;
            }

            .section-title {
                font-size: 1.5rem;
                font-weight: 600;
                color: #333;
                margin: 1.5rem 0 1rem 0;
            }

            .coach-badge {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                padding: 0.25rem 0.75rem;
                border-radius: 12px;
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }

            .attendance-grid {
                display: grid;
                gap: 0.5rem;
            }

            .attendance-row {
                display: grid;
                grid-template-columns: 200px 1fr;
                gap: 1rem;
                align-items: center;
                padding: 0.75rem;
                background: white;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
                transition: all 0.2s ease;
            }

            .attendance-row:hover {
                border-color: #667eea;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
            }

            .skater-name {
                font-weight: 600;
                color: #333;
            }

            .derby-name {
                font-size: 0.85rem;
                color: #666;
                font-style: italic;
            }

            .q-btn {
                text-transform: none !important;
                font-weight: 500 !important;
                border-radius: 8px !important;
                transition: all 0.2s ease !important;
            }

            .q-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
            }

            .q-table {
                border-radius: 12px !important;
                overflow: hidden;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
            }

            .q-table thead tr {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            }

            .q-table thead th {
                color: white !important;
                font-weight: 600 !important;
            }

            .q-table tbody tr:hover {
                background-color: rgba(102, 126, 234, 0.05) !important;
            }

            .nav-button {
                margin: 0 0.25rem;
            }
        </style>
    """)


# ==================== NAVIGATION ====================
def create_navigation():
    """Create the navigation bar."""
    with ui.row().classes("w-full justify-center gap-2 mb-6"):
        ui.button("🏠 Dashboard", on_click=lambda: ui.navigate.to("/")).classes(
            "nav-button"
        ).props("flat color=primary")
        ui.button("👥 Skaters", on_click=lambda: ui.navigate.to("/skaters")).classes(
            "nav-button"
        ).props("flat color=primary")
        ui.button(
            "📅 Practices", on_click=lambda: ui.navigate.to("/practices")
        ).classes("nav-button").props("flat color=primary")
        ui.button(
            "✓ Attendance", on_click=lambda: ui.navigate.to("/attendance")
        ).classes("nav-button").props("flat color=primary")


# ==================== DASHBOARD PAGE ====================
@ui.page("/")
def dashboard_page():
    apply_custom_styles()

    with ui.column().classes("main-container"):
        ui.label("🛼 Junior Roller Derby Attendance Tracker").classes("page-title")
        create_navigation()

        session = get_session()

        # Statistics
        skaters = get_all_skaters(session, active_only=True)
        coaches = [s for s in skaters if s.is_coach]
        players = [s for s in skaters if not s.is_coach]
        practices = get_all_practices(session, limit=10)

        total_skaters = len(players)
        total_coaches = len(coaches)
        total_practices = len(practices)

        # Calculate overall attendance rate
        total_present = 0
        total_records = 0
        for skater in skaters:
            stats = get_skater_attendance_stats(session, skater.id)
            total_present += stats["present"]
            total_records += stats["total"]

        avg_attendance = (
            (total_present / total_records * 100) if total_records > 0 else 0
        )

        ui.label("Overview").classes("section-title")
        with ui.row().classes("w-full gap-4"):
            with ui.card().classes("stat-card flex-1"):
                ui.label("Active Skaters").classes("stat-label")
                ui.label(str(total_skaters)).classes("stat-number")

            with ui.card().classes("stat-card flex-1"):
                ui.label("Coaches").classes("stat-label")
                ui.label(str(total_coaches)).classes("stat-number")

            with ui.card().classes("stat-card flex-1"):
                ui.label("Total Practices").classes("stat-label")
                ui.label(str(total_practices)).classes("stat-number")

            with ui.card().classes("stat-card flex-1"):
                ui.label("Avg Attendance").classes("stat-label")
                ui.label(f"{avg_attendance:.1f}%").classes("stat-number")

        # Coaches section
        if coaches:
            ui.label("Coaches").classes("section-title")
            coach_rows = []
            for coach in coaches:
                stats = get_skater_attendance_stats(session, coach.id)
                coach_rows.append(
                    {
                        "name": coach.name,
                        "derby_name": coach.derby_name or "-",
                        "email": coach.email or "-",
                        "phone": coach.phone or "-",
                        "attendance_rate": f"{stats['attendance_rate']:.1f}%",
                    }
                )

            ui.table(
                columns=[
                    {"name": "name", "label": "Name", "field": "name", "align": "left"},
                    {
                        "name": "derby_name",
                        "label": "Derby Name",
                        "field": "derby_name",
                        "align": "left",
                    },
                    {
                        "name": "email",
                        "label": "Email",
                        "field": "email",
                        "align": "left",
                    },
                    {
                        "name": "phone",
                        "label": "Phone",
                        "field": "phone",
                        "align": "left",
                    },
                    {
                        "name": "attendance_rate",
                        "label": "Attendance",
                        "field": "attendance_rate",
                        "align": "center",
                    },
                ],
                rows=coach_rows,
            ).classes("w-full")

        # Recent practices
        ui.label("Recent Practices").classes("section-title")
        if practices:
            practice_rows = []
            for p in practices[:5]:
                attendance_records = get_attendance(session, p.id)
                present_count = sum(
                    1 for a in attendance_records if a.status == "present"
                )
                practice_rows.append(
                    {
                        "date": p.date,
                        "time": f"{p.start_time or 'N/A'} - {p.end_time or 'N/A'}",
                        "location": p.location or "N/A",
                        "attendance": f"{present_count}/{len(skaters)}",
                    }
                )

            ui.table(
                columns=[
                    {"name": "date", "label": "Date", "field": "date", "align": "left"},
                    {"name": "time", "label": "Time", "field": "time", "align": "left"},
                    {
                        "name": "location",
                        "label": "Location",
                        "field": "location",
                        "align": "left",
                    },
                    {
                        "name": "attendance",
                        "label": "Attendance",
                        "field": "attendance",
                        "align": "center",
                    },
                ],
                rows=practice_rows,
            ).classes("w-full")
        else:
            ui.label("No practices scheduled yet.").classes("text-gray-500")

        session.close()


# ==================== SKATERS PAGE ====================
@ui.page("/skaters")
def skaters_page():
    apply_custom_styles()

    with ui.column().classes("main-container"):
        ui.label("👥 Skater Management").classes("page-title")
        create_navigation()

        # Container for the table (will be refreshed)
        table_container = ui.column().classes("w-full")

        def refresh_table():
            table_container.clear()
            with table_container:
                session = get_session()
                skaters = get_all_skaters(session)

                if skaters:
                    rows = []
                    for s in skaters:
                        stats = get_skater_attendance_stats(session, s.id)
                        rows.append(
                            {
                                "id": s.id,
                                "name": s.name,
                                "derby_name": s.derby_name or "-",
                                "guardian": s.guardian_name or "-",
                                "guardian_phone": s.guardian_phone or "-",
                                "is_coach": "⭐ Coach" if s.is_coach else "",
                                "attendance_rate": f"{stats['attendance_rate']:.1f}%",
                                "active": "✓" if s.active else "✗",
                            }
                        )

                    table = ui.table(
                        columns=[
                            {
                                "name": "name",
                                "label": "Name",
                                "field": "name",
                                "align": "left",
                            },
                            {
                                "name": "derby_name",
                                "label": "Derby Name",
                                "field": "derby_name",
                                "align": "left",
                            },
                            {
                                "name": "guardian",
                                "label": "Guardian",
                                "field": "guardian",
                                "align": "left",
                            },
                            {
                                "name": "guardian_phone",
                                "label": "Guardian Phone",
                                "field": "guardian_phone",
                                "align": "left",
                            },
                            {
                                "name": "is_coach",
                                "label": "Role",
                                "field": "is_coach",
                                "align": "center",
                            },
                            {
                                "name": "attendance_rate",
                                "label": "Attendance",
                                "field": "attendance_rate",
                                "align": "center",
                            },
                            {
                                "name": "active",
                                "label": "Active",
                                "field": "active",
                                "align": "center",
                            },
                            {
                                "name": "actions",
                                "label": "Actions",
                                "field": "actions",
                                "align": "center",
                            },
                        ],
                        rows=rows,
                    ).classes("w-full")

                    # Add action buttons
                    table.add_slot(
                        "body-cell-actions",
                        """
                        <q-td :props="props">
                            <q-btn size="sm" flat dense icon="edit" color="primary" @click="$parent.$emit('edit', props.row)" />
                            <q-btn size="sm" flat dense icon="delete" color="negative" @click="$parent.$emit('delete', props.row)" />
                        </q-td>
                    """,
                    )

                    table.on("edit", lambda e: edit_skater_dialog(e.args["id"]))
                    table.on("delete", lambda e: delete_skater_confirm(e.args["id"]))
                else:
                    ui.label("No skaters found. Add your first skater!").classes(
                        "text-gray-500"
                    )

                session.close()

        def add_skater_dialog():
            with ui.dialog() as dialog, ui.card().classes("p-6 w-96"):
                ui.label("Add New Skater").classes("text-xl font-bold mb-4")

                name_input = ui.input("Name *").classes("w-full").props("outlined")
                derby_input = ui.input("Derby Name").classes("w-full").props("outlined")
                email_input = (
                    ui.input("Skater Email").classes("w-full").props("outlined")
                )
                phone_input = (
                    ui.input("Skater Phone").classes("w-full").props("outlined")
                )

                ui.label("Guardian Information").classes(
                    "text-lg font-semibold mt-4 mb-2"
                )
                guardian_name_input = (
                    ui.input("Guardian Name").classes("w-full").props("outlined")
                )
                guardian_email_input = (
                    ui.input("Guardian Email").classes("w-full").props("outlined")
                )
                guardian_phone_input = (
                    ui.input("Guardian Phone").classes("w-full").props("outlined")
                )

                is_coach_checkbox = ui.checkbox("This person is a coach", value=False)

                with ui.row().classes("w-full justify-end gap-2 mt-4"):
                    ui.button("Cancel", on_click=dialog.close).props("flat")

                    def save_skater():
                        if not name_input.value:
                            ui.notify("Name is required", type="negative")
                            return

                        session = get_session()
                        create_skater(
                            session,
                            name=name_input.value,
                            derby_name=derby_input.value or None,
                            email=email_input.value or None,
                            phone=phone_input.value or None,
                            guardian_name=guardian_name_input.value or None,
                            guardian_email=guardian_email_input.value or None,
                            guardian_phone=guardian_phone_input.value or None,
                            is_coach=is_coach_checkbox.value,
                        )
                        session.close()

                        ui.notify("Skater added successfully!", type="positive")
                        dialog.close()
                        refresh_table()

                    ui.button("Save", on_click=save_skater).props("color=primary")

            dialog.open()

        def edit_skater_dialog(skater_id):
            session = get_session()
            from database import get_skater

            skater = get_skater(session, skater_id)

            if not skater:
                session.close()
                return

            with ui.dialog() as dialog, ui.card().classes("p-6 w-96"):
                ui.label("Edit Skater").classes("text-xl font-bold mb-4")

                name_input = (
                    ui.input("Name *", value=skater.name)
                    .classes("w-full")
                    .props("outlined")
                )
                derby_input = (
                    ui.input("Derby Name", value=skater.derby_name or "")
                    .classes("w-full")
                    .props("outlined")
                )
                email_input = (
                    ui.input("Skater Email", value=skater.email or "")
                    .classes("w-full")
                    .props("outlined")
                )
                phone_input = (
                    ui.input("Skater Phone", value=skater.phone or "")
                    .classes("w-full")
                    .props("outlined")
                )

                ui.label("Guardian Information").classes(
                    "text-lg font-semibold mt-4 mb-2"
                )
                guardian_name_input = (
                    ui.input("Guardian Name", value=skater.guardian_name or "")
                    .classes("w-full")
                    .props("outlined")
                )
                guardian_email_input = (
                    ui.input("Guardian Email", value=skater.guardian_email or "")
                    .classes("w-full")
                    .props("outlined")
                )
                guardian_phone_input = (
                    ui.input("Guardian Phone", value=skater.guardian_phone or "")
                    .classes("w-full")
                    .props("outlined")
                )

                is_coach_checkbox = ui.checkbox(
                    "This person is a coach", value=skater.is_coach
                )
                active_checkbox = ui.checkbox("Active", value=skater.active)

                with ui.row().classes("w-full justify-end gap-2 mt-4"):
                    ui.button("Cancel", on_click=dialog.close).props("flat")

                    def save_changes():
                        if not name_input.value:
                            ui.notify("Name is required", type="negative")
                            return

                        update_skater(
                            session,
                            skater_id,
                            name=name_input.value,
                            derby_name=derby_input.value or None,
                            email=email_input.value or None,
                            phone=phone_input.value or None,
                            guardian_name=guardian_name_input.value or None,
                            guardian_email=guardian_email_input.value or None,
                            guardian_phone=guardian_phone_input.value or None,
                            is_coach=is_coach_checkbox.value,
                            active=active_checkbox.value,
                        )
                        session.close()

                        ui.notify("Skater updated successfully!", type="positive")
                        dialog.close()
                        refresh_table()

                    ui.button("Save", on_click=save_changes).props("color=primary")

            dialog.open()

        def delete_skater_confirm(skater_id):
            with ui.dialog() as dialog, ui.card().classes("p-6"):
                ui.label("Confirm Delete").classes("text-xl font-bold mb-4")
                ui.label("Are you sure you want to deactivate this skater?")

                with ui.row().classes("w-full justify-end gap-2 mt-4"):
                    ui.button("Cancel", on_click=dialog.close).props("flat")

                    def confirm_delete():
                        session = get_session()
                        delete_skater(session, skater_id)
                        session.close()

                        ui.notify("Skater deactivated", type="positive")
                        dialog.close()
                        refresh_table()

                    ui.button("Delete", on_click=confirm_delete).props("color=negative")

            dialog.open()

        # Add skater button
        ui.button("➕ Add Skater", on_click=add_skater_dialog).props(
            "color=primary size=lg"
        )

        # Initial table load
        refresh_table()


# ==================== PRACTICES PAGE ====================
@ui.page("/practices")
def practices_page():
    apply_custom_styles()

    with ui.column().classes("main-container"):
        ui.label("📅 Practice Management").classes("page-title")
        create_navigation()

        # Container for the table
        table_container = ui.column().classes("w-full")

        def refresh_table():
            table_container.clear()
            with table_container:
                session = get_session()
                practices = get_all_practices(session)
                skaters = get_all_skaters(session, active_only=True)

                if practices:
                    rows = []
                    for p in practices:
                        attendance_records = get_attendance(session, p.id)
                        present_count = sum(
                            1 for a in attendance_records if a.status == "present"
                        )

                        rows.append(
                            {
                                "id": p.id,
                                "date": p.date,
                                "time": f"{p.start_time or 'N/A'} - {p.end_time or 'N/A'}",
                                "location": p.location or "-",
                                "attendance": f"{present_count}/{len(skaters)}",
                                "notes": p.notes or "-",
                            }
                        )

                    table = ui.table(
                        columns=[
                            {
                                "name": "date",
                                "label": "Date",
                                "field": "date",
                                "align": "left",
                            },
                            {
                                "name": "time",
                                "label": "Time",
                                "field": "time",
                                "align": "left",
                            },
                            {
                                "name": "location",
                                "label": "Location",
                                "field": "location",
                                "align": "left",
                            },
                            {
                                "name": "attendance",
                                "label": "Attendance",
                                "field": "attendance",
                                "align": "center",
                            },
                            {
                                "name": "notes",
                                "label": "Notes",
                                "field": "notes",
                                "align": "left",
                            },
                            {
                                "name": "actions",
                                "label": "Actions",
                                "field": "actions",
                                "align": "center",
                            },
                        ],
                        rows=rows,
                    ).classes("w-full")

                    table.add_slot(
                        "body-cell-actions",
                        """
                        <q-td :props="props">
                            <q-btn size="sm" flat dense icon="delete" color="negative" @click="$parent.$emit('delete', props.row)" />
                        </q-td>
                    """,
                    )

                    table.on("delete", lambda e: delete_practice_confirm(e.args["id"]))
                else:
                    ui.label(
                        "No practices scheduled yet. Add your first practice!"
                    ).classes("text-gray-500")

                session.close()

        def add_practice_dialog():
            with ui.dialog() as dialog, ui.card().classes("p-6"):
                ui.label("Add New Practice").classes("text-xl font-bold mb-4")

                date_input = (
                    ui.input("Date (YYYY-MM-DD) *", value=date.today().isoformat())
                    .classes("w-full")
                    .props("outlined")
                )
                start_input = (
                    ui.input("Start Time (HH:MM)", placeholder="19:00")
                    .classes("w-full")
                    .props("outlined")
                )
                end_input = (
                    ui.input("End Time (HH:MM)", placeholder="21:00")
                    .classes("w-full")
                    .props("outlined")
                )
                location_input = (
                    ui.input("Location").classes("w-full").props("outlined")
                )
                notes_input = ui.textarea("Notes").classes("w-full").props("outlined")

                with ui.row().classes("w-full justify-end gap-2 mt-4"):
                    ui.button("Cancel", on_click=dialog.close).props("flat")

                    def save_practice():
                        if not date_input.value:
                            ui.notify("Date is required", type="negative")
                            return

                        session = get_session()
                        create_practice(
                            session,
                            date=date_input.value,
                            start_time=start_input.value or None,
                            end_time=end_input.value or None,
                            location=location_input.value or None,
                            notes=notes_input.value or None,
                        )
                        session.close()

                        ui.notify("Practice added successfully!", type="positive")
                        dialog.close()
                        refresh_table()

                    ui.button("Save", on_click=save_practice).props("color=primary")

            dialog.open()

        def delete_practice_confirm(practice_id):
            with ui.dialog() as dialog, ui.card().classes("p-6"):
                ui.label("Confirm Delete").classes("text-xl font-bold mb-4")
                ui.label(
                    "Are you sure you want to delete this practice? All attendance records will be removed."
                )

                with ui.row().classes("w-full justify-end gap-2 mt-4"):
                    ui.button("Cancel", on_click=dialog.close).props("flat")

                    def confirm_delete():
                        session = get_session()
                        delete_practice(session, practice_id)
                        session.close()

                        ui.notify("Practice deleted", type="positive")
                        dialog.close()
                        refresh_table()

                    ui.button("Delete", on_click=confirm_delete).props("color=negative")

            dialog.open()

        ui.button("➕ Add Practice", on_click=add_practice_dialog).props(
            "color=primary size=lg"
        )

        refresh_table()


# ==================== ATTENDANCE PAGE ====================
@ui.page("/attendance")
def attendance_page():
    apply_custom_styles()

    with ui.column().classes("main-container"):
        ui.label("✓ Attendance Tracking").classes("page-title")
        create_navigation()

        session = get_session()
        practices = get_all_practices(session, limit=20)
        session.close()

        if not practices:
            ui.label("No practices available. Please create a practice first.").classes(
                "text-gray-500"
            )
            return

        # Practice selector
        practice_options = {
            p.id: f"{p.date} - {p.location or 'Practice'}" for p in practices
        }
        selected_practice = practices[0].id

        attendance_container = ui.column().classes("w-full")

        def load_attendance(practice_id):
            attendance_container.clear()

            with attendance_container:
                session = get_session()
                skaters = get_all_skaters(session, active_only=True)
                attendance_records = get_attendance(session, practice_id)

                # Create a map of skater_id -> attendance status
                attendance_map = {a.skater_id: a.status for a in attendance_records}

                ui.label(
                    f"Mark Attendance for {practice_options[practice_id]}"
                ).classes("section-title")

                if skaters:
                    with ui.column().classes("attendance-grid w-full"):
                        for skater in skaters:
                            current_status = attendance_map.get(skater.id, "absent")

                            with ui.row().classes("attendance-row"):
                                with ui.column().classes("gap-0"):
                                    with ui.row().classes("gap-2 items-center"):
                                        ui.label(skater.name).classes("skater-name")
                                        if skater.is_coach:
                                            ui.label("⭐ COACH").classes("coach-badge")
                                    if skater.derby_name:
                                        ui.label(f'"{skater.derby_name}"').classes(
                                            "derby-name"
                                        )

                                with ui.row().classes("gap-2"):

                                    def make_handler(s_id, status):
                                        def handler():
                                            sess = get_session()
                                            set_attendance(
                                                sess, practice_id, s_id, status
                                            )
                                            sess.close()
                                            ui.notify(
                                                f"Marked as {status}", type="positive"
                                            )
                                            load_attendance(practice_id)

                                        return handler

                                    ui.button(
                                        "Present",
                                        on_click=make_handler(skater.id, "present"),
                                    ).props(
                                        f"{'' if current_status == 'present' else 'outline'} color=positive"
                                    )
                                    ui.button(
                                        "Absent",
                                        on_click=make_handler(skater.id, "absent"),
                                    ).props(
                                        f"{'' if current_status == 'absent' else 'outline'} color=negative"
                                    )
                                    ui.button(
                                        "Excused",
                                        on_click=make_handler(skater.id, "excused"),
                                    ).props(
                                        f"{'' if current_status == 'excused' else 'outline'} color=warning"
                                    )

                    # Summary
                    present_count = sum(
                        1 for s in attendance_map.values() if s == "present"
                    )
                    absent_count = sum(
                        1 for s in attendance_map.values() if s == "absent"
                    )
                    excused_count = sum(
                        1 for s in attendance_map.values() if s == "excused"
                    )

                    ui.label("Summary").classes("section-title")
                    with ui.row().classes("gap-4"):
                        ui.label(f"✓ Present: {present_count}").classes(
                            "text-lg text-green-600 font-semibold"
                        )
                        ui.label(f"✗ Absent: {absent_count}").classes(
                            "text-lg text-red-600 font-semibold"
                        )
                        ui.label(f"⊘ Excused: {excused_count}").classes(
                            "text-lg text-orange-600 font-semibold"
                        )
                else:
                    ui.label("No active skaters found.").classes("text-gray-500")

                session.close()

        # Practice selector dropdown
        practice_select = (
            ui.select(
                options=practice_options,
                value=selected_practice,
                label="Select Practice",
            )
            .classes("w-full max-w-md")
            .props("outlined")
        )

        practice_select.on("update:model-value", lambda e: load_attendance(e.value))

        # Load initial attendance
        load_attendance(selected_practice)


# ==================== RUN APPLICATION ====================
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="Junior Roller Derby Attendance Tracker",
        port=8080,
        reload=False,
        show=True,
    )
