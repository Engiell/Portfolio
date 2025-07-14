import sqlite3
import os

DB_FILENAME = 'snhu_travel.db'

def get_connection():
    conn = sqlite3.connect(DB_FILENAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def initialize_db():
    """Create tables if they don't exist."""
    exists = os.path.exists(DB_FILENAME)
    print(f"{'Using' if exists else 'Creating'} database {DB_FILENAME}")

    ddl_statements = [
        # Users table
        """
        CREATE TABLE IF NOT EXISTS Users (
            user_id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    NOT NULL UNIQUE,
            password_hash TEXT    NOT NULL
        );
        """,

        # Destinations (unchanged)
        """
        CREATE TABLE IF NOT EXISTS Destinations (
            destination_id INTEGER PRIMARY KEY AUTOINCREMENT,
            city           TEXT    NOT NULL,
            country        TEXT    NOT NULL,
            description    TEXT
        );
        """,

        # Itinerary headers (unchanged)
        """
        CREATE TABLE IF NOT EXISTS ItineraryHeaders (
            itinerary_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER NOT NULL,
            start_date   TEXT,
            end_date     TEXT,
            FOREIGN KEY(user_id) 
                REFERENCES Users(user_id)
                  ON DELETE CASCADE
        );
        """,

        # Itinerary details (unchanged)
        """
        CREATE TABLE IF NOT EXISTS ItineraryDetails (
            detail_id      INTEGER PRIMARY KEY AUTOINCREMENT,
            itinerary_id   INTEGER NOT NULL,
            destination_id INTEGER NOT NULL,
            accommodation  TEXT,
            notes          TEXT,
            FOREIGN KEY(itinerary_id) 
                REFERENCES ItineraryHeaders(itinerary_id)
                  ON DELETE CASCADE,
            FOREIGN KEY(destination_id)
                REFERENCES Destinations(destination_id)
                  ON DELETE RESTRICT
        );
        """,

        # New: UserProfiles table to store extra info
        """
        CREATE TABLE IF NOT EXISTS UserProfiles (
            profile_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER NOT NULL,
            location     TEXT,
            created_date TEXT,
            FOREIGN KEY(user_id)
                REFERENCES Users(user_id)
                  ON DELETE CASCADE
        );
        """
    ]

    conn = get_connection()
    cur = conn.cursor()
    for stmt in ddl_statements:
        cur.execute(stmt)
    conn.commit()
    conn.close()
    print("Database schema initialized.")