"""SQLite storage for Muscle Cafe profiles, measurements and workout logs."""

import sqlite3
from datetime import date, datetime

DB_NAME = "muscle_cafe.db"


def get_connection():
    """Open a connection to the project's SQLite database."""
    return sqlite3.connect(DB_NAME)


def _date_to_text(value):
    """Convert a date or datetime value to YYYY-MM-DD text."""
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return str(value)


def create_table():
    """Create all Muscle Cafe tables if they do not already exist."""
    conn = get_connection()
    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                height REAL NOT NULL,
                weight REAL NOT NULL,
                experience TEXT,
                goal TEXT,
                diet TEXT,
                workout_minutes INTEGER,
                wake_time TEXT,
                sleep_time TEXT
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS body_measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_date TEXT NOT NULL,
                weight_kg REAL NOT NULL CHECK(weight_kg > 0),
                waist_cm REAL,
                chest_cm REAL,
                arm_cm REAL,
                hip_cm REAL,
                notes TEXT DEFAULT '',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS workout_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_date TEXT NOT NULL,
                muscle_group TEXT NOT NULL,
                exercise_name TEXT NOT NULL,
                sets INTEGER NOT NULL CHECK(sets > 0),
                reps INTEGER NOT NULL CHECK(reps > 0),
                load_kg REAL NOT NULL DEFAULT 0 CHECK(load_kg >= 0),
                notes TEXT DEFAULT '',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def save_profile(data):
    """Save a user profile using parameterised SQL."""
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO users (
                name, age, height, weight, experience, goal, diet,
                workout_minutes, wake_time, sleep_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["name"],
                data["age"],
                data["height"],
                data["weight"],
                data.get("experience"),
                data.get("goal"),
                data.get("diet"),
                data.get("workout_minutes"),
                data.get("wake_time"),
                data.get("sleep_time"),
            ),
        )
        conn.commit()
    finally:
        conn.close()


def get_latest_profile():
    """Return the newest profile as a plain tuple, or None.

    main.py reads it by position (profile[1] = name ... profile[10] = sleep_time),
    so do NOT set row_factory here.
    """
    conn = get_connection()
    try:
        return conn.execute(
            "SELECT * FROM users ORDER BY id DESC LIMIT 1"
        ).fetchone()
    finally:
        conn.close()


def save_body_measurement(entry_date, weight_kg, waist_cm=None, chest_cm=None,
                          arm_cm=None, hip_cm=None, notes=""):
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO body_measurements
                (entry_date, weight_kg, waist_cm, chest_cm, arm_cm, hip_cm, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (_date_to_text(entry_date), float(weight_kg), waist_cm, chest_cm,
             arm_cm, hip_cm, (notes or "").strip()),
        )
        conn.commit()
    finally:
        conn.close()


def get_body_measurements():
    """Return a list of dicts, oldest first (main.py uses [-1] as the latest)."""
    conn = get_connection()
    try:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM body_measurements ORDER BY entry_date, id"
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def save_workout_log(entry_date, muscle_group, exercise_name, sets, reps,
                     load_kg=0.0, notes=""):
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO workout_logs
                (entry_date, muscle_group, exercise_name, sets, reps, load_kg, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (_date_to_text(entry_date), muscle_group, exercise_name.strip(),
             int(sets), int(reps), float(load_kg), (notes or "").strip()),
        )
        conn.commit()
    finally:
        conn.close()


def get_workout_logs():
    """Return a list of dicts, oldest first."""
    conn = get_connection()
    try:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM workout_logs ORDER BY entry_date, id"
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()