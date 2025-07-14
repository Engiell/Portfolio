from typing import Optional, List, Dict
from database import get_connection

def add_user(name: str, email: str, password: str) -> int:
    """
    Insert a new user and return its user_id.
    Raises sqlite3.IntegrityError if email is already taken.
    """
    sql = "INSERT INTO Users (name, email, password_hash) VALUES (?, ?, ?);"
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, (name, email, password))
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return user_id

def get_user_by_email(email: str) -> Optional[int]:
    """
    Return the user_id for the given email, or None if not found.
    """
    sql = "SELECT user_id FROM Users WHERE email = ?;"
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, (email,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def authenticate_user(user_id: int, password: str) -> bool:
    """
    Return True if the given user_id/password pair matches.
    """
    sql = "SELECT password_hash FROM Users WHERE user_id = ?;"
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, (user_id,))
    row = cur.fetchone()
    conn.close()
    return bool(row and row[0] == password)

def add_user_profile(user_id: int, location: str, created_date: str) -> int:
    """
    Insert a new user profile record and return its profile_id.
    """
    sql = """
        INSERT INTO UserProfiles (user_id, location, created_date)
        VALUES (?, ?, ?);
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, (user_id, location, created_date))
    conn.commit()
    profile_id = cur.lastrowid
    conn.close()
    return profile_id

def add_destination(city: str, country: str, description: str = None) -> int:
    """
    Insert a new destination and return its destination_id.
    """
    sql = "INSERT INTO Destinations (city, country, description) VALUES (?, ?, ?);"
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, (city, country, description))
    conn.commit()
    dest_id = cur.lastrowid
    conn.close()
    return dest_id

def get_destination_by_city(city: str) -> Optional[int]:
    """
    Return the destination_id for the given city, or None if not found.
    """
    sql = "SELECT destination_id FROM Destinations WHERE city = ?;"
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, (city,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def create_itinerary(user_id: int, start_date: str, end_date: str) -> int:
    """
    Insert a new itinerary header and return its itinerary_id.
    """
    sql = "INSERT INTO ItineraryHeaders (user_id, start_date, end_date) VALUES (?, ?, ?);"
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, (user_id, start_date, end_date))
    conn.commit()
    itin_id = cur.lastrowid
    conn.close()
    return itin_id

def add_itinerary_detail(itin_id: int, dest_id: int,
                         accommodation: str = None, notes: str = None) -> int:
    """
    Insert a new itinerary detail record and return its detail_id.
    """
    sql = """
        INSERT INTO ItineraryDetails
          (itinerary_id, destination_id, accommodation, notes)
        VALUES (?, ?, ?, ?);
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, (itin_id, dest_id, accommodation, notes))
    conn.commit()
    detail_id = cur.lastrowid
    conn.close()
    return detail_id

def get_user_itineraries(user_id: int, start_date: str) -> List[Dict]:
    """
    Return a list of dicts for this user's itinerary items
    with start_date >= the given date.
    """
    sql = """
        SELECT h.itinerary_id,
               h.start_date,
               h.end_date,
               d.city,
               d.country,
               dt.accommodation,
               dt.notes
          FROM ItineraryHeaders h
          JOIN ItineraryDetails dt
            ON dt.itinerary_id = h.itinerary_id
          JOIN Destinations d
            ON d.destination_id = dt.destination_id
         WHERE h.user_id = ? AND h.start_date >= ?
         ORDER BY h.start_date;
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, (user_id, start_date))
    cols = [col[0] for col in cur.description]
    rows = cur.fetchall()
    conn.close()
    return [dict(zip(cols, row)) for row in rows]