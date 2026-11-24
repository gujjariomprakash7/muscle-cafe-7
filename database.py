"""SQLite storage and authentication for the Muscle Cafe prototype.

Each account owns its own profile, body measurements and workout logs.
Passwords are stored as salted PBKDF2-HMAC-SHA256 hashes, never in plaintext.
"""

import hashlib
import hmac
import re
import secrets
import sqlite3
from datetime import date, datetime
from pathlib import Path

DB_NAME = "muscle_cafe.db"
PASSWORD_ITERATIONS = 310_000


def get_connection():
    """Open a connection to the project's SQLite database."""
    conn = sqlite3.connect(DB_NAME, timeout=20)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _date_to_text(value):
    """Convert a date or datetime value to YYYY-MM-DD text."""
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return str(value)


def _ensure_column(conn, table_name, column_name, definition):
    """Add a nullable migration column when upgrading an older local database."""
    existing = {
        row[1] for row in conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    }
    if column_name not in existing:
        conn.execute(
            f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}"
        )


def create_table():
    """Create tables and safely add account ownership to an older database."""
    conn = get_connection()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL COLLATE NOCASE UNIQUE,
                password_salt TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # `users` is the existing profile table; accounts are now separate.
        conn.execute(
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
                sleep_time TEXT,
                account_id INTEGER REFERENCES accounts(id)
            )
            """
        )
        conn.execute(
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
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                account_id INTEGER REFERENCES accounts(id)
            )
            """
        )
        conn.execute(
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
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                account_id INTEGER REFERENCES accounts(id)
            )
            """
        )

        # Migrate tables created by earlier single-user versions.
        _ensure_column(conn, "users", "account_id", "INTEGER REFERENCES accounts(id)")
        _ensure_column(
            conn, "body_measurements", "account_id", "INTEGER REFERENCES accounts(id)"
        )
        _ensure_column(
            conn, "workout_logs", "account_id", "INTEGER REFERENCES accounts(id)"
        )

        conn.execute("CREATE INDEX IF NOT EXISTS idx_profiles_account ON users(account_id, id)")
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_body_account_date "
            "ON body_measurements(account_id, entry_date, id)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_workout_account_date "
            "ON workout_logs(account_id, entry_date, id)"
        )
        conn.commit()
    finally:
        conn.close()


def _normalise_email(email):
    return str(email).strip().lower()


def register_account(email, password):
    """Create an account. Returns (account_id, error_message)."""
    email = _normalise_email(email)
    password = str(password)

    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        return None, "Enter a valid email address."
    if len(password) < 8:
        return None, "Use a password with at least 8 characters."

    salt = secrets.token_bytes(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PASSWORD_ITERATIONS
    )

    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO accounts (email, password_salt, password_hash) VALUES (?, ?, ?)",
            (email, salt.hex(), password_hash.hex()),
        )
        conn.commit()
        return int(cursor.lastrowid), None
    except sqlite3.IntegrityError:
        return None, "An account with this email already exists. Please sign in instead."
    finally:
        conn.close()


def authenticate_user(email, password):
    """Verify credentials and return {id, email}, or None when invalid."""
    email = _normalise_email(email)
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT id, email, password_salt, password_hash FROM accounts WHERE email = ? COLLATE NOCASE",
            (email,),
        ).fetchone()
    finally:
        conn.close()

    if row is None:
        return None

    salt = bytes.fromhex(row[2])
    expected_hash = bytes.fromhex(row[3])
    supplied_hash = hashlib.pbkdf2_hmac(
        "sha256", str(password).encode("utf-8"), salt, PASSWORD_ITERATIONS
    )
    if not hmac.compare_digest(expected_hash, supplied_hash):
        return None

    return {"id": int(row[0]), "email": row[1]}


def save_profile(data, account_id):
    """Save a profile belonging to one authenticated account."""
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO users (
                name, age, height, weight, experience, goal, diet,
                workout_minutes, wake_time, sleep_time, account_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["name"], data["age"], data["height"], data["weight"],
                data["experience"], data["goal"], data["diet"],
                data["workout_minutes"], data["wake_time"], data["sleep_time"],
                int(account_id),
            ),
        )
        conn.commit()
    finally:
        conn.close()


def get_latest_profile(account_id):
    """Return the latest profile for an account as a tuple, or None."""
    conn = get_connection()
    try:
        return conn.execute(
            "SELECT * FROM users WHERE account_id = ? ORDER BY id DESC LIMIT 1",
            (int(account_id),),
        ).fetchone()
    finally:
        conn.close()


def save_body_measurement(
    *, account_id, entry_date, weight_kg, waist_cm=None, chest_cm=None,
    arm_cm=None, hip_cm=None, notes=""
):
    """Save a dated body check-in for one account."""
    date_text = _date_to_text(entry_date)
    weight_value = float(weight_kg)
    if not 20 <= weight_value <= 300:
        raise ValueError("Weight must be between 20 and 300 kg.")

    optional_values = []
    for label, value in (("waist", waist_cm), ("chest", chest_cm), ("arm", arm_cm), ("hip", hip_cm)):
        if value in (None, ""):
            optional_values.append(None)
        else:
            number = float(value)
            if not 0 < number <= 250:
                raise ValueError(f"{label.title()} measurement must be between 0 and 250 cm.")
            optional_values.append(number)

    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO body_measurements (
                entry_date, weight_kg, waist_cm, chest_cm, arm_cm, hip_cm,
                notes, account_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (date_text, weight_value, *optional_values, str(notes).strip(), int(account_id)),
        )
        conn.commit()
    finally:
        conn.close()


def get_body_measurements(account_id):
    """Return only this account's body check-ins as dictionaries."""
    conn = get_connection()
    try:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM body_measurements WHERE account_id = ? ORDER BY entry_date, id",
            (int(account_id),),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def save_workout_log(
    *, account_id, entry_date, muscle_group, exercise_name, sets, reps,
    load_kg=0, notes=""
):
    """Save one exercise log for one account. Load 0 may represent bodyweight."""
    date_text = _date_to_text(entry_date)
    exercise = str(exercise_name).strip()
    if not exercise:
        raise ValueError("Enter an exercise name.")

    sets_value = int(sets)
    reps_value = int(reps)
    load_value = float(load_kg)
    if not 1 <= sets_value <= 30:
        raise ValueError("Sets must be between 1 and 30.")
    if not 1 <= reps_value <= 200:
        raise ValueError("Reps must be between 1 and 200.")
    if not 0 <= load_value <= 1000:
        raise ValueError("Load must be between 0 and 1000 kg.")

    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO workout_logs (
                entry_date, muscle_group, exercise_name, sets, reps, load_kg,
                notes, account_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                date_text, str(muscle_group).strip(), exercise, sets_value,
                reps_value, load_value, str(notes).strip(), int(account_id),
            ),
        )
        conn.commit()
    finally:
        conn.close()


def get_workout_logs(account_id):
    """Return only this account's workout history as dictionaries."""
    conn = get_connection()
    try:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM workout_logs WHERE account_id = ? ORDER BY entry_date DESC, id DESC",
            (int(account_id),),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()
