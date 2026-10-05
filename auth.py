import sqlite3
from database import get_connection


def register_user(name, email, password):

    email = email.strip().lower()
    name = name.strip()

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
            """,
            (name, email, password)
        )

        connection.commit()

        return {
            "success": True,
            "message": "Registration successful"
        }

    except sqlite3.IntegrityError:

        return {
            "success": False,
            "message": "Email already registered"
        }

    finally:

        connection.close()


def login_user(email, password):

    email = email.strip().lower()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, email
        FROM users
        WHERE LOWER(email) = ? AND password = ?
        """,
        (email, password)
    )

    user = cursor.fetchone()

    connection.close()

    if user:

        return {
            "success": True,
            "user": {
                "id": user[0],
                "name": user[1],
                "email": user[2]
            }
        }

    return {
        "success": False,
        "message": "Invalid email or password"
    }